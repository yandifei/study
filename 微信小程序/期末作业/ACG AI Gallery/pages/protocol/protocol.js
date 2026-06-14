// pages/protocol/protocol.js
/**
 * 用户协议展示页面
 * 萌系 ACG 风格 · 纯展示页
 */
Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 控制卡片入场动画
    cardAnimated: false,
    // 滚动位置（可用于后续扩展，如滚动到底部显示印章）
    scrollTop: 0
  },

  /**
   * 生命周期函数 - 监听页面加载
   */
  onLoad(options) {
    // 页面加载时触发入场动画（轻微延迟，让页面先完成初始渲染）
    setTimeout(() => {
      this.setData({
        cardAnimated: true
      });
    }, 150);
  },

  /**
   * 生命周期函数 - 监听页面显示
   */
  onShow() {
    // 如果从其他页面返回，确保动画状态正确
    if (!this.data.cardAnimated) {
      setTimeout(() => {
        this.setData({ cardAnimated: true });
      }, 100);
    }
  },

  /**
   * 监听页面滚动（scroll-view 的 bindscroll 事件）
   */
  onScroll(e) {
    // 记录滚动位置
    this.setData({
      scrollTop: e.detail.scrollTop
    });
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {
    return {
      title: 'ACG智能图廊 - 用户协议',
      path: '/pages/protocol/protocol'
    };
  },

  /**
   * 分享到朋友圈（需开启权限）
   */
  onShareTimeline() {
    return {
      title: 'ACG智能图廊 - 用户协议'
    };
  }
});