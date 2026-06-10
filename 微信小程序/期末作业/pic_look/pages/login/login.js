const request = require('../../utils/request.js');
const { API } = require('../../config/api.js');

Page({
  data: {
    email: '',
    code: '',
    isSending: false,
    countDown: 0
  },

  onEmailInput(e) { this.setData({ email: e.detail.value.trim() }); },
  onCodeInput(e) { this.setData({ code: e.detail.value.trim() }); },

  isEmailValid(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  },

  // 获取验证码（无需认证）
  sendCode() {
    const { email, isSending } = this.data;
    if (!this.isEmailValid(email)) {
      return wx.showToast({ title: '请输入有效的邮箱地址', icon: 'none' });
    }
    if (isSending) return;

    this.setData({ isSending: true });

    request({
      url: API.SEND_CODE,
      method: 'POST',
      data: { email },
      timeout: 5000,
      skipAuth: true
    })
      .then(res => {
        if (res.statusCode === 200) {
          wx.showToast({ title: '验证码已发送', icon: 'success' });
          this.startCountDown();
          const qq = (email || '').match(/(\d+)@qq\.com/)?.[1];
          wx.setStorageSync('qq', qq);
        } else if (res.statusCode === 429) {
          wx.showToast({ title: res.data.detail || '操作太频繁', icon: 'none' });
        } else {
          wx.showToast({ title: `服务异常(${res.statusCode})`, icon: 'error' });
        }
      })
      .catch(() => {
        wx.showToast({ title: '请求超时，请重试', icon: 'none' });
        this.setData({ isSending: false });
      });
  },

  startCountDown() {
    this.setData({ countDown: 60 });
    const timer = setInterval(() => {
      if (this.data.countDown <= 1) {
        clearInterval(this.timer);
        this.setData({ countDown: 0, isSending: false });
      } else {
        this.setData({ countDown: this.data.countDown - 1 });
      }
    }, 1000);
  },

  // 登录（无需认证，但需要保存返回的 token）
  handleLogin() {
    const { email, code } = this.data;
    if (!this.isEmailValid(email) || !code) {
      return wx.showToast({ title: '请填写正确的邮箱和验证码', icon: 'none' });
    }

    wx.showLoading({ title: '登录中...' });

    request({
      url: API.USER_LOGIN,
      method: 'POST',
      data: { email, code },
      skipAuth: true
    })
      .then(res => {
        wx.hideLoading();
        if (res.statusCode === 200) {
          request.saveTokens(res.data);
          wx.reLaunch({ url: "/pages/home/home" });
        } else if (res.statusCode === 401) {
          wx.showToast({ title: res.data.detail, icon: 'none' });
        } else {
          wx.showToast({ title: "服务器异常:" + res.data, icon: 'none' });
        }
      })
      .catch(() => {
        wx.hideLoading();
        wx.showToast({ title: '请求超时，请重试', icon: 'none' });
      });
  }
});
