// index.js
Page({
  data: {
    c_list: [
      {
        imgsrc:"https://github.com/yandifei/ArisuQQChatAI/raw/main/展示项目的图片/爱丽丝.png",
        name: "爱丽丝",
        price: 1000
      },
      {
        imgsrc:"https://github.com/yandifei/ArisuQQChatAI/raw/main/展示项目的图片/爱丽丝.png",
        name: "爱丽丝1",
        price: 1001
      },
      {
        imgsrc:"https://github.com/yandifei/ArisuQQChatAI/raw/main/展示项目的图片/爱丽丝.png",
        name: "爱丽丝2",
        price: 1002
      },
      {
        imgsrc:"https://github.com/yandifei/ArisuQQChatAI/raw/main/展示项目的图片/爱丽丝.png",
        name: "爱丽丝3",
        price: 1003
      },
    ]
  },

  changeNum(e) {
    // 拿到当前点击的是第几个组件
    const index = e.currentTarget.dataset.index;
    // 更新父组件对应的数组数据
    this.setData({
      [`c_list[${index}].price`]: e.detail
    });
  }
})
