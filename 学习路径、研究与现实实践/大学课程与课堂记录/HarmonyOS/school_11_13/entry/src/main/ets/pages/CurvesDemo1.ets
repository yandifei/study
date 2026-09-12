class MyCurve {
  public title: string;
  public curve: Curve;
  public color: Color | string;
  public text: string;
  constructor(title: string, curve: Curve, color: Color | string = '', text: string) {
    this.title = title;
    this.curve = curve;
    this.color = color;
    this.text = text;
  }
}


const myCurves: MyCurve[] = [
  new MyCurve(' Linear', Curve.Linear, '#317AF7', '1'),
  new MyCurve(' Ease', Curve.Ease, '#D94838', '2'),
  new MyCurve(' EaseIn', Curve.EaseIn, '#DB6B42', '3'),
  new MyCurve(' EaseOut', Curve.EaseOut, '#5BA854', '4'),
  new MyCurve(' EaseInOut', Curve.EaseInOut, '#317AF7', '5'),
  new MyCurve(' FastOutSlowIn', Curve.FastOutSlowIn, '#D94838', '6'),
]

@Entry
@Component
export struct CurvesDemo1 {
  @State dRotate: number = 0; // 旋转角度
  build() {
    Column() {
      Stack() {
        // 摆动管道
        Row()
          .width(290)
          .height(290)
          .border({
            width: 15, color: 0xE6E8EB, radius: 145
          })
        // 曲线图例
        Grid() {
          ForEach(myCurves, (item: MyCurve) => {
            GridItem() {
              Column() {
                Text(item.text)
                  .width(30)
                  .height(30)
                  .borderRadius(15)
                  .backgroundColor(item.color)
                  .fontColor(Color.White)
                  .textAlign(TextAlign.Center)
                Text(item.title)
                  .fontSize(15)
                  .fontColor(0x909399)
              }
              .width('100%')
            }
          })
        }
        .columnsTemplate('1fr 1fr 1fr')
        .rowsTemplate('1fr 1fr 1fr 1fr 1fr')
        .padding(10)
        .width('100%')
        .height(300).margin({top:50})

        ForEach(myCurves, (item: MyCurve) => {
          // 小球
          Column() {
            Text(item.text)
              .width(30)
              .height(30)
              .borderRadius(15)
              .backgroundColor(item.color)
              .textAlign(TextAlign.Center)
              .fontColor(Color.White)
          }
          .width(20)
          .height(300)
          .rotate({ angle: this.dRotate })
          .animation({ duration: 2000, iterations: -1, curve: item.curve, delay: 100})})
      }
      .width('100%')
      .height(200)
      .margin(100)
      .onClick(() => {
        this.dRotate ? null : this.dRotate = 360;
      })
    }
    .width('100%')
  }
}