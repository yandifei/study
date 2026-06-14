/**
 * utils/request.js
 * 统一请求封装 —— 自动挂 Authorization、遇 401 自动刷新 token 后重试
 *
 * 用法：
 *   const request = require('../../utils/request.js');
 *   request({ url: API.XXX, method: 'GET' }).then(res => {...}).catch(err => {...});
 *   request.get(API.XXX).then(...);
 *   request.post(API.XXX, { key: val }).then(...);
 *
 * 不需要认证的接口（如登录、发验证码）加 skipAuth: true：
 *   request({ url: API.SEND_CODE, method: 'POST', data: {...}, skipAuth: true })
 */

const { API } = require('../config/api.js');

// ==================== 刷新锁 ====================
// 解决并发 401：只发一次刷新请求，其他 401 排队等结果
let isRefreshing = false;
let refreshQueue = [];

// ==================== 工具函数 ====================

/**
 * 保存 token 到本地
 */
function saveTokens(data) {
  const { access_token, refresh_token, expires_in } = data;
  if (access_token) wx.setStorageSync('access_token', access_token);
  if (refresh_token) wx.setStorageSync('refresh_token', refresh_token);
  if (expires_in) wx.setStorageSync('expire_time', Date.now() + expires_in * 1000);
}

/**
 * 清除 token 并跳转登录页
 */
function clearAndGoLogin() {
  wx.removeStorageSync('access_token');
  wx.removeStorageSync('refresh_token');
  wx.removeStorageSync('expire_time');
  const pages = getCurrentPages();
  const currentPage = pages[pages.length - 1];
  if (!currentPage || currentPage.route !== 'pages/login/login') {
    wx.reLaunch({ url: '/pages/login/login' });
  }
}

/**
 * 调用后端刷新接口，返回新的 access_token
 */
function doRefresh() {
  const refreshTokenValue = wx.getStorageSync('refresh_token');
  if (!refreshTokenValue) {
    clearAndGoLogin();
    return Promise.reject(new Error('无 refresh_token'));
  }

  return new Promise((resolve, reject) => {
    wx.request({
      url: API.USER_REFRESH,
      method: 'POST',
      data: { refresh_token: refreshTokenValue },
      success: (res) => {
        if (res.statusCode === 200 && res.data.access_token) {
          saveTokens(res.data);
          resolve(res.data.access_token);
        } else {
          // refresh 也过期了，彻底登出
          clearAndGoLogin();
          reject(new Error('refresh_token 已过期'));
        }
      },
      fail: (err) => {
        clearAndGoLogin();
        reject(err);
      }
    });
  });
}

// ==================== 核心方法 ====================

/**
 * 发起请求（替代 wx.request）
 *
 * @param {Object}  options        - 同 wx.request，额外支持 skipAuth
 * @param {boolean} options.skipAuth - 跳过自动挂 Authorization（登录类接口）
 * @returns {Promise} resolve(res) / reject(err)
 */
function request(options = {}) {
  const { skipAuth, ...rest } = options;

  // 自动附加 Authorization
  if (!skipAuth) {
    const accessToken = wx.getStorageSync('access_token');
    if (accessToken) {
      rest.header = {
        'Authorization': `Bearer ${accessToken}`,
        ...rest.header
      };
    }
  }

  return new Promise((resolve, reject) => {
    const originalSuccess = rest.success;
    const originalFail = rest.fail;

    rest.success = (res) => {
      if (res.statusCode === 401 && !skipAuth) {
        // —— token 过期，进入刷新队列 ——
        refreshQueue.push({ options, resolve, reject });

        // 只有第一个 401 触发刷新
        if (!isRefreshing) {
          isRefreshing = true;

          doRefresh()
            .then(() => {
              // 刷新成功：用新 token 重试队列中的所有请求
              retryQueue();
            })
            .catch(() => {
              // 刷新失败：拒绝所有（clearAndGoLogin 已在 doRefresh 中调用）
              failQueue();
            });
        }
        // 其他并发 401 安静排队，等刷新完成后自动重试
        return;
      }

      // 非 401，正常返回
      if (originalSuccess) originalSuccess(res);
      resolve(res);
    };

    rest.fail = (err) => {
      if (originalFail) originalFail(err);
      reject(err);
    };

    wx.request(rest);
  });
}

/** 用新 token 重试队列中所有请求 */
function retryQueue() {
  const queue = refreshQueue.slice();
  refreshQueue = [];
  isRefreshing = false;

  const newToken = wx.getStorageSync('access_token');

  queue.forEach(({ options, resolve, reject }) => {
    const retryOptions = { ...options };
    delete retryOptions.success;
    delete retryOptions.fail;

    retryOptions.header = {
      ...retryOptions.header,
      'Authorization': `Bearer ${newToken}`
    };

    wx.request({
      ...retryOptions,
      success: (res) => resolve(res),
      fail: (err) => reject(err)
    });
  });
}

/** 刷新失败时拒绝队列中所有请求 */
function failQueue() {
  const queue = refreshQueue.slice();
  refreshQueue = [];
  isRefreshing = false;

  queue.forEach(({ reject }) => reject(new Error('登录已过期')));
}

// ==================== 便捷方法 ====================

request.get = function (url, options = {}) {
  return request({ ...options, url, method: 'GET' });
};

request.post = function (url, data, options = {}) {
  return request({ ...options, url, method: 'POST', data });
};

request.put = function (url, data, options = {}) {
  return request({ ...options, url, method: 'PUT', data });
};

request.delete = function (url, options = {}) {
  return request({ ...options, url, method: 'DELETE' });
};

// 暴露工具方法给外部使用（如登录页保存 token）
request.saveTokens = saveTokens;
request.clearAndGoLogin = clearAndGoLogin;

module.exports = request;
