/**
 * utils/dify-api.js — Dify 对话型应用 API 封装
 *
 * 所有请求走本地 Nginx /ai/* → Dify 服务 :21326
 * 鉴权: Authorization: Bearer {DIFY_API_KEY}
 * 用户标识: user 参数 (来自 DB 服务 USER_INFO 返回的 id)
 *
 * Dify SSE 流式事件类型:
 *   message       — LLM 文本块 (answer 字段)
 *   message_end   — 消息结束 (含 metadata)
 *   message_file  — 文件事件 (id, url)
 *   error         — 错误事件
 *   ping          — 心跳 (每 10s)
 */

const { API } = require('../config/api.js');

// ==================== 工具函数 ====================

/** ArrayBuffer → UTF-8 字符串 */
function buf2str(buffer) {
  if (typeof buffer === 'string') return buffer;
  if (buffer instanceof ArrayBuffer) {
    const bytes = new Uint8Array(buffer);
    let str = '';
    for (let i = 0; i < bytes.length; i++) {
      str += '%' + ('00' + bytes[i].toString(16)).slice(-2);
    }
    try { return decodeURIComponent(str); } catch (e) { return str; }
  }
  return String(buffer || '');
}

// ==================== API 方法 ====================

/**
 * 上传文件到 Dify（图片等）
 * @param {string} filePath - 微信临时文件路径
 * @param {string} userId   - 终端用户标识
 * @returns {Promise<{id, name, size, extension, mime_type}>}
 */
function uploadFile(filePath, userId) {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: API.AI_FILE_UPLOAD,
      filePath,
      name: 'file',
      formData: { user: userId },
      header: { 'Authorization': `Bearer ${API.DIFY_API_KEY}` },
      success(res) {
        try {
          const data = JSON.parse(res.data);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(data);
          } else {
            reject(new Error(data.message || data.code || '上传失败'));
          }
        } catch (e) {
          reject(new Error('解析上传响应失败'));
        }
      },
      fail(err) {
        reject(new Error(err.errMsg || '网络异常'));
      }
    });
  });
}

/**
 * 发送对话消息（SSE 流式）
 *
 * @param {Object} options
 * @param {string} options.query          - 用户输入内容
 * @param {string} options.userId         - 终端用户标识
 * @param {string} [options.conversationId] - 会话 ID（续接历史对话）
 * @param {Array}  [options.files]        - 文件列表 [{type, transfer_method, upload_file_id}]
 * @param {Function} options.onToken      - token 回调 (token: string)
 * @param {Function} options.onConvId     - 会话 ID 回调 (conversationId: string)
 * @param {Function} options.onTaskId     - 任务 ID 回调 (taskId: string)
 * @param {Function} options.onFile       - 文件回调 ({id, type, url})
 * @param {Function} options.onDone       - 完成回调 (conversationId: string)
 * @param {Function} options.onError      - 错误回调 (error: Error)
 * @returns {wx.RequestTask} 可调用 .abort() 停止
 */
