/**
 * pages/search/search.js — AI 图片鉴赏助手（完整融合版）
 *
 * 包含：
 * - 用户 & 会话管理
 * - 图片上传 + AI 多模态流式对话
 * - 输入框行数自动增长（最多 4 行）
 * - 完整的功能开关与错误处理
 */

const request = require('../../utils/request.js');
const { API } = require('../../config/api.js');
const DifyAPI = require('../../utils/dify-api.js');

Page({
  data: {
    // ===== 用户 =====
    userId: '',

    // ===== 消息 =====
    messages: [],              // 消息列表
    inputValue: '',            // 输入框内容
    isGenerating: false,       // 是否正在生成
    currentTaskId: '',         // 当前流式任务 ID
    streamingMsgIndex: -1,     // 当前流式输出消息索引

    // ===== 会话 =====
    conversationId: '',        // 当前会话 ID
    conversations: [],         // 历史会话列表
    showSidebar: false,        // 侧边栏展开

    // ===== 图片 =====
    uploadedFiles: [],         // 已选待发送图片

    // ===== 滚动 =====
    scrollToView: '',
    showScrollToBottom: false,
    manualScroll: false,

    // ===== 欢迎页 =====
    welcomeMsg: '你好！我是 AI 鉴赏助手 🎨\n上传一张图片，让我帮你鉴赏分析～',
    suggestions: [
      '这幅画的艺术风格是什么？',
      '帮我分析这张图片的构图',
      '推荐一些类似风格的作品',
    ],

    // ===== 弹窗 =====
    showClearConfirm: false,

    // ===== 自定义导航栏 =====
    statusBarHeight: 0,
    navBarHeight: 0,
    totalNavHeight: 0,

    // ===== 输入框动态高度（rpx） =====
    textareaHeight: '72rpx',   // 初始单行高度，不再为空

    // ===== 功能开关（确保左侧按钮等显隐正常） =====
    showCopyBtn: true,
    showFeedbackBtn: true,
    enableFileUpload: true,
  },

  // ==================== 生命周期 ====================

  onLoad() {
    this.initNavBar();
  },

  onShow() {
    wx.setTabBarStyle({
      color: '#abbcff',
      selectedColor: '#00e1ff',
      backgroundColor: '#4B70FD',
    });
    this.loadUserInfo();
  },

  onUnload() {
    if (this._requestTask) {
      try { this._requestTask.abort(); } catch (e) {}
    }
  },

  // ==================== 自定义导航栏 ====================

  initNavBar() {
    const systemInfo = wx.getSystemInfoSync();
    const menuButton = wx.getMenuButtonBoundingClientRect();
    const statusBarHeight = systemInfo.statusBarHeight;
    const gap = menuButton.top - statusBarHeight;
    const navBarHeight = gap * 2 + menuButton.height;
    const totalNavHeight = statusBarHeight + navBarHeight;

    this.setData({
      statusBarHeight,
      navBarHeight,
      totalNavHeight,
    });
  },

  // ==================== 用户信息 ====================

  loadUserInfo() {
    request({ url: API.USER_INFO, method: 'GET' })
      .then(res => {
        if (res.statusCode === 200) {
          const userId = res.data.id || res.data.email || 'anonymous';
          if (userId !== this.data.userId) {
            this.setData({ userId });
            this.loadConversations();
            this.loadAppParams();
          }
        }
      })
      .catch(() => {
        wx.showToast({ title: '加载用户信息失败', icon: 'none' });
      });
  },

  // ==================== 应用参数 ====================

  loadAppParams() {
    DifyAPI.getAppParameters()
      .then(data => {
        const updates = {};
        if (data.opening_statement) {
          updates.welcomeMsg = data.opening_statement;
        }
        if (data.suggested_questions && data.suggested_questions.length > 0) {
          updates.suggestions = data.suggested_questions;
        }
        if (Object.keys(updates).length > 0) {
          this.setData(updates);
        }
      })
      .catch(() => {});
  },

  // ==================== 会话管理 ====================

  loadConversations() {
    if (!this.data.userId) return;
    DifyAPI.getConversations(this.data.userId)
      .then(data => {
        this.setData({ conversations: data.data || [] });
      })
      .catch(() => {});
  },

  handleToggleSidebar() {
    this.setData({ showSidebar: !this.data.showSidebar });
    if (!this.data.showSidebar) return;
    this.loadConversations();
  },

  handleSelectConversation(e) {
    const { id, name } = e.currentTarget.dataset;
    if (id === this.data.conversationId) {
      this.setData({ showSidebar: false });
      return;
    }

    this.setData({
      conversationId: id,
      messages: [],
      showSidebar: false,
      isGenerating: false,
    });

    this.loadMessages(id);
  },

  loadMessages(conversationId) {
    if (!conversationId || !this.data.userId) return;

    DifyAPI.getMessages(conversationId, this.data.userId)
      .then(data => {
        const list = (data.data || []).reverse();
        const messages = [];

        list.forEach(item => {
          messages.push({
            id: item.id + '_user',
            role: 'user',
            content: item.query,
            status: 'sent',
            timestamp: item.created_at * 1000,
            errorMsg: '',
            files: [],
            feedback: null,
          });

          if (item.answer) {
            messages.push({
              id: item.id,
              difyMessageId: item.id,
              role: 'assistant',
              content: item.answer,
              status: 'sent',
              timestamp: item.created_at * 1000,
              errorMsg: '',
              feedback: item.feedback || null,
              thought: '',                // 历史消息暂时不解析 think，如需可后续增强
              showThought: false,
            });
          }
        });

        this.setData({ messages });
        this._scrollToBottom();
      })
      .catch(() => {
        wx.showToast({ title: '加载历史消息失败', icon: 'none' });
      });
  },

  handleNewChat() {
    this.setData({
      conversationId: '',
      messages: [],
      inputValue: '',
      isGenerating: false,
      uploadedFiles: [],
      showSidebar: false,
      textareaHeight: '72rpx',
    });
  },

  handleDeleteConversation(e) {
    const { id } = e.currentTarget.dataset;
    wx.showModal({
      title: '删除会话',
      content: '确定要删除这个会话吗？',
      confirmColor: '#e84f50',
      success: res => {
        if (!res.confirm) return;
        DifyAPI.deleteConversation(id, this.data.userId)
          .then(() => {
            if (id === this.data.conversationId) {
              this.handleNewChat();
            }
            this.loadConversations();
          })
          .catch(() => {
            wx.showToast({ title: '删除失败', icon: 'none' });
          });
      }
    });
  },

  // ==================== 图片上传 ====================

  handleChooseImage() {
    if (this.data.isGenerating) {
      wx.showToast({ title: '正在生成回复中', icon: 'none' });
      return;
    }

    const remain = 3 - this.data.uploadedFiles.length;
    if (remain <= 0) return;

    wx.chooseMedia({
      count: remain,
      mediaType: ['image'],
      sourceType: ['album', 'camera'],
      success: res => {
        const newFiles = res.tempFiles.map(f => ({
          id: `file_${Date.now()}_${Math.random().toString(36).slice(2, 6)}`,
          path: f.tempFilePath,
          name: `image_${Date.now()}.${f.tempFilePath.split('.').pop() || 'jpg'}`,
          size: f.size,
        }));

        this.setData({
          uploadedFiles: [...this.data.uploadedFiles, ...newFiles].slice(0, 3),
        });
      }
    });
  },

  handleRemoveFile(e) {
    const { id } = e.currentTarget.dataset;
    this.setData({
      uploadedFiles: this.data.uploadedFiles.filter(f => f.id !== id),
    });
  },

  handlePreviewFile(e) {
    const { path } = e.currentTarget.dataset;
    wx.previewImage({
      urls: [path],
      current: path,
    });
  },

  // ==================== 消息发送 ====================

  handleSend() {
    const content = this.data.inputValue.trim();
    const hasFiles = this.data.uploadedFiles.length > 0;

    if (!content && !hasFiles) return;
    if (this.data.isGenerating) return;

    // 确保用户信息已加载
    if (!this.data.userId) {
      wx.showToast({ title: '正在加载用户信息，请稍后再试', icon: 'none' });
      return;
    }

    const query = content || '请帮我鉴赏这张图片';
    const files = [...this.data.uploadedFiles];

    // 清空输入
    this.setData({
      inputValue: '',
      uploadedFiles: [],
      textareaHeight: '72rpx',   // 改为明确的单行高度
    });

    if (hasFiles) {
      this._uploadFilesThenSend(query, files);
    } else {
      this._sendMessage(query, []);
    }
  },

  async _uploadFilesThenSend(content, files) {
    wx.showLoading({ title: '上传图片中...' });

    // 使用 allSettled 保证部分成功也能发送
    const results = await Promise.allSettled(
      files.map(f => DifyAPI.uploadFile(f.path, this.data.userId))
    );

    wx.hideLoading();

    const fileRefs = [];
    const errors = [];

    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        fileRefs.push({
          id: result.value.id,              // WXML wx:key 使用
          type: 'image',
          transfer_method: 'local_file',
          upload_file_id: result.value.id,
          path: files[index].path,          // 与 WXML 中 f.path 一致
          url: '',                          // 远程 URL（如有）
        });
      } else {
        const errMsg = result.reason?.message || '未知错误';
        errors.push(errMsg);
      }
    });

    if (fileRefs.length === 0) {
      const detail = errors.length > 0 ? errors[0] : '未知错误';
      wx.showToast({ title: `上传失败: ${detail}`, icon: 'none', duration: 3000 });
      console.error('[upload] 所有文件上传失败:', errors);
      return;
    }

    if (errors.length > 0) {
      wx.showToast({ title: `部分图片上传失败: ${errors[0]}`, icon: 'none', duration: 2500 });
      console.warn('[upload] 部分上传失败:', errors);
    }

    this._sendMessage(content, fileRefs);
  },

  _sendMessage(query, fileRefs) {
    const userMsg = this._createMessage('user', query, 'sent', fileRefs);
    const aiMsg = this._createMessage('assistant', '', 'sending');

    const messages = [...this.data.messages, userMsg, aiMsg];
    const aiIndex = messages.length - 1;

    this.setData({
      messages,
      isGenerating: true,
      streamingMsgIndex: aiIndex,
      currentTaskId: '',
    });
    this._scrollToBottom();

    // 提取纯上传参数（去掉 _path 等本地字段）
    const pureFiles = fileRefs.filter(f => f.upload_file_id).map(f => ({
      type: f.type,
      transfer_method: f.transfer_method,
      upload_file_id: f.upload_file_id,
    }));

    // —— <think> 标签流式剥离状态机 ——
    var THINK_OPEN = '<think>';
    var THINK_CLOSE = '</' + 'think>';   // 拼接避免写入时被转义
    var inThink = false;
    var tagBuf = '';
    var thoughtAcc = '';

    this._requestTask = DifyAPI.sendChatMessage({
      query,
      userId: this.data.userId,
      conversationId: this.data.conversationId,
      files: pureFiles,
      onConvId: (convId) => {
        if (convId && !this.data.conversationId) {
          this.setData({ conversationId: convId });
          this.loadConversations();
        }
      },
      onTaskId: (taskId) => {
        this.setData({ currentTaskId: taskId });
      },
      onMessageId: (messageId) => {
        if (messageId) {
          this.setData({ [`messages[${aiIndex}].difyMessageId`]: messageId });
        }
      },
      onThought: (thoughtData) => {
        // SSE agent_thought 事件（Agent 模式）
        const cur = this.data.messages[aiIndex];
        if (!cur) return;
        let add = '';
        if (thoughtData.thought) add += thoughtData.thought + '\n';
        if (thoughtData.observation) add += '🔍 ' + thoughtData.observation + '\n';
        this.setData({
          [`messages[${aiIndex}].thought`]: (cur.thought || '') + add,
          [`messages[${aiIndex}].showThought`]: false,
        });
      },
      onToken: (token) => {
        const cur = this.data.messages[aiIndex];
        if (!cur) return;

        // —— 流式剥离 <think>...</think> 标签 ——
        const combined = tagBuf + token;
        tagBuf = '';
        let display = '';
        let i = 0;

        while (i < combined.length) {
          if (!inThink) {
            // 检查 <think> 开始标签
            if (combined.substring(i, i + 7) === THINK_OPEN) {
              inThink = true;
              i += 7;
            } else {
              display += combined[i];
              i++;
            }
          } else {
            // 检查 </think> 结束标签
            if (combined.substring(i, i + 8) === THINK_CLOSE) {
              inThink = false;
              i += 8;
            } else {
              thoughtAcc += combined[i];
              i++;
            }
          }
        }

        // 防止 <think> / </think> 跨 chunk 被截断
        if (inThink) {
          // 在 think 内：保留末尾可能形成 </think 的片段
          const tail = combined.slice(-7);
          const endMatch = tail.match(/(<\/t?h?i?n?k?)$/);
          if (endMatch && endMatch[1].length > 0 && THINK_CLOSE.startsWith(endMatch[1])) {
            thoughtAcc = thoughtAcc.slice(0, -endMatch[1].length);
            tagBuf = endMatch[1];
          }
        } else {
          // 在 think 外：保留末尾可能形成 <think> 的片段
          const tail = combined.slice(-6);
          const startMatch = tail.match(/(<t?h?i?n?k?>?)$/);
          if (startMatch && THINK_OPEN.startsWith(startMatch[1]) && startMatch[1].length < 7) {
            display = display.slice(0, -(startMatch[1].length));
            tagBuf = startMatch[1];
          }
        }

        // 更新显示的文本内容
        if (display) {
          this.setData({
            [`messages[${aiIndex}].content`]: cur.content + display,
            [`messages[${aiIndex}].status`]: 'streaming',
          });
        }

        // 实时更新思考内容（但默认折叠）
        if (thoughtAcc && !cur.thought) {
          // 首个 thought chunk 到来时初始化
          this.setData({
            [`messages[${aiIndex}].thought`]: thoughtAcc,
            [`messages[${aiIndex}].showThought`]: false,
          });
        } else if (thoughtAcc) {
          this.setData({
            [`messages[${aiIndex}].thought`]: thoughtAcc,
          });
        }
      },
      onFile: (fileInfo) => {
        if (fileInfo.type === 'image' && fileInfo.url) {
          const cur = this.data.messages[aiIndex];
          if (!cur) return;
          this.setData({
            [`messages[${aiIndex}].content`]: cur.content + `\n![图片](${fileInfo.url})\n`,
          });
        }
      },
      onDone: (convId) => {
        // 流结束：最终处理一次，确保所有思考和内容正确落盘
        const cur = this.data.messages[aiIndex];
        const updates = {
          [`messages[${aiIndex}].status`]: 'sent',
          [`messages[${aiIndex}].showThought`]: false,
          isGenerating: false,
          streamingMsgIndex: -1,
          currentTaskId: '',
        };

        // 最终清洗：用正则确保所有 <think> 块都被处理
        if (cur && cur.content) {
          const finalThought = (cur.thought || '') + (inThink ? thoughtAcc : '');
          let finalContent = cur.content;
          var thinkRegex = new RegExp(THINK_OPEN + '[\\s\\S]*?' + THINK_CLOSE, 'g');
          finalContent = finalContent.replace(thinkRegex, '');
          updates[`messages[${aiIndex}].content`] = finalContent.trim();
          updates[`messages[${aiIndex}].thought`] = finalThought.trim();
        }

        this.setData(updates);
        if (convId && !this.data.conversationId) {
          this.setData({ conversationId: convId });
          this.loadConversations();
        }
      },
      onError: (err) => {
        const curMsg = this.data.messages[aiIndex];
        this.setData({
          [`messages[${aiIndex}].status`]: curMsg && curMsg.content ? 'sent' : 'failed',
          [`messages[${aiIndex}].errorMsg`]: err.message || '请求失败',
          isGenerating: false,
          streamingMsgIndex: -1,
          currentTaskId: '',
        });
        if (!curMsg || !curMsg.content) {
          wx.showToast({ title: err.message || '请求失败，请重试', icon: 'none' });
        }
      },
    });
  },

  handleSendSuggestion(e) {
    const text = e.currentTarget.dataset.text;
    if (!text) return;
    this.setData({ inputValue: text }, () => this.handleSend());
  },

  // ==================== 停止生成 ====================

  handleStop() {
    if (this.data.currentTaskId && this.data.userId) {
      DifyAPI.stopResponse(this.data.currentTaskId, this.data.userId).catch(() => {});
    }

    if (this._requestTask) {
      try { this._requestTask.abort(); } catch (e) {}
      this._requestTask = null;
    }

    const idx = this.data.streamingMsgIndex;
    if (idx >= 0 && this.data.messages[idx]) {
      const hasContent = !!this.data.messages[idx].content;
      if (hasContent) {
        this.setData({
          [`messages[${idx}].status`]: 'sent',
        });
      } else {
        const msgs = [...this.data.messages];
        msgs.splice(idx, 1);
        this.setData({ messages: msgs });
      }
    }

    this.setData({
      isGenerating: false,
      streamingMsgIndex: -1,
      currentTaskId: '',
    });
  },

  // ==================== 重试 ====================

  handleRetry(e) {
    const id = e.currentTarget.dataset.id;
    const messages = [...this.data.messages];
    const idx = messages.findIndex(m => m.id === id);
    if (idx === -1) return;

    const userMsg = messages.slice(0, idx).reverse().find(m => m.role === 'user');
    if (!userMsg) return;

    messages.splice(idx, 1);
    this.setData({ messages });
    this._sendMessage(userMsg.content, userMsg.files || []);
  },

  // ==================== 消息操作 ====================

  handleCopyContent(e) {
    const content = e.currentTarget.dataset.content;
    wx.setClipboardData({
      data: content,
      success: () => wx.showToast({ title: '已复制', icon: 'success' }),
    });
  },

  handleFeedback(e) {
    const { id, type } = e.currentTarget.dataset;
    const rating = type === 'like' ? 'like' : 'dislike';

    // 使用 Dify 真实 message_id（不存在时回退到本地 id，兼容历史消息）
    const idx = this.data.messages.findIndex(m => m.id === id);
    const realMessageId = (idx !== -1 && this.data.messages[idx].difyMessageId) || id;

    DifyAPI.sendFeedback(realMessageId, rating, this.data.userId)
      .then(() => {
        wx.showToast({ title: type === 'like' ? '感谢反馈 👍' : '已记录', icon: 'none' });
        if (idx !== -1) {
          this.setData({ [`messages[${idx}].feedback`]: rating });
        }
      })
      .catch((err) => {
        console.error('[feedback] 反馈失败:', err);
        wx.showToast({ title: '反馈失败，请重试', icon: 'none' });
      });
  },

  /** 折叠/展开思考过程 */
  handleToggleThought(e) {
    const { id } = e.currentTarget.dataset;
    const idx = this.data.messages.findIndex(m => m.id === id);
    if (idx !== -1) {
      this.setData({
        [`messages[${idx}].showThought`]: !this.data.messages[idx].showThought,
      });
    }
  },

  /** 重新生成：找到上一条用户消息重新发送 */
  handleRegenerate(e) {
    if (this.data.isGenerating) return;
    const { id } = e.currentTarget.dataset;
    const msgs = [...this.data.messages];
    const idx = msgs.findIndex(m => m.id === id);
    if (idx === -1) return;
    const uMsg = msgs.slice(0, idx).reverse().find(m => m.role === 'user');
    if (!uMsg) return;
    msgs.splice(idx, 1);
    this.setData({ messages: msgs });
    this._sendMessage(uMsg.content, uMsg.files || []);
  },

  // ==================== 清空对话 ====================

  handleClearChat() {
    this.setData({ showClearConfirm: true });
  },

  handleCancelClear() {
    this.setData({ showClearConfirm: false });
  },

  handleConfirmClear() {
    this.setData({
      messages: [],
      conversationId: '',
      showClearConfirm: false,
      isGenerating: false,
      uploadedFiles: [],
      currentTaskId: '',
      streamingMsgIndex: -1,
      textareaHeight: '72rpx',   // 回到单行
    });
    if (this._requestTask) {
      try { this._requestTask.abort(); } catch (e) {}
      this._requestTask = null;
    }
  },

  // ==================== 滚动控制 ====================

  _scrollToBottom() {
    this.setData({ scrollToView: 'scroll-bottom' });
  },

  scrollToBottom() {
    this.setData({
      manualScroll: false,
      showScrollToBottom: false,
      scrollToView: 'scroll-bottom',
    });
  },

  onScrollToLower() {
    this.setData({ manualScroll: false, showScrollToBottom: false });
  },

  onScroll(e) {
    // 可根据实际滚动位置控制“滚到底部”按钮
    // 此处保留接口，可在 wxml 中绑定 bindscroll
  },

  onInputFocus() {
    this._scrollToBottom();
  },

  onInputChange(e) {
    this.setData({ inputValue: e.detail.value });
  },

  /**
   * 输入框行数变化 —— 最多增长到 4 行，之后内部滚动
   * 适配旧版与新版的 textarea 动态高度
   */
  onLineChange(e) {
    const lineCount = e.detail.lineCount || 1;
    const maxLines = 4;
    const rowHeight = 45;    // 30rpx * 1.5
    const pad = 28;          // 上下 padding
    let height;
    if (lineCount <= maxLines) {
      height = rowHeight * lineCount + pad;
    } else {
      height = rowHeight * maxLines + pad;  // 封顶 208rpx
    }
    this.setData({ textareaHeight: height + 'rpx' });
  },

  // ==================== 工具方法 ====================

  _createMessage(role, content, status, files) {
    return {
      id: `msg_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      difyMessageId: '',          // 由 SSE 流回调更新，用于反馈接口
      role,
      content,
      status: status || 'sent',
      timestamp: Date.now(),
      errorMsg: '',
      files: files || [],
      feedback: null,
      thought: '',                // 思考过程（由 <think> 标签或 agent_thought 事件填充）
      showThought: false,         // 默认折叠思考过程
    };
  },
});
