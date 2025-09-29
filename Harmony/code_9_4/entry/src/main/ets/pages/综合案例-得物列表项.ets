/*综合案例-得物列表项
实现分析：
1、整体-横向布局Row
2、Row主轴，两端对齐
3、内部子元素，一个列，一个行
4、列的内容居左显示alignltems(..)
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
        // 左侧列
        // space调整2个Text之间的距离
        Column({ space: 5}) {
          Text("玩一玩")
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
          Text("签到兑礼 | 超多大奖 超好玩")
            .fontSize(12)
            .fontColor("#999")
        }
        .alignItems(HorizontalAlign.Start)
        // 右侧行
        Row({ space: 5}) {
          Image($r("app.media.Arisu1"))
            .width(40)
            .height(40)
            .backgroundColor("#efefef")
            .borderRadius(5)
          Image($r("app.media.ic_chevron_right"))
            .width(10)
              //给矢量图添加颜色
            .fillColor("#999")
        }
      }
      .width("100%")
      .height("8%")
      .backgroundColor(Color.White)
      .borderRadius(5)
      .justifyContent(FlexAlign.SpaceBetween)
      .padding({ left: 15, right: 15, top: 5, bottom: 5})
    }
    .width("100%")
    .height("100%")
    .backgroundColor("#ccc")
  }
}

