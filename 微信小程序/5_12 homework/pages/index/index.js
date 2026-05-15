// index.js
Page({
  data: {
    img_urls: [],
  },
  // 页面加载时立即请求图片
  onLoad() {
    this.get_img_urls()
  },

  // 页面下拉刷新
  onPullDownRefresh() {
    this.get_img_urls()
    // 至少1秒时间停顿（不然看不到load界面）
  },

  //页面触底事件的处理函数
  onReachBottom() {
    this.get_img_urls()
  },
  
  get_img_urls() {
    // 显示加载框
    wx.showLoading({ title: '图片刷新中' });
    // 微信网络请求的方法
    wx.request({
      // 请求10张PC图片
      url: "https://t.alcy.cc/json?pc=10",
      // 请求成功
      success: (res) => {
        // 设置图片链接列表
        this.setData({ img_urls: res.data.links });
        // 1秒时间后停止刷新用到的UI组件
        setTimeout(() => { wx.hideLoading(); wx.stopPullDownRefresh() }, 1000);
      },
      // 请求失败
      fail: (err) => {
        console.error('请求失败', err);
      }
    });
  }
})
