/**
 * chat-interface 组件 — 微信小程序 AI 聊天界面核心组件
 *
 * Properties:
 *   welcomeMsg    {String}  初始欢迎语
 *   placeholder   {String}  输入框占位文字
 *   userAvatar    {String}  用户头像 URL
 *   aiAvatar      {String}  AI 头像 URL
 *   title         {String}  顶部标题
 *   suggestions   {Array}   推荐问题列表
 *   showCopyBtn   {Boolean} 是否显示复制按钮
 *   showClearBtn  {Boolean} 是否显示清空按钮
 *   showFeedbackBtn {Boolean} 是否显示点赞/点踩
 *   enableDarkMode {Boolean} 是否适配暗黑模式
 *   enableVoice   {Boolean} 是否启用语音输入
 *   enableFileUpload {Boolean} 是否启用文件上传
 *   enableWebSearch {Boolean} 是否启用联网搜索开关
 *   apiMode       {String}  API 对接模式："mock" | "real"
 *   apiEndpoint   {String}  API 地址（apiMode=real 时必填）
 *
 * Events:
 *   messageschange  {detail: {messages}}  消息列表变更
 *   send            {detail: {content}}    用户发送消息（apiMode=real 时）
 */

const { MockAPI, streamChat } = require('../../utils/chat-api');

