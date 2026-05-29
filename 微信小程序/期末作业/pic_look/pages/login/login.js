// pages/login/login.js
Page({
  login() {
    wx.showLoading({ title: '正在登陆中...', mask: true});
    wx.login({
      success (res) {
        if (res.code) {
          // //发起网络请求
          // wx.request({
          //   url: 'http://localhost:21325/login',
          //   timeout: 10,
          //   data: {
          //     code: res.code
          //   }
          // })
          console.log(res.code)
          wx.hideLoading()
        } else {
          console.log('登录失败！' + res.errMsg)
          wx.showToast({ title: '登录失败！' + res.errMsg, icon: 'error' });
        }
      }
    })
  }
})