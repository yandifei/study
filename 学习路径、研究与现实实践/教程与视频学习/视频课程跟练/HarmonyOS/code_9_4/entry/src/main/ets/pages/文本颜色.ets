@Entry
@Component
struct Index {
  @State message: string = "你好雁低飞";
  // 构建 -> 界面
  build() {
    // 1.演示文字颜色(枚举或 16进制)
    // Column() {
    //   Text("吕布")
    //     .fontSize(30)
    //     // .fontColor(Color.Red) //内置颜色
    //     .fontColor("#df3c50") //16进制颜色
    // }

    //综合练习:今日头条置顶新闻
    //思路： 排版->内容->美化
    Column() {
      Text("鸿蒙基础视频坐牢中...ing")
        .width("100%")
        .height(40)
        .fontSize(24)
      Row() {
        Text("置顶 ")
          .fontColor("#df3c50")
        Text("新华社 ")
          .fontColor("#a1a1a1")
        Text("4680评论")
          .fontColor("#a1a1a1")
      }
      .width("100%")
    }
    .width("100%")
  }
}