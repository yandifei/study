/*个人中心-顶部导航
 实现分析：
1、横向布局Row组件
2、排布方向水平往右
（主轴）
3、在主轴上两端对齐spaceBetween
 */

//去除系统安全区域（导入包）
import { window } from '@kit.ArkUI';


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
  // 去除系统的安全区域
  onPageShow(): void {
    window.getLastWindow(getContext(this), (err, data) => {
      if (!err.code) {
        data.setWindowLayoutFullScreen(true);
      }
    })
  }
  // 构建 -> 界面
  build() {
    Column() {
      Row() {
        Image($r("app.media.ic_chevron_left"))
          .width(18)
        Text("个人中心")
        Image($r("app.media.ic_more"))
          .width(28)
      }
      .width("100%")
      .height(50)
      .backgroundColor(Color.White)
      // 设置3个组件的对齐方式
      .justifyContent(FlexAlign.SpaceBetween)
      //外边距
      .padding({ left: 10, right: 10 })

    }
    .width("100%")
    .height("100%")
    .backgroundColor("#ccc")
    // .expandSafeArea([SafeAreaType.SYSTEM])
  }
}

