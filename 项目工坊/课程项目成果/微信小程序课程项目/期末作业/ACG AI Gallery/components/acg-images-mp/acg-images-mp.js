// components/acg-images-mp/acg-images-mp.js
Component({
  properties: {
    acg_url: {
      type: String,
      value: "https://github.com/yandifei/ArisuQQChatAI/raw/main/展示项目的图片/爱丽丝.png"
      },
    img_urls: {
      type: Array,
      value: []
    },
  },
  // 方法必须写在 methods 里面(吐槽真的颇有vue2的味道)
  methods: {
    // 对应wxml的save事件，用来保存到用户手机相册，这里是收藏了
    // save() {
    //   const imgUrl = this.properties.acg_url;
    //   wx.downloadFile({
    //     url: imgUrl,
    //     success: (res) => {
    //       wx.saveImageToPhotosAlbum({
    //         filePath: res.tempFilePath,
    //         success() {
    //           wx.showToast({ title: '保存成功', icon: 'success' });
    //         },
    //         fail(err) {
    //           wx.showToast({ title: '保存失败', icon: 'none' });
    //         }
    //       });
    //     },
    //     fail() {
    //       wx.showToast({ title: '下载失败', icon: 'none' });
    //     }
    //   });
    // },
    // 收藏
    favorite() {
      // 构建请求格式需要的内容
      const data = {
         // 时间戳 + 索引，避免同一毫秒内重复
         image_id: Date.now().toString(),
         image_url: this.properties.acg_url // 拿到父界面给我的url并给我传给image_url
      }
      request.post(API.FAVORITE_ADD, data, { timeout: 5000 })
      .then(res => {
        // console.log(res);
        console.log(data.image_id + '收藏记录上传成功');
      })
      .catch(err => console.error('收藏失败', err));
    },
    previewImage() {
      const urls = this.properties.img_urls;
      if (urls && urls.length > 0) {
        wx.previewImage({
          current: this.properties.acg_url,
          urls: urls
        });
      }
    }
  }
})