// config/api.js
// 导出代码
// const { API } = require('../../config/api.js');

const accountInfo = wx.getAccountInfoSync();
const envVersion = accountInfo.miniProgram.envVersion; // 'develop', 'trial', 'release'

// 定义不同环境对应的基础URL
const base_urls = {
    // 手机ip：172.20.10.3
    // wifi：10.43.128.231
  develop: 'http://10.43.128.231:61000',   // 开发版（开发者工具、真机预览）必须开启Nginx反代才行
  trial: 'https://scraggly-regress-cape.ngrok-free.dev',    // 体验版（上传后设为体验版）
  release: 'https://scraggly-regress-cape.ngrok-free.dev'    // 正式版（审核上线后）
};

// 自动匹配当前环境的URL
const base_url = base_urls[envVersion];

// 定义所有业务接口路径（方便管理）
const API = {
  // 邮箱登陆
  SEND_CODE: base_url + '/db/auth/send-code',       // 发送邮箱验证码
  USER_LOGIN: base_url + '/db/auth/login',          // 验证码登录/注册
  USER_REFRESH: base_url + '/db/auth/refresh',      // accesss接口刷新
  USER_LOGOUT: base_url + '/db/auth/logout',        // 登出

  // 用户模块
  USER_INFO: base_url + '/db/auth/me',              // 用户信息
  USER_DELETE: base_url + '/db/auth/logout',        // 注销登陆

  // 浏览模块
  BROWSE_LIST: base_url + '/db/browse/',            // 我的浏览记录 (GET)
  BROWSE_BATCH: base_url + '/db/browse/',           // 批量记录浏览 (POST)
  BROWSE_CLEAR: base_url + '//dbbrowse/',           // 清空我的浏览记录 (DELETE)

  // 收藏模块
  FAVORITE_LIST: base_url + '/db/favorite/',        // 我的收藏列表 (GET)
  FAVORITE_ADD: base_url + '/db/favorite/',         // 添加收藏 (POST)
  FAVORITE_CLEAR: base_url + '/db/favorite/',       // 清空我的收藏 (DELETE)
  FAVORITE_REMOVE: base_url + '/db/favorite/',      // 取消收藏 (DELETE + image_id 路径参数)

  // AI模块（Dify 对话型应用 — Nginx /ai/* → Dify 服务 :21326）
  // ⚠️ Dify API Key 请从 Dify 后台「访问 API」页面获取，不要泄露到客户端仓库
  DIFY_API_KEY: 'app-xxxxxxxxxxxxxxxx',

  AI_INFO:        base_url + '/ai/v1/info',
  AI_PARAMETERS:  base_url + '/ai/v1/parameters',
  AI_META:        base_url + '/ai/v1/meta',
  AI_SITE:        base_url + '/ai/v1/site',
  AI_CHAT:        base_url + '/ai/v1/chat-messages',
  AI_FILE_UPLOAD: base_url + '/ai/v1/files/upload',
  AI_CONVERSATIONS: base_url + '/ai/v1/conversations',
  AI_MESSAGES:    base_url + '/ai/v1/messages',
  AI_FEEDBACK:    base_url + '/ai/v1/messages',
  AI_SUGGESTED:   base_url + '/ai/v1/messages',

};

module.exports = {
  API
};