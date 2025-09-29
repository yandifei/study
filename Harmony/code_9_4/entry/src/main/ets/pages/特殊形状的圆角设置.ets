/*特殊形状的圆角设置
正圆
宽度高度一样
圆角是宽或高的一半

胶囊按钮（左右半圆）
宽度大，高度小
圆角是高的一半
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
      // 1.正圆 （头像）
      Image($r("app.media.Arisu1"))
        .width(100)
        .height(100)
        .borderRadius(50)

      // 2.胶囊按钮
      Text("今天还没打卡呦~") //胶囊按钮重点在宽而不在高
        .width(200)
        .height(50)
        .borderRadius(25)
        .backgroundColor(Color.Pink)
        .margin({ top: 20 })
    }
  }
}

