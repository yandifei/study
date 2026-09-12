/*边框 border
作用：给组件添加边界，进行装饰美化
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
      Text("待完善")
        //配置边框
        .border({
          width: 1, //边框大小为1(必须配置边框大小)
          color: Color.Red, //颜色为红色
          //边框样式（Solid实线，Dotted点线，Dashed虚线）
          style:BorderStyle.Solid
        })
      /*颗粒控制，对边框不同的边配置不同的样式*/
      Text("单边框")
        // 单边框，可以通过left right bottom top配置四个方向边掴
        .border({
          width: { left: 1, right: 2, top: 3, bottom: 4},
          color: { left: Color.Red, right: Color.Green },
          style: {
            left: BorderStyle.Dashed,
            right: BorderStyle.Dashed

          }
        })
    }
    .width("100%")
    .padding(20)
  }
}

