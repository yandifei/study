/*自适 应伸缩
设置layoutWeight属性的子元素与兄弟元素，会按照权重进行分配主轴的空间
语法：.layoutWeight(数字）

这我可太熟了，被Qt控件全分辨率对齐折磨的日子就适应伸缩的累题
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
    Column({ space: 20}) {
      // LayoutWeight 自适应伸缩：按照[份数权重]，分配[剩余空间]
      Row() {
        Text("左侧")
          // 核心代码：自适应伸缩
          .layoutWeight(1)
          .backgroundColor(Color.Pink)
          .height(40)
        Text("右侧固定")
          .width(80)
          .height(40)
          .backgroundColor(Color.Orange)
      }
      .width(300)
      .height(40)
      .backgroundColor(Color.White)
      /*第二个案例
       实际上这里的写法我还是要吐槽的，既然算是权重分配为什么整在一起呢？
       控价这么多，每个控件单独调用layoutWeight方法，我怎么清晰知道所有控件的权重呢？
       就不能是{ 控件1: 1, 控件2: 2, 控件3: 1 }这种吗？
       或者是百分比分配也行呀！
       */
      Row() {
        Text("老大")
          .layoutWeight(1)
          .backgroundColor(Color.Gray)
          .height(40)
        Text("老二")
          .layoutWeight(2)
          .backgroundColor(Color.Orange)
          .height(40)
        Text("老三")
          .layoutWeight(1)
          .height(40)
          .backgroundColor(Color.Pink)
        Text("小宝")
          .width(50)
          .height(40)
          .backgroundColor(Color.Brown)
      }
      .width(300)
      .height(40)
      .backgroundColor(Color.White)


    }
    .padding(10)
    .width("100%")
    .height("100%")
    .backgroundColor("#ccc")
  }
}

