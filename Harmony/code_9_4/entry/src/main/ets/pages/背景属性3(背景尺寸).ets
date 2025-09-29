/*背景图尺寸-backgroundImageSize
作用：背景图缩放
属性：.backgroundImageSize(宽高对象或枚举）
参数：
背景图宽高:{width:尺寸，height：尺寸}
枚举ImageSize:
Contain：等比例缩放背景图，当宽或高与组件尺寸相同停止缩放
Cover：等比例缩放背景图至图片完全覆盖组件范围
Auto：默认，原图尺寸
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
        .width(360)
        .height(300)
        .backgroundColor(Color.Pink)
        .backgroundImage($r("app.media.Arisu2"))
          //自动调整大小
        .backgroundImagePosition(Alignment.Center)
          //硬编码，写死宽高
        .backgroundImageSize({
          width: 150,
          //一般都是只写一个，让图片自动调整大小
          // height: 100
        })
          //设置背景尺寸的枚举
        .backgroundImageSize(ImageSize.Auto) //Auto：自动调整（实际就是保持比例的同时居中显示）
        .backgroundImageSize(ImageSize.Contain) //Contain：等比例缩放，展示整张图片，可能会留白
        .backgroundImageSize(ImageSize.Cover) //Cover：等比例缩放，让图片铺满整个容器，不会留白，但是有可能会有部分内容显示不全
        .backgroundImageSize(ImageSize.FILL) //FILL：fill强制填满 但是不保证图片放缩比例


    }
  }
}

