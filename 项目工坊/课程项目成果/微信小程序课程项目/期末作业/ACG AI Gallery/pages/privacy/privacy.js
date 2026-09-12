// pages/privacy/privacy.js
// privacy-policy.js
Page({
  data: {
    cardAnimated: false,
    scrollTop: 0
  },

  onLoad() {
    setTimeout(() => {
      this.setData({ cardAnimated: true });
    }, 150);
  },

  onShow() {
    if (!this.data.cardAnimated) {
      setTimeout(() => {
        this.setData({ cardAnimated: true });
      }, 100);
    }
  },

  onScroll(e) {
    this.setData({ scrollTop: e.detail.scrollTop });
  },

  onShareAppMessage() {
    return {
      title: 'ACG智能图廊 - 隐私保护指引',
      path: '/pages/privacy-policy/privacy-policy'
    };
  },

  onShareTimeline() {
    return {
      title: 'ACG智能图廊 - 隐私保护指引'
    };
  }
});