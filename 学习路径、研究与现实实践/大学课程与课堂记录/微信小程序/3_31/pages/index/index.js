// index.js
Page({
  data: {
    scrollList: ["家装", "服饰", "家电", "美食", "特产"],
    swiperList: [
      {
        id: 1,
        imgUrl: 'https://storage.360buyimg.com/component-libray/images/pc/pc_banner_first_focus_furniture.png',
        title: "小米手机，旗舰选择"
      },
      {
        id: 2,
        imgUrl: 'https://storage.360buyimg.com/component-libray/images/pc/pc_banner_first_focus_office_equipment.png',
        title: "京东美妆，靓丽你我"
      },
      {
        id: 3,
        imgUrl: 'https://storage.360buyimg.com/component-libray/images/pc/pc_banner_first_focus_computer.gif',
        title: "京东好货，值得购买"
      },
      {
        id: 4,
        imgUrl: 'https://storage.360buyimg.com/component-libray/images/pc/pc_banner_first_focus_cell_phone.png',
        title: "京东好纸，干净卫生"
      }
    ]
  },
  scrollTop() {
    console.log("触发了scrollTop事件（横向滚动到左边界）");
  },
  scrollLower() {
    console.log("触发了scrollLower事件（横向滚动到右边界）"); 
  }
})