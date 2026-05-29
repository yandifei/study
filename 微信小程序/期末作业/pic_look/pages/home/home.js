// pages/home/home.js
Page({
  data: {
    list: [
      {code: 'pc', name: 'PC壁纸', icon: '💻', type: ''},
      {code: 'ai', name: 'AI生成', icon: '🤖', type: 'ai'},
      {code: 'aimp', name: 'AI竖屏', icon: '📱', type: 'ai'},
      {code: 'bd', name: '白底极简', icon: '⚪', type: ''},
      {code: 'fj', name: '风景', icon: '🏔️', type: ''},
      {code: 'fjmp', name: '风景竖屏', icon: '🏞️', type: ''},
      {code: 'lai', name: '软萌表情', icon: '🐾', type: 'moe'},
      {code: 'moe', name: '萌图', icon: '🌸', type: 'moe'},
      {code: 'moemp', name: '萌图竖屏', icon: '💖', type: 'moe'},
      {code: 'mp', name: '横屏壁纸', icon: '📺', type: ''},
      {code: 'tx', name: '头像', icon: '👤', type: ''},
      {code: 'xhl', name: '软萌狐', icon: '🦊', type: 'moe'},
      {code: 'ys', name: '原神横屏', icon: '⚔️', type: 'ys'},
      {code: 'ysmp', name: '原神竖屏', icon: '🎒', type: 'ys'}
    ]
  },

  // 页面加载时改变底部导航栏颜色
  onLoad(args) {
    wx.setTabBarStyle({ selectedColor: '#5d4a30', "backgroundColor": "#ffeed2",})
  },

  nav(e) {
    const code = e.currentTarget.dataset.url;
    wx.navigateTo({ url: `/pages/gallery/gallery?code=${code}` });
  }
})