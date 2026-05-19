// components/acg-images/acg-images.js
Component({
  properties: {
    acg_url: {
      type: String,
      value: "https://github.com/yandifei/ArisuQQChatAI/raw/main/展示项目的图片/爱丽丝.png"
      },
  },
  // 方法必须写在 methods 里面(吐槽真的颇有vue2的味道)
  methods: {
    save() {
      const imgUrl = this.properties.acg_url;
      wx.downloadFile({
        url: imgUrl,
        success: (res) => {
          wx.saveImageToPhotosAlbum({
            filePath: res.tempFilePath,
            success() {
              wx.showToast({ title: '保存成功', icon: 'success' });
            },
            fail(err) {
              wx.showToast({ title: '保存失败', icon: 'none' });
            }
          });
        },
        fail() {
          wx.showToast({ title: '下载失败', icon: 'none' });
        }
      });
    }
  }
})