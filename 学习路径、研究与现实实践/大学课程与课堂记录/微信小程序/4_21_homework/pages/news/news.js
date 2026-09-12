// pages/news/news.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    // 存储新闻列表，每个元素为 {id, title}
    newsarr: [],
    // 绑定输入框的当前内容
    newTitle: ''      
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  // 监听输入框变化，实时更新 newTitle
  titlechange(e) {
    this.setData({
      newTitle: e.detail.value
    });
  },

  // 表单提交事件
  newssubmit(e) {
    // 获取用户输入的内容,通过表单的 name="newstitle"
    const inputTitle = e.detail.value.newstitle;
    //  生成新 ID,取当前最大 id +1，若数组为空则从1开始
    const oldArr = this.data.newsarr;
    const newId = oldArr.length === 0 ? 1 : oldArr[oldArr.length - 1].id + 1; // 这里我用三元操作符
    // 添加新闻到数组顶部
    const newNews = {
      id: newId,
      title: inputTitle.trim()
    };
    const newArr = [...oldArr, newNews]; // 给我我解引用
    
    // 更新 data，并清空输入框
    this.setData({
      newsarr: newArr,
      newTitle: ''   // 清空输入框显示
    });
  },

   // 删除新闻
   deleteNews(e) {
    const idToDelete = e.currentTarget.dataset.id;  // 获取点击的新闻 id
    const currentArr = this.data.newsarr;
    const newArr = currentArr.filter(item => item.id !== idToDelete);

    this.setData({
      newsarr: newArr
    });
  }
})