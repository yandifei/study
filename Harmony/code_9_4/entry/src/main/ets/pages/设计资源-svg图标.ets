/*设计资源-svg图标
需求：界面中展示的图标->可以使用svg图标(任意放大缩小不失真，可以改变颜色)
使用方式：
1.设计师提供：基于项目设计的图标，拷贝到项目目录中使用
2.图标库中选取:找到合适的图标资源->下载(svg)->拷贝使用
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
    //Column参数传入对象，使用的space是控件(组件)之间的空格
    Column({ space: 15 }) {
      Image($r("app.media.ic_setting"))
        .width(200) //不失真
        .fillColor(Color.Red) //只有svg矢量图才能够修改颜色
      Image($r("app.media.ic_airplane_fill"))
        .width(50)
      //这个项目自带的图标（默认就有的图标）
      Image($r("app.media.startIcon"))
        .width(50)
    }
  }
}