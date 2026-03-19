// index.js

Page({
  data:{
    Person:({
      age:"18",
      name:"yandifei"
    }),
    randNum:Math.random().toFixed(1) * 10,
    count:0,
    array: [{
      message: 'foo',
    }, {
      message: 'bar'
    }]
  },
  
  add(){
    console.log("我被点击了"),
    this.setData({
      count: this.data.count + 1
    })
  }
})
