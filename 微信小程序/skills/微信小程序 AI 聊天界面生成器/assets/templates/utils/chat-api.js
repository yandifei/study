/**
 * chat-api.js — AI 对话 API 封装
 *
 * 提供三种模式：
 *   1. MockAPI — 本地模拟，无需后端，适合原型开发和演示
 *   2. streamChat — SSE 流式对接真实后端（DeepSeek/OpenAI 兼容格式）
 *   3. DifyAPI — Dify 对话型应用完整 API（SSE 流式、文件上传、反馈、会话管理）
 *
 * 使用方式：
 *   const { MockAPI, streamChat, DifyAPI } = require('../../utils/chat-api');
 */

// ==================== 配置 ====================

/** 真实 API 默认地址（DeepSeek API） */
const DEFAULT_API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';

/** API Key（建议通过环境变量或后端代理管理，不要硬编码在前端） */
let API_KEY = '';

/**
 * 设置 API Key
 * @param {string} key
 */
function setApiKey(key) {
  API_KEY = key;
}

/**
 * 获取 API Key（优先从全局配置读取）
 */
function getApiKey() {
  return API_KEY || '';
}

// ==================== MockAPI ====================

/** 预置模拟回复 */
const MOCK_REPLIES = [
  '你好！我是 AI 助手，很高兴为你服务。\n\n我可以帮你：\n- 解答技术问题\n- 编写代码\n- 文本处理\n- 知识问答\n\n请问有什么可以帮你的？',
  '这是一个很好的问题！让我来为你详细解答。\n\n首先，我们需要理解核心概念。在计算机科学中，**算法**是解决特定问题的一系列步骤。\n\n以下是一个简单的示例：\n\n```javascript\nfunction fibonacci(n) {\n  if (n <= 1) return n;\n  return fibonacci(n - 1) + fibonacci(n - 2);\n}\n\nconsole.log(fibonacci(10)); // 输出: 55\n```\n\n> 提示：递归实现虽然简洁，但对于大数值可能存在性能问题，建议使用迭代或记忆化优化。\n\n希望这个解答对你有帮助！',
  '当然可以！以下是你要的代码实现：\n\n```python\ndef quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)\n\n# 测试\ndata = [3, 6, 8, 10, 1, 2, 1]\nprint(quick_sort(data))  # [1, 1, 2, 3, 6, 8, 10]\n```\n\n这个实现的时间复杂度为 O(n log n)（平均情况），空间复杂度为 O(n)。',
  '让我帮你分析一下这个问题。\n\n| 方案 | 优点 | 缺点 | 适用场景 |\n|------|------|------|----------|\n| 方案 A | 实现简单 | 性能较低 | 小规模数据 |\n| 方案 B | 性能优秀 | 复杂度高 | 大规模并发 |\n| 方案 C | 平衡性好 | 维护成本中等 | 中等规模 |\n\n综合来看，我推荐**方案 B**，因为它在长期来看能更好地支撑业务增长。',
  '好的，我理解你的需求。以下是几点建议：\n\n1. **保持代码简洁**：遵循 KISS 原则（Keep It Simple, Stupid）\n2. **注重可读性**：代码是写给人看的，顺便能在机器上运行\n3. **合理的注释**：解释 **为什么** 这样做，而不是做了什么\n4. **持续重构**：小步快跑，定期优化\n\n如果你有具体的代码需要 review，欢迎分享给我！',
];

/**
 * 本地模拟 API
 * 模拟流式输出效果：逐 token 返回，模拟真实 AI 回复体验
 */
class MockAPI {
  constructor(options = {}) {
    this.delay = options.delay || 500;       // 首 token 延迟（ms）
    this.tokenDelay = options.tokenDelay || 30; // token 间延迟（ms）
  }

  /**
   * 发送消息（模拟流式）
   * @param {Array} messages - 对话上下文 [{role, content}]
   * @param {Function} onToken - 每个 token 回调
   * @param {Function} onDone - 完成回调
   * @param {Function} onError - 错误回调
   */
  async sendMessage(messages, onToken, onDone, onError) {
    try {
      // 模拟网络延迟
      await this._sleep(this.delay);

      // 随机选择一条回复
      const reply = MOCK_REPLIES[Math.floor(Math.random() * MOCK_REPLIES.length)];

      // 逐 token 输出（模拟流式效果）
      const tokens = this._tokenize(reply);
      for (const token of tokens) {
        await this._sleep(this.tokenDelay);
        if (typeof onToken === 'function') {
          onToken(token);
        }
      }

      if (typeof onDone === 'function') {
        onDone(reply);
      }
    } catch (e) {
      if (typeof onError === 'function') {
        onError(e);
      }
    }
  }

