@Entry
@Component
struct Index {
  @State message: string = 'Hello World';

  // 控件复用，包括控件的样式也能复用
  @Builder
  indicatorBuilder() {
    Image($r("app.media.arisu"))  // 构建一个星星图标
      .width(200)
  }

  // 控件动态变量
  @State heightValue: number = 50;
  // 样式复用
  @Styles
  fancy() {
    .height(this.heightValue)
    .backgroundColor(Color.Blue)
    // 点击回调事件
    .onClick(() => {
      // if (this.heightValue == 50) {
      //     this.heightValue = 100
      // } else {
      //   this.heightValue = 50
      // }
      // 改成三目运算符
      this.heightValue == 50 ? this.heightValue = 100 : this.heightValue = 50
    })
  }


  build() {
    Column() {
      Text(this.message)
        .onClick(() => {
          this.message = 'Welcome'
        })
        // .backgroundImage()
      // 或者直接调用
      this.indicatorBuilder()
      // 或者直接调用
      this.indicatorBuilder()

      // 样式复用
      Button('change height')
        .fancy() // 自定义样式

    }
    .height('100%')
    .width('100%')
  }
}