/*线性布局-交叉轴对齐方式
 属性：alignItems(
参数：枚举类型
交叉轴在水平应向：HorizontalAlign
交叉轴在垂直方向：VerticalAlign
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
    /* Column的对齐
    // Column交叉轴的对齐方式（水平往右）
    // alignItems(HorizontalAlign.Start)  Center End
    Column() {
      Text()
        .width(200)
        .height(100)
        .backgroundColor(Color.Pink)
        .border({ width: 2 })
      Text()
        .width(200)
        .height(100)
        .backgroundColor(Color.Pink)
        .border({ width: 2 })
      Text()
        .width(200)
        .height(100)
        .backgroundColor(Color.Pink)
        .border({ width: 2 })

    }
    //设置对齐为左对齐
    .alignItems(HorizontalAlign.Start)
    //设置对齐为右对齐
    .alignItems(HorizontalAlign.End)
    //设置对齐为居中对齐
    .alignItems(HorizontalAlign.Center)
    .width("100%")
    .height("100%")
    .backgroundColor("#ccc")
    */

    // Row交叉轴的对齐方式（垂直往下的交叉轴）
    // alignItems(VerticalAlign.Top)  Center Bottom
    Row() {
      Text()
        .width(50)
        .height(50)
        .backgroundColor(Color.Pink)
        .border({ width: 2 })
      Text()
        .width(50)
        .height(50)
        .backgroundColor(Color.Pink)
        .border({ width: 2 })
      Text()
        .width(50)
        .height(50)
        .backgroundColor(Color.Pink)
        .border({ width: 2 })

    }
    //设置对齐为顶部
    .alignItems(VerticalAlign.Top)
    //设置对齐为底部
    .alignItems(VerticalAlign.Bottom)
    //设置对齐为居中对齐
    .alignItems(VerticalAlign.Center)
    .width("100%")
    .height("100%")
    .backgroundColor("#ccc")
  }
}