Component({
  properties: {
    welcomeMsg:    { type: String,  value: '你好！我是 AI 助手，有什么可以帮你的？' },
    placeholder:   { type: String,  value: '输入消息...' },
    userAvatar:    { type: String,  value: '' },
    aiAvatar:      { type: String,  value: '' },
    title:         { type: String,  value: 'AI 助手' },
    suggestions:   { type: Array,   value: ['介绍一下你自己', '帮我写一段代码', '今天有什么新闻'] },
    showCopyBtn:   { type: Boolean, value: true },
    showClearBtn:  { type: Boolean, value: true },
    showFeedbackBtn: { type: Boolean, value: true },
    enableDarkMode:{ type: Boolean, value: true },
    enableVoice:   { type: Boolean, value: false },
    enableFileUpload: { type: Boolean, value: false },
    enableWebSearch:  { type: Boolean, value: false },
    apiMode:       { type: String,  value: 'mock' },
    apiEndpoint:   { type: String,  value: '' },
  },

  data: {
    messages: [],           // 消息列表
    inputValue: '',         // 输入框内容
    isGenerating: false,    // 是否正在生成回复
    scrollTo: '',           // scroll-into-view 目标
    scrollTop: 0,           // scroll-top 值
    showScrollToBottom: false, // 是否显示"回到底部"按钮
    manualScroll: false,    // 是否处于手动滚动状态
    voiceMode: false,       // 是否处于语音输入模式
    voiceActive: false,     // 语音是否激活（长按中）
    voiceStatus: 'recording', // recording | canceling
    showTools: false,       // 是否显示工具栏
    showFileList: false,    // 是否显示文件预览行
    fileList: [],           // 待发送文件列表
    useWebSearch: false,    // 是否使用联网搜索
    showClearConfirm: false, // 是否显示清空确认弹窗
    welcomeLogo: 'AI',      // 欢迎页 logo 文字
    _mockAPI: null,         // MockAPI 实例
    _lastScrollTop: 0,      // 上次滚动位置
    _scrollTimer: null,     // 滚动防抖定时器
  },

  lifetimes: {
    attached() {
      // 初始化 MockAPI（仅 mock 模式）
      if (this.properties.apiMode === 'mock') {
        this.data._mockAPI = new MockAPI();
      }
      // 添加欢迎消息
      this._addWelcomeMessage();
    },
    detached() {
      if (this.data._scrollTimer) {
        clearTimeout(this.data._scrollTimer);
      }
    },
  },

  methods: {
    // ==================== 消息管理 ====================

    /** 添加欢迎消息 */
    _addWelcomeMessage() {
      const welcomeMsg = this.properties.welcomeMsg;
      if (!welcomeMsg) return;
      const msg = this._createMessage('assistant', welcomeMsg, 'sent');
      this.setData({ messages: [msg] });
      this.triggerEvent('messageschange', { messages: this.data.messages });
    },

    /** 创建消息对象 */
    _createMessage(role, content, status) {
      return {
        id: `msg_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
        role,
        content,
        status: status || 'sent',
        timestamp: Date.now(),
        errorMsg: '',
      };
    },

    /** 生成唯一 ID */
    _genId() {
      return `msg_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    },

    // ==================== 发送消息 ====================

    /** 发送文本消息 */
    handleSend() {
      const content = this.data.inputValue.trim();
      if (!content || this.data.isGenerating) return;

      // 添加用户消息
      const userMsg = this._createMessage('user', content, 'sent');
      // 添加 AI 占位消息（sending 状态）
      const aiMsg = this._createMessage('assistant', '', 'sending');

      const messages = [...this.data.messages, userMsg, aiMsg];
      this.setData({
        messages,
        inputValue: '',
        isGenerating: true,
        showTools: false,
      });
      this.triggerEvent('messageschange', { messages });
      this._scrollToBottom();

      // 调用 API
      if (this.properties.apiMode === 'real') {
        this._sendReal(content, aiMsg.id);
      } else {
        this._sendMock(aiMsg.id);
      }
    },

    /** 发送推荐问题 */
    handleSendSuggestion(e) {
      const text = e.currentTarget.dataset.text;
      if (!text) return;
      this.setData({ inputValue: text }, () => {
        this.handleSend();
      });
    },

    /** Mock 模式发送 */
    async _sendMock(aiMsgId) {
      const messages = [...this.data.messages];
      const aiIndex = messages.findIndex(m => m.id === aiMsgId);
      if (aiIndex === -1) return;

      // 切换到 streaming 状态
      this.setData({ [`messages[${aiIndex}].status`]: 'streaming' });

      try {
        const contextMessages = messages
          .filter(m => m.status === 'sent')
          .map(m => ({ role: m.role, content: m.content }));

        await this.data._mockAPI.sendMessage(
          contextMessages,
          (token) => {
            // onToken: 追加 token
            const cur = this.data.messages[aiIndex];
            if (!cur) return;
            this.setData({
              [`messages[${aiIndex}].content`]: cur.content + token,
            });
          },
          (fullText) => {
            // onDone: 标记完成
            this.setData({
              [`messages[${aiIndex}].status`]: 'sent',
              isGenerating: false,
            });
            this.triggerEvent('messageschange', { messages: this.data.messages });
          },
          (err) => {
            // onError: 标记失败
            this.setData({
              [`messages[${aiIndex}].status`]: 'failed',
              [`messages[${aiIndex}].errorMsg`]: err.message || '请求失败',
              isGenerating: false,
            });
            this.triggerEvent('messageschange', { messages: this.data.messages });
          }
        );
      } catch (e) {
        this.setData({
          [`messages[${aiIndex}].status`]: 'failed',
          [`messages[${aiIndex}].errorMsg`]: '网络异常，请稍后重试',
          isGenerating: false,
        });
      }
    },

    /** 真实 API 模式发送 */
    _sendReal(content, aiMsgId) {
      const messages = [...this.data.messages];
      const aiIndex = messages.findIndex(m => m.id === aiMsgId);
      if (aiIndex === -1) return;

      this.setData({ [`messages[${aiIndex}].status`]: 'streaming' });

      const contextMessages = messages
        .filter(m => m.status === 'sent' || m.role === 'user')
        .map(m => ({ role: m.role, content: m.content }));

      streamChat({
        endpoint: this.properties.apiEndpoint,
        messages: contextMessages,
        onToken: (token) => {
          const cur = this.data.messages[aiIndex];
          if (!cur) return;
          this.setData({
            [`messages[${aiIndex}].content`]: cur.content + token,
          });
        },
        onDone: () => {
          this.setData({
            [`messages[${aiIndex}].status`]: 'sent',
            isGenerating: false,
          });
          this.triggerEvent('messageschange', { messages: this.data.messages });
        },
        onError: (err) => {
          this.setData({
            [`messages[${aiIndex}].status`]: 'failed',
            [`messages[${aiIndex}].errorMsg`]: err.message || '请求失败',
            isGenerating: false,
          });
        },
      });
    },

    /** 停止生成 */
    handleStop() {
      this.setData({ isGenerating: false });
      const messages = [...this.data.messages];
      const lastAi = [...messages].reverse().find(m => m.role === 'assistant');
      if (lastAi && lastAi.status === 'streaming') {
        const idx = messages.findIndex(m => m.id === lastAi.id);
        if (lastAi.content) {
          this.setData({ [`messages[${idx}].status`]: 'sent' });
        } else {
          // 没有内容则移除
          messages.splice(idx, 1);
          this.setData({ messages });
        }
      }
      this.triggerEvent('messageschange', { messages: this.data.messages });
    },

    /** 重试发送 */
    handleRetry(e) {
      const id = e.currentTarget.dataset.id;
      const messages = [...this.data.messages];
      const idx = messages.findIndex(m => m.id === id);
      if (idx === -1) return;

      // 找到对应的用户消息
      const userMsg = messages.slice(0, idx).reverse().find(m => m.role === 'user');
      const content = userMsg ? userMsg.content : '';

      // 移除失败的 AI 消息
      messages.splice(idx, 1);
      // 添加新的 AI 占位消息
      const newAiMsg = this._createMessage('assistant', '', 'sending');
      messages.push(newAiMsg);

      this.setData({ messages, isGenerating: true });
      this.triggerEvent('messageschange', { messages });
      this._scrollToBottom();

      if (this.properties.apiMode === 'real') {
        this._sendReal(content, newAiMsg.id);
      } else {
        this._sendMock(newAiMsg.id);
      }
    },

    // ==================== 滚动控制 ====================

    /** 滚动到底部 */
    _scrollToBottom() {
      if (this.data.manualScroll) return;
      this.setData({
        scrollTo: 'scroll-bottom',
      });
    },

    /** 点击回到底部按钮 */
    scrollToBottom() {
      this.setData({
        manualScroll: false,
        showScrollToBottom: false,
        scrollTo: 'scroll-bottom',
      });
    },

    /** 滚动事件 */
    onScroll(e) {
      const { scrollTop } = e.detail;
      this.data._lastScrollTop = scrollTop;

      if (this.data._scrollTimer) {
        clearTimeout(this.data._scrollTimer);
      }
      this.data._scrollTimer = setTimeout(() => {
        this.setData({ scrollTop });
      }, 100);
    },

    /** 开始拖拽 */
    onDragStart(e) {
      if (e.detail.scrollTop > 0 && !this.data.manualScroll) {
        this.setData({ manualScroll: true, showScrollToBottom: true });
      }
    },

    /** 滚动到底部 */
    onScrollToLower() {
      this.setData({ manualScroll: false, showScrollToBottom: false });
    },

    /** 输入框获焦 */
    onInputFocus() {
      this.setData({ manualScroll: false, showScrollToBottom: false });
      this._scrollToBottom();
    },

    // ==================== 输入处理 ====================

    /** 输入变更 */
    onInputChange(e) {
      this.setData({ inputValue: e.detail.value });
    },

    /** 行数变更 */
    onLineChange(e) {
      // textarea 行数变化时，滚动到底部
      this._scrollToBottom();
    },

    /** 切换语音模式 */
    handleToggleVoiceMode() {
      this.setData({ voiceMode: !this.data.voiceMode });
    },

    /** 语音触摸开始 */
    onVoiceTouchStart(e) {
      this.setData({ voiceActive: true, voiceStatus: 'recording' });
      // 开始录音
      const recorder = wx.getRecorderManager();
      recorder.start({
        duration: 60000,
        sampleRate: 44100,
        numberOfChannels: 1,
        encodeBitRate: 192000,
        format: 'aac',
      });
    },

    /** 语音触摸移动 */
    onVoiceTouchMove(e) {
      if (!this.data.voiceActive) return;
      const { clientY } = e.touches[0];
      // 获取起始 Y（通过 data 记录）
      if (!this.data._voiceStartY) {
        this.data._voiceStartY = clientY;
      }
      const deltaY = clientY - this.data._voiceStartY;
      this.setData({
        voiceStatus: deltaY < -50 ? 'canceling' : 'recording',
      });
    },

    /** 语音触摸结束 */
    onVoiceTouchEnd(e) {
      const wasRecording = this.data.voiceStatus === 'recording';
      this.setData({ voiceActive: false, voiceMode: false });
      this.data._voiceStartY = 0;

      const recorder = wx.getRecorderManager();
      recorder.stop();

      if (wasRecording) {
        // 处理语音识别结果
        recorder.onStop((res) => {
          // 可接入语音识别 API 转文字后发送
          console.log('录音结束', res);
        });
      }
    },

    // ==================== 工具操作 ====================

    /** 切换工具栏 */
    handleToggleTools() {
      this.setData({ showTools: !this.data.showTools });
    },

    /** 上传图片 */
    handleUploadImage() {
      const self = this;
      wx.chooseMedia({
        count: 1,
        mediaType: ['image'],
        sourceType: ['album', 'camera'],
        success(res) {
          const file = res.tempFiles[0];
          self.setData({
            fileList: [...self.data.fileList, {
              id: self._genId(),
              name: 'image_' + Date.now(),
              path: file.tempFilePath,
              type: 'image',
              size: file.size,
            }],
            showFileList: true,
            showTools: false,
          });
        },
      });
    },

    /** 上传文件 */
    handleUploadFile() {
      const self = this;
      wx.chooseMessageFile({
        count: 5,
        type: 'file',
        success(res) {
          const files = res.tempFiles.map(f => ({
            id: self._genId(),
            name: f.name,
            path: f.path,
            type: 'file',
            size: f.size,
          }));
          self.setData({
            fileList: [...self.data.fileList, ...files],
            showFileList: true,
            showTools: false,
          });
        },
      });
    },

    /** 移除文件 */
    handleRemoveFile(e) {
      const id = e.currentTarget.dataset.id;
      const fileList = this.data.fileList.filter(f => f.id !== id);
      this.setData({
        fileList,
        showFileList: fileList.length > 0,
      });
    },

    /** 切换联网搜索 */
    handleToggleWebSearch() {
      this.setData({ useWebSearch: !this.data.useWebSearch });
    },

    // ==================== 消息操作 ====================

    /** 复制内容 */
    handleCopyContent(e) {
      const content = e.currentTarget.dataset.content;
      wx.setClipboardData({
        data: content,
        success() {
          wx.showToast({ title: '已复制', icon: 'success' });
        },
      });
    },

    /** 反馈（点赞/点踩） */
    handleFeedback(e) {
      const { id, type } = e.currentTarget.dataset;
      wx.showToast({
        title: type === 'up' ? '感谢反馈' : '已记录',
        icon: 'success',
      });
    },

    // ==================== 清空对话 ====================

    /** 显示清空确认弹窗 */
    handleClearChat() {
      this.setData({ showClearConfirm: true });
    },

    /** 取消清空 */
    handleCancelClear() {
      this.setData({ showClearConfirm: false });
    },

    /** 确认清空 */
    handleConfirmClear() {
      this.setData({
        messages: [],
        showClearConfirm: false,
        isGenerating: false,
        fileList: [],
        showFileList: false,
      });
      this._addWelcomeMessage();
      this.triggerEvent('messageschange', { messages: this.data.messages });
    },
  },
});
