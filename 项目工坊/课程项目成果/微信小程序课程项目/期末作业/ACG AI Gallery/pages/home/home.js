// pages/home/home.js
Page({
  data: {
    list: [
      {code: 'pc',     name: 'PC壁纸',     icon: '💻', type: ''},
      {code: 'mp',     name: '手机壁纸',   icon: '📱', type: 'mp'},
      {code: 'moe',    name: '萌图',       icon: '🌸', type: ''},
      {code: 'moemp',  name: '萌图竖屏',   icon: '💖', type: 'moemp'},
      {code: 'lai',    name: '七濑胡桃',   icon: '🐾', type: ''},
      {code: 'xhl',    name: '小狐狸',     icon: '🦊', type: 'xhl'},
      {code: 'ys',     name: '原神横屏',   icon: '⚔️', type: ''},
      {code: 'ysmp',   name: '原神竖屏',   icon: '🎒', type: 'ysmp'},
      {code: 'miku',   name: '初音横屏',   icon: '🎤', type: ''},
      {code: 'mikump', name: '初音竖屏',   icon: '🎶', type: 'mikump'},
      {code: 'fj',     name: '风景',       icon: '🏔️', type: ''},
      {code: 'bd',     name: '白底极简',   icon: '⚪', type: ''},
      {code: 'tx',     name: '头像',       icon: '👤', type: 'tx'}
    ]
  },

  // 页面加载时改变底部导航栏颜色
  onLoad(args) {
    wx.setTabBarStyle({ color: '#828282', selectedColor: '#5d4a30', "backgroundColor": "#ffeed2",})
  },
  // 页面加载时改变底部导航栏颜色
  onShow() {
    wx.setTabBarStyle({ color: '#828282', selectedColor: '#5d4a30', "backgroundColor": "#ffeed2",})
  },

  nav(e) {
    const code = e.currentTarget.dataset.url;
    wx.navigateTo({ url: `/pages/gallery/gallery?code=${code}` });
  }
})