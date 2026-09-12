/*线性布局
线性布局(LinearLayout)通过线性容器Column和Row创建。
Column容器：子元素垂直方向排列作
Row容器：子元素水平方向排列
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
      Text()
        .width(200).height(100)
        .backgroundColor(Color.Pink)
        .border({ width: 2 })
      Text()
        .width(200)
        .height(100)
        .backgroundColor(Color.Pink)
        .border({ width: 2 })
        .margin(5)
      Text()
        .width(200).height(100)
        .backgroundColor(Color.Pink)
        .border({ width: 2 })

    }
    .width("100%")
    .height("100%")
    .backgroundColor("#ccc")
    // 设置排布主方向的对齐方式（主轴）
    // 1. Start         （排布主方向）主轴起始位置对齐
    // 2. Center        主轴居中对齐
    // 3. End           主轴结束位置对齐
    // 4.SpaceBetween   贴边显示，中间的元素均匀分布间隙
    // 5.SpaceAround间隙环绕0.51110.5的间隙分布，靠边只有一半的间隙
    // 6.SpaceEvenly间隙均匀环绕，靠边也是完整的一份间隙
    // justifyContent(枚举FlexAlign) ctrl+p cmd+p

    // .justifyContent(FlexAlign.Center)
    // .justifyContent(FlexAlign.SpaceBetween)
    // .justifyContent(FlexAlign.SpaceAround)
    .justifyContent(FlexAlign.SpaceEvenly )

  }
}

