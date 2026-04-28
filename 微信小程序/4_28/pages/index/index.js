// index.js
Page({
  // 1. 显示消息提示框
  showToast() {
    wx.showToast({
      title: '操作成功', // 提示的内容
      icon: 'success',  // 图标，支持 "success", "loading", "none", "error"
      duration: 2000    // 提示的延迟时间
    })
  },

  // 2. 显示消息模态框
  showModal() {
    wx.showModal({
      title: '提示',      // 提示的标题
      content: '这是一个模态弹窗', // 提示的内容
      success (res) {
        if (res.confirm) {
          console.log('用户点击确定')
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
  },

  // 3. 显示加载框（你图片中已有的部分）
  showLoading() {
    wx.showLoading({
      title: '正在加载', // 加载提示文字
      // mask: true        // 是否显示透明蒙层，防止触摸穿透
    })
  },

  // 4. 取消加载框
  hideLoading() {
    wx.hideLoading()
  },

  // 显示 TabBar
  showTabbar() {
    wx.showTabBar({
      animation: true // 是否需要动画效果，默认为 false
    })
  },

  // 隐藏 TabBar
  hideTabbar() {
    wx.hideTabBar({
      animation: true // 是否需要动画效果
    })
  },

  
})
