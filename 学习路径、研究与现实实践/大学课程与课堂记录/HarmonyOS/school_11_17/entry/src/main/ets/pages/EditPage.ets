import { router } from '@kit.ArkUI';
@Entry
@Component
struct EditPage {
  @State message: string = '编辑页';
  build() {
    Row() {
      Column() {
        Text(this.message)
          .fontSize(50)
          .fontWeight(FontWeight.Bold)
        Button('跳转到详情页')
          .onClick(() => {
            router.pushUrl({
              url: 'pages/DetailPage' })
          })
        Button('获取页面栈长度')
          .onClick(() => {
            AlertDialog.show({
              message: router.getLength()
            })
          })
      }
      .width('100%')
    }
    .height('100%')
  }
}
