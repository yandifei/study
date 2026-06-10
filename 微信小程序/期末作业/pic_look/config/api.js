// config/api.js
// 导出代码
// const { API } = require('../../config/api.js');

const accountInfo = wx.getAccountInfoSync();
const envVersion = accountInfo.miniProgram.envVersion; // 'develop', 'trial', 'release'

// 定义不同环境对应的基础URL
const base_urls = {
  // develop: 'http://127.0.0.1:8000',   // 开发版（开发者工具、真机预览）得要用Nginx反代才行
  develop: 'http://127.0.0.1:21325',   // 本地单个服务
  trial: 'https://scraggly-regress-cape.ngrok-free.dev',    // 体验版（上传后设为体验版）
  release: 'https://scraggly-regress-cape.ngrok-free.dev'    // 正式版（审核上线后）
};

// 自动匹配当前环境的URL
const base_url = base_urls[envVersion];

// 定义所有业务接口路径（方便管理）
const API = {
  // 邮箱登陆
  SEND_CODE: base_url + '/auth/send-code',       // 发送邮箱验证码
  USER_LOGIN: base_url + '/auth/login',          // 验证码登录/注册
  USER_REFRESH: base_url + '/auth/refresh',      // accesss接口刷新
  USER_LOGOUT: base_url + '/auth/logout',        // 登出

  // 用户模块
  USER_INFO: base_url + '/auth/me',              // 用户信息
  USER_DELETE: base_url + '/auth/logout',        // 注销登陆

  // 浏览模块
  BROWSE_LIST: base_url + '/browse/',            // 我的浏览记录 (GET)
  BROWSE_BATCH: base_url + '/browse/',           // 批量记录浏览 (POST)
  BROWSE_CLEAR: base_url + '/browse/',           // 清空我的浏览记录 (DELETE)

  // 收藏模块
  FAVORITE_LIST: base_url + '/favorite/',        // 我的收藏列表 (GET)
  FAVORITE_ADD: base_url + '/favorite/',         // 添加收藏 (POST)
  FAVORITE_CLEAR: base_url + '/favorite/',       // 清空我的收藏 (DELETE)
  FAVORITE_REMOVE: base_url + '/favorite/',      // 取消收藏 (DELETE + image_id 路径参数)
};

module.exports = {
  API
};