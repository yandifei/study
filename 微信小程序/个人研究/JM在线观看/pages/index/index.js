// index.js
Page({
  data: {
    img_urls: [],
  },

  handleSubmit(e) {
    const formData = e.detail.value;
    console.log('表单数据:', formData);
    wx.redirectTo({
      url: '/pages/JMComic/JMComic'
    });
  }
 
})
