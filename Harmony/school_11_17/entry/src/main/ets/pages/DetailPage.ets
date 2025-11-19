import { router } from '@kit.ArkUI';
@Entry
@Component
struct DetailPage {
  @State message: string = '详情页';
  build() {
    Row() {
      Column({space: 10}) {
        Text(this.message)
          .fontSize(50)
          .fontWeight(FontWeight.Bold)
        Button('跳转到编辑页')
          .onClick(() => {
            router.pushUrl({
              url: 'pages/EditPage' })
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