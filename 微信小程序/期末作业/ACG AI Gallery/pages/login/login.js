const request = require('../../utils/request.js');
const { API } = require('../../config/api.js');

Page({
  data: {
    isAgree: false, // 用来记录用户是否同意用户协议和隐私政策
    email: '',
    code: '',
    isSending: false,
    countDown: 0,
  },

  onEmailInput(e) { this.setData({ email: e.detail.value.trim() }); },
  onCodeInput(e) { this.setData({ code: e.detail.value.trim() }); },

  isEmailValid(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  },

  onAgreeChange() {
    this.setData({
      // 新的状态是当前状态取反(需要要拿到e去解析具体传参)
      isAgree: !this.data.isAgree
    })
  },

  // 获取验证码（无需认证）
  sendCode() {
    const { email, isSending } = this.data;
    if (!this.isEmailValid(email)) {
      return wx.showToast({ title: '请输入有效的邮箱地址', icon: 'none' });
    }
    if (isSending) return;

    this.setData({ isSending: true });
    console.log(API.SEND_CODE)
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
    // 检查用户是否读取勾选了“用户协议”和“隐私政策”
    if (!this.data.isAgree) {
      return wx.showToast({ title: '请阅读并同意协议', icon: 'none' });
    }

    // 检查右键和验证码上是否都填写了
    const { email, code } = this.data;
    if (!this.isEmailValid(email) || !code) {
      return wx.showToast({ title: '请正确填写邮箱和验证码', icon: 'none' });
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
          wx.setStorageSync('qq', email.match(/(\d+)@qq\.com/)?.[1]);
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
  },

  // 用户协议
  openUserAgreement() {
    wx.navigateTo({ url: '/pages/protocol/protocol' })
  },

  // 隐私政策
  // 打开微信官方隐私协议页面（推荐用这个）
  openPrivacyContract() {
    wx.openPrivacyContract({
      fail: (err) => {
        // 打开兜底界面
        wx.navigateTo({ url: '/pages/privacy/privacy' })
      }
    })
  },
});
