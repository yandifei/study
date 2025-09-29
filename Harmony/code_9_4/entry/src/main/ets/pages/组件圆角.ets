/*设置组件圆角
属性：.borderRadius(参数）
参数：数值或对象（四个角单独设置）
topLeft：左上角
topRight：右上角
bottomLeft:左下角
bottomRight：右下角
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
      Text("没有圆角")
        .width(100)
        .height(60)
        .backgroundColor(Color.Pink)
        .margin({ bottom: 30 })
      //添加圆角：
      // 1. .borderRadius(数值) 四个角圆角相同
      // 1. .borderRadius({ 方位词: 值 }) 单独给某个角设置圆角
      Text("添加了圆角")
        .width(100)
        .height(60)
        .backgroundColor(Color.Orange)
        .borderRadius(15)
          //重复方法的话仅采用最后一个，和Qt一样也和css一样·
        .borderRadius({
          topLeft: 10,
          topRight: 20,
          bottomRight: 30,
          bottomLeft: 40
        })
    }
  }
}

