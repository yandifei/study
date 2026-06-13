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
      color: 'rgba(255,255,255,0.65)',
      selectedColor: '#ffffff',
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
              role: 'assistant',
              content: item.answer,
              status: 'sent',
              timestamp: item.created_at * 1000,
              errorMsg: '',
              feedback: item.feedback || null,
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
    let hasError = false;

    results.forEach((result, index) => {
      if (result.status === 'fulfilled') {
        fileRefs.push({
          type: 'image',
          transfer_method: 'local_file',
          upload_file_id: result.value.id,
          _path: files[index].path,   // 辅助字段，仅本地用
        });
      } else {
        hasError = true;
      }
    });

    if (fileRefs.length === 0) {
      wx.showToast({ title: '图片上传失败，请重试', icon: 'none' });
      return;
    }

    if (hasError) {
      wx.showToast({ title: '部分图片上传失败，已跳过', icon: 'none' });
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

    // 提取纯上传参数（去掉 _path）
    const pureFiles = fileRefs.filter(f => f.upload_file_id).map(f => ({
      type: f.type,
      transfer_method: f.transfer_method,
      upload_file_id: f.upload_file_id,
    }));

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
      onToken: (token) => {
        const cur = this.data.messages[aiIndex];
        if (!cur) return;
        this.setData({
          [`messages[${aiIndex}].content`]: cur.content + token,
          [`messages[${aiIndex}].status`]: 'streaming',
        });
      },
      onFile: (fileInfo) => {
        // 可选：支持 Dify 返回图片
        if (fileInfo.type === 'image' && fileInfo.url) {
          const cur = this.data.messages[aiIndex];
          if (!cur) return;
          this.setData({
            [`messages[${aiIndex}].content`]: cur.content + `\n![图片](${fileInfo.url})\n`,
          });
        }
      },
      onDone: (convId) => {
        this.setData({
          [`messages[${aiIndex}].status`]: 'sent',
          isGenerating: false,
          streamingMsgIndex: -1,
          currentTaskId: '',
        });
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

    DifyAPI.sendFeedback(id, rating, this.data.userId)
      .then(() => {
        wx.showToast({ title: type === 'like' ? '感谢反馈 👍' : '已记录', icon: 'none' });
        const idx = this.data.messages.findIndex(m => m.id === id);
        if (idx !== -1) {
          this.setData({ [`messages[${idx}].feedback`]: rating });
        }
      })
      .catch(() => {
        wx.showToast({ title: '反馈失败', icon: 'none' });
      });
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
      role,
      content,
      status: status || 'sent',
      timestamp: Date.now(),
      errorMsg: '',
      files: files || [],
      feedback: null,
    };
  },
});