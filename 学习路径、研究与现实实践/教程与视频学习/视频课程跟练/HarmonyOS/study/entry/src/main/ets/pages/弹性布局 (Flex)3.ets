/*案例练习
 */
@Entry
@Component
struct Index {
  build() {
    Column() {
      Text("阶段选择")
        .fontSize(30)
        .fontWeight(700)
        .padding(15)
        .width("100%")

      // 这里和视频里面一致都是用Flex容器组件(在控件需要换行对齐的情况下直接用Flex)
      Flex({
        wrap: FlexWrap.Wrap
      }) {
        Text("ArkUI").margin(5).padding(15).backgroundColor('#f1f1f1')
        Text("ArkTS").margin(5).padding(15).backgroundColor('#f1f1f1')
        Text("界面开发").margin(5).padding(15).backgroundColor('#f1f1f1')
        Text("系统能力").margin(5).padding(15).backgroundColor('#f1f1f1')
        Text("权限控制").margin(5).padding(15).backgroundColor('#f1f1f1')
        Text("元服务").margin(5).padding(15).backgroundColor('#f1f1f1')
      }
    }
  }
}