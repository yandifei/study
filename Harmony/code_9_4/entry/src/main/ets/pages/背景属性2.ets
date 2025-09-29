/*背景属性
属性方法     属性
背景色       backgroundColor
背景图       backgroundImage
背景图位置    backgroundImagePosition
背景图尺寸    backgroundImageSize

背景图位置-backgroundImagePosition
作用：调整背景图在组件内的显示位置，默认显示位置为组件左上角
属性：.backgroundImagePosition(坐标对象或枚举)
参数：
位置坐标：｛x：位置坐标，y：位置坐标}（单位下一节详细说）
枚举Alignment

30-背景定位-单位问题vp2px
这个不用看

1.单位vp和px更推荐使用哪个？
vp基于设备自动转换，保证不同设备视觉一致
2.如何将vp 转px?
vp2px(数值）
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
    //backgroundImagePosition
    //1，传入对象，设置位置坐标，背景图片的左顶点
    //  {x:坐标值，y:坐标值}
    //2.Alignment枚举，设置一些特殊的位置（中央、左顶点...）
    // Center 居中 TopStart 左顶点 TopEnd 右顶点 BottomEnd右下。
    Column() {
      Text("我是内容文本")
        .fontColor(Color.White)
        .width(360)
        .height(300)
        .backgroundColor(Color.Pink)
          // backgroundImage(加载背景图片，是否平铺ImageRepeat枚举)
        .backgroundImage($r("app.media.Arisu1"))
          //图片位置设置为相对位置
        .backgroundImagePosition({
          x: 100,
          y: 200
        })
        .backgroundImagePosition(Alignment.Center)
    }
    .padding(20)
  }
}

