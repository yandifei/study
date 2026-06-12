/**
 * pages/chat/chat.js — AI 聊天页面
 *
 * 这是使用 chat-interface 组件的示例页面。
 * 开发者可根据实际需求修改以下配置参数。
 */

// 如果使用真实 API，取消下面的注释并填入 API Key
// const { setApiKey } = require('../../utils/chat-api');
// setApiKey('your-api-key-here');

Page({
  data: {
    // ===== 基础配置 =====
    /** 初始欢迎语（支持 Markdown） */
    welcomeMsg: '你好！我是 AI 助手，有什么可以帮你的？',

    /** 输入框占位提示文字 */
    placeholder: '输入消息...',

    /** 顶部标题栏文字 */
    title: 'AI 助手',

    // ===== 头像配置 =====
    /** 用户头像 URL（空则显示默认"我"字头像） */
    userAvatar: '',

    /** AI 头像 URL（空则显示默认"AI"字头像） */
    aiAvatar: '',

    // ===== 推荐问题（欢迎页展示） =====
    suggestions: [
      '介绍一下你自己',
      '帮我写一段代码',
      '今天有什么新闻',
    ],

    // ===== 功能开关 =====
    showCopyBtn: true,
    showClearBtn: true,
    showFeedbackBtn: true,
    enableDarkMode: true,
    enableVoice: false,
    enableFileUpload: false,
    enableWebSearch: false,

    // ===== API 配置 =====
    /** API 模式："mock"（本地模拟）或 "real"（真实后端） */
    apiMode: 'mock',

    /** 真实 API 地址（apiMode 为 "real" 时必填） */
    apiEndpoint: 'https://api.deepseek.com/v1/chat/completions',
  },

  /**
   * 消息列表变更回调
   */
  onMessagesChange(e) {
    console.log('消息列表更新:', e.detail.messages);
  },

  /**
   * 用户发送消息回调（apiMode 为 "real" 时触发）
   */
  onSend(e) {
    console.log('用户发送消息:', e.detail.content);
  },

  onLoad() {
    // 页面加载
  },

  onShow() {
    // 页面显示
  },

  onHide() {
    // 页面隐藏
  },

  onUnload() {
    // 页面卸载
  },

  onShareAppMessage() {
    return {
      title: 'AI 助手 - 智能对话',
      path: '/pages/chat/chat',
    };
  },
});
