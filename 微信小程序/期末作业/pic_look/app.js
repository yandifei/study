const request = require('./utils/request.js');
const { API } = require('./config/api.js');

App({
  onLaunch() {
    this.checkLoginStatus();
  },

  onShow() {
    this.checkLoginStatus();
  },

  /**
   * 校验登录态：request 自动处理 token 过期 → 刷新 → 重试
   */
  checkLoginStatus() {
    const accessToken = wx.getStorageSync('access_token');
    if (!accessToken) {
      this.redirectToLogin();
      return;
    }

    request({ url: API.USER_INFO })
      .then(res => {
        if (res.statusCode === 200) this.redirectToHome();
        else this.redirectToLogin();
      })
      .catch(() => this.redirectToLogin());
  },

  redirectToHome() {
    const pages = getCurrentPages();
    const currentPage = pages[pages.length - 1];
    if (currentPage && currentPage.route === 'pages/index/index') return;
    wx.reLaunch({ url: '/pages/index/index' });
  },

  redirectToLogin() {
    const pages = getCurrentPages();
    const currentPage = pages[pages.length - 1];
    if (currentPage && currentPage.route === 'pages/login/login') return;
    wx.reLaunch({ url: '/pages/login/login' });
  }
});
