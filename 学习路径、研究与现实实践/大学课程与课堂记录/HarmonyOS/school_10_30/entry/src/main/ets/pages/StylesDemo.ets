// 1. 全局定义
@Styles function commonStyles () {
  .width(100)
  .height(100)
}

@Entry
@Component
struct StylesDemo {
  @State message: string = '@styles';
  @State bgColor: ResourceColor = Color.Blue
  build() {
    Column({ space: 10 }) {
      Text(this.message)
        .fontColor(Color.White)
        .width(100)
        .height(100)
        .backgroundColor(this.bgColor)
        .onClick(() => {
          this.bgColor = Color.Orange
        })
      Column() {}
      .width(100)
      .height(100)
      .backgroundColor(this.bgColor)
      .onClick(() => {
        this.bgColor = Color.Orange
      })
      Button('按钮')
        .width(100)
        .height(100)
        .backgroundColor(this.bgColor)
        .onClick(() => {
          this.bgColor = Color.Orange
        })
    }
    .width('100%')
    .height('100%')
  }
}