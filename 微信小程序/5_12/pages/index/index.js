// index.js
Page({
  getData() {
    wx.request({
      url: 'https://api.thecatapi.com/v1/images/search',
      data: { limit: 1 },
      method: 'GET',
      dataType: 'json',
      timeout: 10000,
      success: (res) => {
        if (res.data && res.data.length) {
          this.setData({ imgurl: res.data[0].url });
        }
      },
      fail: (err) => {
        console.error('请求失败', err);
        wx.showToast({ title: '加载失败', icon: 'none' });
      },
      complete: () => {
        wx.stopPullDownRefresh(); // 停止下拉刷新动画
      }
    });
  },

  onPullDownRefresh() {
    this.getData();
  },

  onReachBottom() {
    console.log("触底部了")
    this.getData();
  },

  // 选择相片
  getImg(){
    // chooseImage不再维护
    // wx.chooseImage({
    // 用新版的
    wx.chooseMedia({
      // 只选择图片，因为新接口能同时选图片和视频
      count: 1,
      mediaType: ['image'], 
      // 原图的选项名也变了
      sourceType: ['album', 'camera'],
      success (res) { 
        console.log(res)
        const tempFilePath = res.tempFiles[0].tempFilePath
        console.log('选中的图片路径：', tempFilePath)
      //  tempFiles[0] 的具体内容：
      //  {
      //    tempFilePath: '', // 临时文件路径 (对应旧版的 res.tempFilePaths[0])
      //    size: 0,         // 文件大小（字节）
      //    duration: 0,     // 视频时长（秒）
      //    height: 0,       // 高度（像素）
      //    width: 0,        // 宽度（像素）
      //    fileType: 'image' // 文件类型
      //  }
      }
    })
  }

})
