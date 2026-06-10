const request = require('../../utils/request.js');
const { API } = require('../../config/api.js');

Page({
  data: {
    avatar: "",
    username: '',
    email: '',
    menus: [
      { key: 'favorites', icon: '💖', label: '我的收藏', tap: 'goFavorites' },
      { key: 'history',   icon: '🌸', label: '浏览记录', tap: 'goHistory'   }
    ]
  },

  onShow() {
    wx.setTabBarStyle({ selectedColor: '#fff', "backgroundColor": "#ffb6c1",})
    this.loadUserInfo();
  },

  /**
   * 从后端获取当前用户信息
   */
  loadUserInfo() {
    // 腾讯官方公开接口
    this.setData({avatar: `https://q.qlogo.cn/headimg_dl?dst_uin=${wx.getStorageSync('qq')}&spec=640`})
    
    // 后端数据库信息 —— request 自动挂 token、遇 401 自动刷新
    request({ url: API.USER_INFO, method: 'GET' })
      .then(res => {
        if (res.statusCode === 200) {
          const { username, email, avatar } = res.data;
          this.setData({
            username: username || '',
            email: email || '',
            avatar: avatar || this.data.avatar
          });
        }
      })
      .catch(err => console.error('获取用户信息失败', err));
  },

  goFavorites() {
    wx.showToast({ title: '收藏功能开发中', icon: 'none' });
  },

  goHistory() {
    wx.showToast({ title: '浏览记录功能开发中', icon: 'none' });
  },

  handleLogout() {
    wx.showModal({
      title: '确认注销',
      content: '注销后需要重新登录，确定要继续吗？',
      confirmText: '确定注销',
      cancelText: '再想想',
      confirmColor: '#ff6b9d',
      success: (res) => {
        if (res.confirm) {
          this.doLogout();
        }
      }
    });
  },

  doLogout() {
    const refreshToken = wx.getStorageSync('refresh_token');

    const cleanup = () => {
      wx.removeStorageSync('access_token');
      wx.removeStorageSync('refresh_token');
      wx.removeStorageSync('expire_time');
      wx.reLaunch({ url: '/pages/login/login' });
    };

    if (refreshToken) {
      request.post(API.USER_LOGOUT, { refresh_token: refreshToken })
        .finally(cleanup);
    } else {
      cleanup();
    }
  }
});
