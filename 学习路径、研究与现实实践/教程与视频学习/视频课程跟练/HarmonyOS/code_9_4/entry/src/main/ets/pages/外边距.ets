/*布局元素的组成
组件区域 是最外层的“盒子”，定义了组件在页面中的占地面积。
组件内容区 在组件区域内部，专门用于放置内容。
组件内容 是你真正想展示的东西。
组件布局边界 则决定了组件与周围元素之间的间隔。

内边距padding
作用：在组件内添加间距，拉开内与组件边缘之间的距离

外边距margin
作用：在组件外添加间距，拉开两个组件之间的距离
 */

//去华为官网掏的logo
const huaweiLogo: string = "https://res-static.hc-cdn.cn/cloudbu-site/china/zh-cn/hdhomeportal/logonew.png"

//华为官方图标（svg矢量图）
// https://developer.huawei.com/consumer/cn/design/harmonyos-symbol/

@Entry
@Component
struct Index {
  @State message: string = "雁低飞";
  // 构建 -> 界面
  build() {
    Row() {
      Text("刘备")
        .backgroundColor(Color.Orange)
          //单个边距设置
        .margin({
          left: 30
        })
      Text("张飞")
        .backgroundColor(Color.Pink)
          // .margin(50) //一次性设置四个方向的margin外边距
          //单个边距设置
        .margin({
          left: 30
        })
      Text("关羽")
        .backgroundColor(Color.Green)
          //单个边距设置
        .margin({
          left: 30
        })

      Column() {
        //设置上下边距
        Text("刘备")
          .backgroundColor(Color.Orange)
            //单个边距设置
          .margin({
            top: 30
          })
        Text("张飞")
          .backgroundColor(Color.Pink)
            // .margin(50) //一次性设置四个方向的margin外边距
            //单个边距设置
          .margin({
            top: 30
          })
        Text("关羽")
          .backgroundColor(Color.Green)
            //单个边距设置
          .margin({
            top: 30
          })
      }
    }
  }
}