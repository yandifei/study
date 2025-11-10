@Extend(Text)
function bannerItem (bgColor: ResourceColor, msg: string) {
  .textAlign(TextAlign.Center)
  .backgroundColor(bgColor)
  .fontColor(Color.White)
  .fontSize(30)
  .onClick(() => {
    AlertDialog.show({
      message: msg
    })
  })
}

@Extend(Text)
function textFn () {
  .fontSize(20)
  .fontWeight(FontWeight.Bold)
  .margin({top: 20, bottom: 20})
}

@Entry
@Component
struct ExtendDemo {
  @State message: string = '@Extend-扩展组件(样式,事件)';
  build() {
    Column() {
      Text(this.message)
        .textFn()
      Swiper() {
        Text('1')
          .bannerItem(Color.Orange, '轮播图 1 号')
        Text('2')
          .bannerItem(Color.Brown, '轮播图 2 号')
        Text('3')
          .bannerItem(Color.Green, '轮播图 3 号')
      }
      .width('100%')
      .height(160)
    }
    .width('100%')
    .height('100%')
  }
}