function sendChatMessage(options) {
  const {
    query, userId, conversationId, files,
    onToken, onConvId, onTaskId, onFile,
    onDone, onError,
  } = options;

  let convId = conversationId || '';
  let taskId = '';

  const requestTask = wx.request({
    url: API.AI_CHAT,
    method: 'POST',
    enableChunked: true,
    header: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API.DIFY_API_KEY}`
    },
    data: {
      inputs: {},
      query,
      response_mode: 'streaming',
      user: userId,
      conversation_id: convId,
      files: files || [],
      auto_generate_name: true,
    },
    success(res) {
      // 非 200 走 onError
      if (res.statusCode !== 200) {
        try {
          const errData = JSON.parse(res.data);
          if (onError) onError(new Error(errData.message || errData.code || `请求失败(${res.statusCode})`));
        } catch (e) {
          if (onError) onError(new Error(`请求失败(${res.statusCode})`));
        }
      }
    },
    fail(err) {
      if (onError) onError(new Error(err.errMsg || '网络异常'));
    }
  });

  let buffer = '';

  requestTask.onChunkReceived(res => {
    try {
      const chunk = buf2str(res.data);
      buffer += chunk;

      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith('data: ')) continue;

        const jsonStr = trimmed.slice(6);
        let json;
        try { json = JSON.parse(jsonStr); } catch (e) { continue; }

        switch (json.event) {
          case 'message':
          case 'agent_message':
            if (json.answer && onToken) onToken(json.answer);
            if (json.conversation_id && !convId) {
              convId = json.conversation_id;
              if (onConvId) onConvId(json.conversation_id);
            }
            if (json.task_id && !taskId) {
              taskId = json.task_id;
              if (onTaskId) onTaskId(json.task_id);
            }
            break;

          case 'message_file':
            if (onFile) onFile({ id: json.id, type: json.type, url: json.url });
            break;

          case 'message_end':
            if (onDone) onDone(json.conversation_id || convId);
            return;

          case 'error':
            if (onError) onError(new Error(json.message || '服务异常'));
            return;

          case 'ping':
            break;

          default:
            break;
        }
      }
    } catch (e) {
      // 解析异常忽略，buffer 中的残留数据会在下一个 chunk 重试
    }
  });

  return requestTask;
}

/**
 * 停止流式响应
 * @param {string} taskId - 任务 ID
 * @param {string} userId - 用户标识
 */
function stopResponse(taskId, userId) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${API.AI_CHAT}/${taskId}/stop`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API.DIFY_API_KEY}`
      },
      data: { user: userId },
      success(res) {
        if (res.statusCode === 200) resolve(res.data);
        else reject(new Error('停止失败'));
      },
      fail(err) { reject(err); }
    });
  });
}

/**
 * 获取会话列表
 * @param {string} userId - 用户标识
 * @param {string} [lastId] - 分页游标
 * @param {number} [limit=20] - 每页数量
 */
function getConversations(userId, lastId, limit = 20) {
  return new Promise((resolve, reject) => {
    let url = `${API.AI_CONVERSATIONS}?user=${encodeURIComponent(userId)}&limit=${limit}`;
    if (lastId) url += `&last_id=${lastId}`;

    wx.request({
      url,
      method: 'GET',
      header: { 'Authorization': `Bearer ${API.DIFY_API_KEY}` },
      success(res) {
        if (res.statusCode === 200) resolve(res.data);
        else reject(new Error('获取会话列表失败'));
      },
      fail(err) { reject(err); }
    });
  });
}

/**
 * 获取会话历史消息（倒序，最新在前）
 * @param {string} conversationId - 会话 ID
 * @param {string} userId - 用户标识
 * @param {string} [firstId] - 分页游标
 * @param {number} [limit=20] - 每页数量
 */
function getMessages(conversationId, userId, firstId, limit = 20) {
  return new Promise((resolve, reject) => {
    let url = `${API.AI_MESSAGES}?user=${encodeURIComponent(userId)}&conversation_id=${conversationId}&limit=${limit}`;
    if (firstId) url += `&first_id=${firstId}`;

    wx.request({
      url,
      method: 'GET',
      header: { 'Authorization': `Bearer ${API.DIFY_API_KEY}` },
      success(res) {
        if (res.statusCode === 200) resolve(res.data);
        else reject(new Error('获取消息失败'));
      },
      fail(err) { reject(err); }
    });
  });
}

/**
 * 删除会话
 * @param {string} conversationId - 会话 ID
 * @param {string} userId - 用户标识
 */
function deleteConversation(conversationId, userId) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${API.AI_CONVERSATIONS}/${conversationId}`,
      method: 'DELETE',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API.DIFY_API_KEY}`
      },
      data: { user: userId },
      success(res) {
        if (res.statusCode === 204 || res.statusCode === 200) resolve();
        else reject(new Error('删除失败'));
      },
      fail(err) { reject(err); }
    });
  });
}

/**
 * 发送消息反馈（点赞/点踩）
 * @param {string} messageId - 消息 ID
 * @param {string} rating - like / dislike / null
 * @param {string} userId - 用户标识
 * @param {string} [content] - 反馈内容
 */
function sendFeedback(messageId, rating, userId, content) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${API.AI_FEEDBACK}/${messageId}/feedbacks`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API.DIFY_API_KEY}`
      },
      data: { rating, user: userId, content: content || '' },
      success(res) {
        if (res.statusCode === 200) resolve(res.data);
        else reject(new Error('反馈失败'));
      },
      fail(err) { reject(err); }
    });
  });
}

/**
 * 获取应用参数（开场白、推荐问题、文件上传配置等）
 */
function getAppParameters() {
  return new Promise((resolve, reject) => {
    wx.request({
      url: API.AI_PARAMETERS,
      method: 'GET',
      header: { 'Authorization': `Bearer ${API.DIFY_API_KEY}` },
      success(res) {
        if (res.statusCode === 200) resolve(res.data);
        else reject(new Error('获取参数失败'));
      },
      fail(err) { reject(err); }
    });
  });
}

module.exports = {
  uploadFile,
  sendChatMessage,
  stopResponse,
  getConversations,
  getMessages,
  deleteConversation,
  sendFeedback,
  getAppParameters,
};