  /**
   * 将文本拆分为 token 序列（简单模拟：按字/词拆分）
   */
  _tokenize(text) {
    const tokens = [];
    // 中英文混合拆分：中文逐字，英文逐词+标点
    const regex = /([一-鿿])|([a-zA-Z]+)|(\d+)|(\n)|([^\S\n]+)|([^\w\s])/g;
    let match;
    while ((match = regex.exec(text)) !== null) {
      tokens.push(match[0]);
    }
    // 如果正则没有匹配到（极端情况），逐字拆分
    if (tokens.length === 0) {
      for (const char of text) {
        tokens.push(char);
      }
    }
    return tokens;
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ==================== 真实 API 流式请求 ====================

/**
 * SSE 流式请求（对接 DeepSeek / OpenAI 兼容 API）
 *
 * @param {Object} options
 * @param {string} options.endpoint  - API 地址
 * @param {Array}  options.messages  - 对话上下文
 * @param {Function} options.onToken - token 回调 (token: string)
 * @param {Function} options.onDone  - 完成回调
 * @param {Function} options.onError - 错误回调 (error: Error)
 */
function streamChat(options) {
  const {
    endpoint = DEFAULT_API_ENDPOINT,
    messages = [],
    model = 'deepseek-chat',
    onToken,
    onDone,
    onError,
  } = options;

  const apiKey = getApiKey();
  if (!apiKey && endpoint === DEFAULT_API_ENDPOINT) {
    if (typeof onError === 'function') {
      onError(new Error('请先调用 setApiKey() 设置 API Key'));
    }
    return;
  }

  // 微信小程序 wx.request 流式请求
  const requestTask = wx.request({
    url: endpoint,
    method: 'POST',
    enableChunked: true,  // 开启分块传输
    header: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    data: {
      model,
      messages,
      stream: true,
    },
    success: (res) => {
      // 流式请求完成后检查
      if (res.statusCode !== 200) {
        if (typeof onError === 'function') {
          onError(new Error(`API 请求失败: ${res.statusCode}`));
        }
      }
    },
    fail: (err) => {
      if (typeof onError === 'function') {
        onError(new Error(`网络请求失败: ${err.errMsg}`));
      }
    },
  });

  // 监听分块数据
  let buffer = '';
  requestTask.onChunkReceived((res) => {
    try {
      // 将 ArrayBuffer 转为文本
      const chunk = this._arrayBufferToString(res.data);
      buffer += chunk;

      // 按行解析 SSE
      const lines = buffer.split('\n');
      // 最后一个可能是不完整的行，保留到下次
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith('data: ')) continue;

        const data = trimmed.slice(6); // 去掉 "data: " 前缀

        // [DONE] 标记
        if (data === '[DONE]') {
          if (typeof onDone === 'function') {
            onDone();
          }
          return;
        }

        try {
          const json = JSON.parse(data);
          const delta = json.choices?.[0]?.delta?.content;
          if (delta && typeof onToken === 'function') {
            onToken(delta);
          }
        } catch (e) {
          // 非 JSON 行或解析失败，跳过
        }
      }
    } catch (e) {
      // 解析异常，忽略
    }
  });
}

/**
 * ArrayBuffer → UTF-8 字符串
 */
function _arrayBufferToString(buffer) {
  // 微信小程序中 onChunkReceived 的 data 是 ArrayBuffer
  if (typeof buffer === 'string') return buffer;
  if (buffer instanceof ArrayBuffer) {
    const uint8 = new Uint8Array(buffer);
    let str = '';
    for (let i = 0; i < uint8.length; i++) {
      str += String.fromCharCode(uint8[i]);
    }
    return decodeURIComponent(escape(str));
  }
  return String(buffer);
}

// ==================== Dify 对话型应用 API ====================

/**
 * Dify 对话型应用 API 封装
 *
 * 鉴权: Authorization: Bearer {apiKey}
 * 用户标识: user 参数（来自业务系统的用户 ID）
 * Nginx 路由: /ai/* → Dify 服务（端口 21326）
 *
 * SSE 流式事件:
 *   message       — LLM 文本块 (answer, message_id, conversation_id, task_id)
 *   agent_message — Agent 模式文本块
 *   agent_thought — Agent 思考步骤 (thought, observation, tool, tool_input)
 *   message_file  — 文件事件 (id, type, url)
 *   message_end   — 流结束标记
 *   error         — 错误事件
 *   ping          — 心跳 (每 10s)
 */
