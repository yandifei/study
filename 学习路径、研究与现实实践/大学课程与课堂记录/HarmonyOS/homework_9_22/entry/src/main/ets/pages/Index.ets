@Entry
@Component
struct Index {
  @State message: string = "雁低飞，欢迎你";

  build() {
    Column() {
      Text(this.message)
        .id('HelloWorld')
        .fontSize($r('app.float.page_text_font_size'))
        .fontWeight(FontWeight.Bold)
        .alignRules({
          center: { anchor: '__container__', align: VerticalAlign.Center },
          middle: { anchor: '__container__', align: HorizontalAlign.Center }
        })
        .onClick(() => {
          this.message = 'Welcome';
        })
      Button("Back")
        .width("50%") // 按钮大小
        .margin(10) // 外边距
        .fontSize(40) //字体大小
        .backgroundColor(Color.Red) //按钮背景色
    }
    .height('100%')
    .width('100%')
    .justifyContent(FlexAlign.Center)
  }
}