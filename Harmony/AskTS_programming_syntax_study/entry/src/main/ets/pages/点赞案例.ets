/*核心思路分析：
1.注册点击事件→onClick
2．点击时候，修改颜色，修改数字
①提取颜色为状态变量
②提取数字为状态变量
 */

// 我靠，他直接准备好了代码，但是我没有去找黑马拿资料
// 这里直接用我之前写的来顶替

/*综合案例一京东登录
模块拆分：
1.布局容器+顶部+Logo
2.输入框和登录区域
3.底部模块区域
 */

@Entry
@Component
struct Index {
  // 声明状态 颜色 点赞数
  @State myColor: string = "#7e7e7e"
  @State myCount: number = 6666

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
            Image($r("app.media.ic_heart"))
              .width(12)
              .fillColor(this.myColor)
            Text(this.myCount.toString())
              .fontSize(10)
              .fontColor(this.myColor)
          }
          //给这个row去注册点击事件
          .onClick(() => {
            // 修改点赞数
            this.myCount += 1
            // 修改颜色
            this.myColor = "#ff0000"
          })
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

