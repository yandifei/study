/*背景属性
属性方法     属性
背景色       backgroundColor
背景图       backgroundImage
背景图位置    backgroundImagePosition
背景图尺寸    backgroundImageSize

背景图-backgroundImage
属性：.backgroundImage（背景图地址）

背景图-backgroundlmage
属性：.backgroundImage(背景图地址，背景图平铺方式-枚举ImageRepeat)
背景图平铺方式：（可省略）
NoRepeat:不平铺，默认值
X：水平平铺
Y：垂直平铺
XY：水平垂直均平铺
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
      Text("我是内容文本")
        .fontColor(Color.White)
        .width(200)
        .height(200)
        .backgroundColor(Color.Pink)
          // backgroundImage(加载背景图片，是否平铺ImageRepeat枚举)
        .backgroundImage($r("app.media.Arisu1"), ImageRepeat.X)
    }
    .padding(20)
  }
}

