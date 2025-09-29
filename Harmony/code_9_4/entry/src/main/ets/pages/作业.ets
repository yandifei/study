@Entry
@Component
struct Index {
  @State message: string = "你好，雁低飞";

  build() {
    RelativeContainer() {
      Text(this.message)
        .id('HelloWorld')
        .fontSize($r('app.float.page_text_font_size'))
        .fontWeight(FontWeight.Bold)
        .alignRules({
          center: { anchor: '__container__', align: VerticalAlign.Center },
          middle: { anchor: '__container__', align: HorizontalAlign.Center }
        })
        .onClick(() => {
          this.message = "欢迎使用HarmonyOS 5.0.5(17)系统";
        })
      Button("登陆使用")
        .width("100%")
        .onClick(() => {
          if (this.message==="新用户") {
            this.message = "雁低飞";
          } else {
            this.message==="新用户"
          }
        })

    }
    .height('100%')
    .width('100%')
  }
}