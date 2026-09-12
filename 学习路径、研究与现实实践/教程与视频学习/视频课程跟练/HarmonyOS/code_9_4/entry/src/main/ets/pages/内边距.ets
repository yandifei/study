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
    Column() {
      Text("小龙女")
        .backgroundColor(Color.Pink)
          // .padding(20) //四个方向同时设置内边距
          //内边距颗粒度控制
        .padding({
          left: 20,
          top: 30,
          right: 5,
          bottom:30
        })
    }
  }
}