// pages/gallery/gallery.js
Page({
  data: {
    // 接收url拼接的参数
    code: "",
    // 用来判断当前code是否属于竖屏类型
    isVerticalType: false, 
    img_urls: [],
  },

  // 页面加载时立即请求图片
  onLoad(args) {
    // console.log(args)
    // 判断图片是否竖屏，用来做条件渲染的判断
    const is_mobile_portrait = ['aimp', 'fjmp', 'moemp', 'mp', 'tx', 'xhl', 'ysmp'];
    
    this.setData({ 
      // 判定是否拿到字符串并拿到传递的字符串，没有则为''
      code: args.code || '',
      // 判断code是否存在需要竖屏的数组中(这里需要说明code没有被赋值好不能直接调)
      isVerticalType: is_mobile_portrait.includes(args.code)
    })
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
      url: `https://t.alcy.cc/json/?${this.data.code}=10`,
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
