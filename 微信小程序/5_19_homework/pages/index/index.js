// index.js
Page({
  data: {
    img_urls: [],
  },

  // 页面加载时立即请求图片
  onLoad() {
    wx.showLoading({ title: '图片刷新中' });
    this.get_img_urls()
    setTimeout(() => { wx.hideLoading() }, 1000);
  },

  // 页面下拉刷新
  onPullDownRefresh() {
    wx.showLoading({ title: '图片刷新中' });
    this.setData({ img_urls: [] });
    this.get_img_urls()
    setTimeout(() => { wx.hideLoading(); wx.stopPullDownRefresh() }, 1000);
  },

  //页面触底事件的处理函数
  onReachBottom() {
    this.get_img_urls()
  },

  get_img_urls() {
    console.log("进行了请求");
    // 微信网络请求的方法
    wx.request({
      // 请求10张PC图片
      url: "https://t.alcy.cc/json/?lai=10",
      // 请求成功
      success: (res) => {
        // 不断增加
        this.setData({ img_urls: [...this.data.img_urls, ...res.data.links]});
      },
      // 请求失败
      fail: (err) => {
        console.error('请求失败', err);
      }
    });
  }
})