const DifyAPI = {
  /** Dify API Key（从 Dify 后台「访问 API」页面获取） */
  API_KEY: '',

  /** API 基础路径（含 Nginx /ai/ 前缀） */
  BASE_URL: '',

  /**
   * 初始化配置
   * @param {string} apiKey  - Dify API Key
   * @param {string} baseUrl - 基础 URL（如 http://10.43.128.231:61000/ai/v1）
   */
  init(apiKey, baseUrl) {
    this.API_KEY = apiKey;
    this.BASE_URL = baseUrl;
  },

  // ==================== 文件上传 ====================

  /**
   * 上传文件（图片等）到 Dify
   *
   * 【关键踩坑】wx.uploadFile 在新版微信 SDK 中可能已自动解析 JSON，
   * res.data 可能是 object 而非 string，必须同时处理两种类型。
   *
   * 【关键踩坑】Nginx 默认 client_max_body_size=1MB，图片必然超限返回 413。
   * 需在 nginx.conf 中设置 client_max_body_size 500m;
   *
   * @param {string} filePath - 微信临时文件路径 (wx.chooseMedia 返回的 tempFilePath)
   * @param {string} userId   - 终端用户标识
   * @returns {Promise<{id, name, size, extension, mime_type}>}
   */
  uploadFile(filePath, userId) {
    return new Promise((resolve, reject) => {
      wx.uploadFile({
        url: `${this.BASE_URL}/files/upload`,
        filePath,
        name: 'file',
        formData: { user: userId },
        header: { 'Authorization': `Bearer ${this.API_KEY}` },
        success(res) {
          let data;
          if (typeof res.data === 'string') {
            try { data = JSON.parse(res.data); } catch (e) {
              reject(new Error(`服务器返回非 JSON (status=${res.statusCode})，请检查 Nginx/Dify 是否正常`));
              return;
            }
          } else if (typeof res.data === 'object' && res.data !== null) {
            data = res.data;  // SDK 已自动解析
          } else {
            reject(new Error(`服务器返回异常数据 (status=${res.statusCode})`));
            return;
          }
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(data);
          } else {
            reject(new Error(data.message || data.code || `上传失败(${res.statusCode})`));
          }
        },
        fail(err) { reject(new Error(err.errMsg || '网络异常')); }
      });
    });
  },

  // ==================== 发送对话消息（SSE 流式） ====================

  /**
   * 发送对话消息（SSE 流式）
   * @param {Object} opts
   * @param {string} opts.query          - 用户输入
   * @param {string} opts.userId         - 用户标识
   * @param {string} [opts.conversationId] - 会话 ID
   * @param {Array}  [opts.files]        - [{type, transfer_method, upload_file_id}]
   * @param {Function} opts.onToken      - (token: string)
   * @param {Function} opts.onMessageId  - (messageId: string) Dify 真实 message_id
   * @param {Function} opts.onThought    - ({thought, observation, tool, tool_input})
   * @param {Function} opts.onConvId     - (conversationId: string)
   * @param {Function} opts.onTaskId     - (taskId: string)
   * @param {Function} opts.onFile       - ({id, type, url})
   * @param {Function} opts.onDone       - (conversationId: string)
   * @param {Function} opts.onError      - (error: Error)
   * @returns {wx.RequestTask} 可调用 .abort() 停止
   */
  sendChatMessage(opts) {
    const {
      query, userId, conversationId, files,
      onToken, onMessageId, onThought, onConvId, onTaskId, onFile,
      onDone, onError,
    } = opts;

    let convId = conversationId || '';
    let taskId = '';

    const requestTask = wx.request({
      url: `${this.BASE_URL}/chat-messages`,
      method: 'POST',
      enableChunked: true,
      header: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.API_KEY}`
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
        if (res.statusCode !== 200 && onError) {
          try { const e = JSON.parse(res.data); onError(new Error(e.message || e.code)); }
          catch (_) { onError(new Error(`请求失败(${res.statusCode})`)); }
        }
      },
      fail(err) { if (onError) onError(new Error(err.errMsg || '网络异常')); }
    });

    let buffer = '';
    requestTask.onChunkReceived(res => {
      try {
        const chunk = this._buf2str(res.data);
        buffer += chunk;
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith('data: ')) continue;
          let json;
          try { json = JSON.parse(trimmed.slice(6)); } catch (_) { continue; }

          switch (json.event) {
            case 'message':
            case 'agent_message':
              if (json.answer && onToken) onToken(json.answer);
              if (json.message_id && onMessageId) onMessageId(json.message_id);
              if (json.conversation_id && !convId) { convId = json.conversation_id; if (onConvId) onConvId(convId); }
              if (json.task_id && !taskId) { taskId = json.task_id; if (onTaskId) onTaskId(taskId); }
              break;
            case 'agent_thought':
              if (onThought) onThought({
                thought: json.thought || '',
                observation: json.observation || '',
                tool: json.tool || '',
                tool_input: json.tool_input || '',
              });
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
            case 'ping': break;
          }
        }
      } catch (_) { /* 解析异常忽略，buffer 残留数据下个 chunk 重试 */ }
    });

    return requestTask;
  },

  /** ArrayBuffer → UTF-8 字符串 */
  _buf2str(buffer) {
    if (typeof buffer === 'string') return buffer;
    if (buffer instanceof ArrayBuffer) {
      const bytes = new Uint8Array(buffer);
      let str = '';
      for (let i = 0; i < bytes.length; i++) str += '%' + ('00' + bytes[i].toString(16)).slice(-2);
      try { return decodeURIComponent(str); } catch (_) { return str; }
    }
    return String(buffer || '');
  },

  // ==================== 反馈 ====================

  /**
   * 发送消息反馈（点赞/点踩）
   * 【关键踩坑】必须使用 Dify 真实 message_id（UUID），不能用本地生成的 msg_xxx ID
   * @param {string} messageId - Dify 真实 message_id
   * @param {string} rating    - "like" | "dislike" | null
   * @param {string} userId    - 用户标识
   */
  sendFeedback(messageId, rating, userId) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${this.BASE_URL}/messages/${messageId}/feedbacks`,
        method: 'POST',
        header: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.API_KEY}`
        },
        data: { rating, user: userId, content: '' },
        success(res) {
          if (res.statusCode === 200) resolve(res.data);
          else reject(new Error('反馈失败'));
        },
        fail(err) { reject(err); }
      });
    });
  },

  // ==================== 会话管理 ====================

  /** 获取会话列表 */
  getConversations(userId, lastId, limit = 20) {
    return new Promise((resolve, reject) => {
      let url = `${this.BASE_URL}/conversations?user=${encodeURIComponent(userId)}&limit=${limit}`;
      if (lastId) url += `&last_id=${lastId}`;
      wx.request({
        url, method: 'GET',
        header: { 'Authorization': `Bearer ${this.API_KEY}` },
        success(res) { res.statusCode === 200 ? resolve(res.data) : reject(new Error('获取失败')); },
        fail(err) { reject(err); }
      });
    });
  },

  /** 获取会话历史消息 */
  getMessages(conversationId, userId, firstId, limit = 20) {
    return new Promise((resolve, reject) => {
      let url = `${this.BASE_URL}/messages?user=${encodeURIComponent(userId)}&conversation_id=${conversationId}&limit=${limit}`;
      if (firstId) url += `&first_id=${firstId}`;
      wx.request({
        url, method: 'GET',
        header: { 'Authorization': `Bearer ${this.API_KEY}` },
        success(res) { res.statusCode === 200 ? resolve(res.data) : reject(new Error('获取失败')); },
        fail(err) { reject(err); }
      });
    });
  },

  /** 删除会话 */
  deleteConversation(conversationId, userId) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${this.BASE_URL}/conversations/${conversationId}`,
        method: 'DELETE',
        header: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.API_KEY}`
        },
        data: { user: userId },
        success(res) { (res.statusCode === 204 || res.statusCode === 200) ? resolve() : reject(new Error('删除失败')); },
        fail(err) { reject(err); }
      });
    });
  },

  /** 获取应用参数（开场白、推荐问题等） */
  getAppParameters() {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${this.BASE_URL}/parameters`,
        method: 'GET',
        header: { 'Authorization': `Bearer ${this.API_KEY}` },
        success(res) { res.statusCode === 200 ? resolve(res.data) : reject(new Error('获取失败')); },
        fail(err) { reject(err); }
      });
    });
  },
};

// ==================== 导出 ====================

module.exports = {
  MockAPI,
  streamChat,
  DifyAPI,
  setApiKey,
  getApiKey,
  DEFAULT_API_ENDPOINT,
};
