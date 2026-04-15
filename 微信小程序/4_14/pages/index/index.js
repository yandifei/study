// index.js
Page({
  data:{
    value:"",
    value_radio:"",
    value_switch:"",
    selist:["北京","广州","上海","深圳"],
    index:1,
    value_picker:"01:00",
    value_picker2:"2026-4-14",
    region:["北京","广州","上海","深圳"],

  },
  cbchange(e) {
    console.log(e.detail.value)
    this.setData({
      value:e.detail.value
    })
  },
  rdchange(e) {
    console.log(e.detail.value)
    this.setData({
      value_radio:e.detail.value
    })
  },

  shchange(e) {
    console.log(e.detail.value)
    this.setData({
      value_switch:e.detail.value
    })
  },

  prchange(e) {
    console.log(e.detail.value)
    this.setData({
      index:e.detail.value
    })
  },

  timechange(e) {
    console.log(e.detail.value)
    this.setData({
      value_picker:e.detail.value
    })
  },
  timechange2(e) {
    console.log(e.detail.value)
    this.setData({
      value_picker2:e.detail.value
    })
  },
  regionchange(e) {
    console.log(e.detail.value)
    this.setData({
      region:e.detail.value
    })
  },
})
