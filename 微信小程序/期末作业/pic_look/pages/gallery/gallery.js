const request = require('../../utils/request.js');
const { API } = require('../../config/api.js');

Page({
  data: {
    code: "",
    isVerticalType: false,
    img_urls: [],
  },

  onLoad(args) {
    const is_mobile_portrait = ['aimp', 'fjmp', 'moemp', 'mp', 'tx', 'xhl', 'ysmp'];
    this.setData({
      code: args.code || '',
      isVerticalType: is_mobile_portrait.includes(args.code)
    });
    wx.showLoading({ title: '图片刷新中' });
    this.get_img_urls();
    setTimeout(() => { wx.hideLoading(); }, 1000);
  },

  onPullDownRefresh() {
    wx.showLoading({ title: '图片刷新中' });
    this.setData({ img_urls: [] });
    this.get_img_urls();
    setTimeout(() => { wx.hideLoading(); wx.stopPullDownRefresh(); }, 1000);
  },

  onReachBottom() {
    this.get_img_urls();
  },

  // 外部图源，不走后端认证
  get_img_urls() {
    console.log("进行了请求");
    wx.request({
      url: `https://t.alcy.cc/json/?${this.data.code}=10`,
      success: (res) => {
        this.setData({ img_urls: [...this.data.img_urls, ...res.data.links]});
      },
      fail: (err) => {
        console.error('请求失败', err);
      }
    });
  },

  // 浏览记录上报 —— 自动挂 token、遇 401 自动刷新
  reportBrowse(images) {
    request.post(API.BROWSE_BATCH, { images })
      .then(res => console.log('浏览记录上传成功', res))
      .catch(err => console.error('浏览记录上传失败', err));
  }
});
