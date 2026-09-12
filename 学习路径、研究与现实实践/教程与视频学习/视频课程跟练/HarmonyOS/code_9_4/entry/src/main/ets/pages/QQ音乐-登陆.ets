/*QQ音乐-登陆
 */


//华为官方图标（svg矢量图）
// https://developer.huawei.com/consumer/cn/design/harmonyos-symbol/

//去华为官网掏的logo
const huaweiLogo: string = "https://res-static.hc-cdn.cn/cloudbu-site/china/zh-cn/hdhomeportal/logonew.png"
//QQ的logo
const qqLogo: string = "https://wiki.connect.qq.com/wp-content/uploads/2013/10/03_qq_symbol-1-768x921.png"
//GitHub账号的头像
const liuying: string = "https://avatars.githubusercontent.com/u/178072152?v=4"

@Entry
@Component
struct Index {
  @State message: string = "雁低飞";
  // 构建 -> 界面
  build() {
    Column() {
      Image(liuying)
        .width(50)
      Text("雁低飞")
        .fontWeight(700)
        .margin({
          top: 10,
          bottom: 40
        })
      Button("QQ登陆")
        .width("100%")
        .margin({
          bottom: 10
        })
      Button("微信登陆")
        .width("100%")
        .backgroundColor("#ddd")
        .fontColor("#000")
    }
    .width("100%")
    .padding(20)
  }
}

