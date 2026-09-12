// Second.ets
@Entry
@Component
struct Second {
  @State message: string = '同学，欢迎你'
  build() {
  Row() {
    Column() {
      Text(this.message)
        .fontSize(50)
        .fontWeight(FontWeight.Bold)
      Button() {
        Text('Back')
          .fontSize(25)
          .fontWeight(FontWeight.Bold)
      }
      .type(ButtonType.Capsule)
      .margin({
        top: 20
      })
      .backgroundColor('#0D9FFB')
      .width('40%')
      .height('5%')
    }
    .width('100%')
  }
  .height('100%')
}
}