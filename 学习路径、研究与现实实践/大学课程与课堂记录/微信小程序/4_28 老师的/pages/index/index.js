// index.js
Page({
  showToast(){
    wx.showToast({
      title:"提示内容提示内容提示内容提示内容",
      icon:"success",
      duration:3000,
      mask:true,
      success:(result)=>{
        console.log(result)
      }
    })
  },
  showModal(){
    wx.showModal({
      title:"模态框",
      content:"提示的内容。。。",
      cancelText:"否",
      confirmText:"是",
      complete:(res)=>{
        if(res.confirm)
        console.log("是")
        else if(res.cancel)
        console.log("否")

      }
    })
  },
  showLoading(){
    wx.showLoading({
      title:"正在加载"
    })
  },
  hideLoading(){
    wx.hideLoading({
    })
  },
  showTabbar(){
    wx.showTabBar({ 
    })
  },
  hideTabbar(){
    wx.hideTabBar({ 
    })
  }

})
