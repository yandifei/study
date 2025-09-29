/*交互-点击事件
说明：组件被点击时触发的事件
作用：监听（感知）用户点击行为，进行对应操作
 */

@Entry
@Component
struct Index {
  build() {
    Row() {
      Column() {
        Button("点击我显示对话框")
          .onClick(() => {
            // console.log("消息", "你好点击事件")
            // 弹框
            AlertDialog.show({
              message: "你好~这是一个弹框"
            })
          })
        Text("我是文本")
          .onClick(() => {
            AlertDialog.show({
              message: "我是一个文本组件"
            })
          })
      }
      .width('100%')
    }
    .height('100%')
  }
}