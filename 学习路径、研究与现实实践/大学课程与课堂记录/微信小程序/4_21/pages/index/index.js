// index.js
Page({
  data:{
    newTitle:"",
    newsarr:[
      {id: 1, title:"昨天信息太多。"},
      {id: 2, title:"今天的事情有点急。"},
      {id: 3, title:"明天是否也会如此"},
    ]
  },


  iptsubmit(e) {
    console.log(e.detail.value)
  },

  titlechange(e) {
    // console.log(e.detail.vaule)
    let oldTitle= e.detail.value
    this.setData({
      newTitle: this.detail.value
    })
  },

  newsubmit(e) {
    let id=Data.now()
    let oldArr=shis.data.newsarr
    oldArr.push({id, title: this.Data.newTitle})
    this.setData({
      oldArr: this.oldArr,
      newTitle:""
    })
  },

  delnews(e){
    let index=e.currentTarget.dataseet.index
    let oldarr=this.data.newsarr
    oldarr.splice(index,1)
    this.stData({
      newsarr:oldarr
    })
  }
})
