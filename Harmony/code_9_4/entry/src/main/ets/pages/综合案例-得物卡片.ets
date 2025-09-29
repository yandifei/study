/*综合案例-得物卡片
 实现分析：
1、整体，纵向布局-Column组件
2、底部，横向布局-Row组件
3、左右，两个Row组件
4、左侧可似自适应layoutWeight
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
      Column() {
        Image($r("app.media.Arisu2"))
          .width("100%")
          .borderRadius({ topLeft: 5, topRight: 5 })
        //文本框
        Text("爱丽丝壁纸 | 每日艺术分享 No.1")
          .fontWeight(500 )
          .fontSize(14)
          .lineHeight(18) //字体行高的大小
          .height(50)
          .padding({ left: 15, right: 15})

        // 底部
        Row() {
          // 头像、名称
          Row({ space: 5}) {
            Image($r("app.media.Arisu1"))
              .width(16)
              .height(16)
              .borderRadius(8)
            Text("插画师分享聚集地")
              .fontSize(10)
              .fontColor("#999 ")

          }
          .layoutWeight(1)
          // 点赞图标和点赞岁数
          Row({ space: 5}) {
            Image($r("app.media.ic_hand_thumbsup_fill"))
              .width(12)
              .fillColor("#999")
            Text("2300")
              .fontSize(10)
              .fontColor("#666")

          }
        }
        .padding({ left: 15, right: 15})
      }
      .width(200)
      // 高度不建议写死
      // .height(400) // 先定死一个高，后续内容撑开来支撑
      .backgroundColor(Color.White)
      .borderRadius(5)
      .padding({ bottom: 15}) // 设置边距
    }
    .padding(10)
    .width("100%")
    .height("100%")
    .backgroundColor("#ccc")
  }
}

