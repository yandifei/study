// pages/lab/lab.js
Page({

  /**
   * 页面初始数据
   */
  data: {
    // 进度条的当前百分比，默认66，用来progress 组件和 slider 联动
    progressValue: 66,

    // 兴趣列表，每个选项都有唯一 value 和显示用的 label，checked 记录是否被选中
    interests: [
      { value: 'yueju', label: '粤剧', checked: false },
      { value: 'xingshi', label: '醒狮', checked: false },
      { value: 'zaocha', label: '早茶', checked: false },
      { value: 'gongfu', label: '功夫', checked: false }
    ],

    // 用于页面展示已选兴趣的中文字符串，例如“粤剧、早茶”
    selectedInterests: ''
  },

  // 弹出成功提示 Toast
  showToast() {
    wx.showToast({ title: '这是Toast提示', icon: 'success' });
  },

  // 弹出模态对话框，模拟需要用户确认的场景
  showModal() {
    wx.showModal({
      title: '模态框',
      content: '这是一个模态对话框示例',
      showCancel: true   // 显示取消按钮
    });
  },

  // 显示并自动隐藏loading加载动画，这里我用异步实现防止卡死
  showLoading() {
    wx.showLoading({ title: '加载中...(别催我)' });
    // 定时器2秒后隐藏loading
    setTimeout(() => { wx.hideLoading(); }, 2000);
  },

  // 进度条slider拖动时实时更新 progressValue
  sliderChange(e) {
    // e.detail.value 就是当前滑块的位置值（0-100）
    this.setData({ progressValue: e.detail.value });
  },

  // 兴趣多选框组发生变化时触发
  interestChange(e) {
    // e.detail.value 是当前所有被选中选项的 value 数组，例如 ['yueju', 'zaocha']
    const values = e.detail.value;

    // 根据 value 从 interests 数组中找到对应的 label
    const labels = values.map(v => {
      const item = this.data.interests.find(i => i.value === v);
      return item ? item.label : v;  // 万一找不到，兜底直接用 value
    });

    // 将选中的 label 用顿号连接，例如“粤剧、早茶”
    this.setData({ selectedInterests: labels.join('、') });
  }
})