/*Image图片组件
作用：界面中展示图片
语法：Image(图片数据源）支持网络图片资源和本地图片资源
column(){
  Image($r(资源地址))
}
 */
//图片url
const arisuImage: string = "https://static.kivo.wiki/images/students/%E5%A4%A9%E7%AB%A5%20%E7%88%B1%E4%B8%BD%E4%B8%9D/%E5%A5%B3%E4%BB%86/CH0200_home_Idle_01_0.8374999999999998.jpg"

@Entry
@Component
struct Index {
  @State message: string = "你好雁低飞";
  // 构建 -> 界面
  build() {
    // // 1.网络图片加载 Image("网图地址")
    // Column() {
    //   Image(arisuImage)
    //     .height(50) //调整宽度或高度的话，对应的高度和宽度会自动等比例缩放
    // }
    // .width("100%")

    // 2.本地图片加载 Image($r("app.media.文件名"))
    Column() {
      Image($r("app.media.Arisu1"))
        .width(200) //设置宽度为200像素
      Text("女仆爱丽丝！！！")
        .width(200)
      Row() {
        Image($r("app.media.Arisu2"))
          .width(20) //设置宽度
        Text("爱丽丝转职了")
      }
      .width(200) //设置整个行的宽度
    }
  }
}