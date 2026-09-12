@Component
struct Header {
  build() {
    Row() {
      Text('头部区域').fontColor(Color.White)
    }.width('100%')
    .height(60)
    .backgroundColor(Color.Green)
  }
}

@Component
struct ContentPiece {
  @State count: number = 0
  build() {
    Row({space: 20}) {
      Text(this.count.toString())
      Button('Click Me').onClick(() => {
        this.count++
      })
    }.width('100%')
    .height(30)
    .justifyContent(FlexAlign.Center)
  }
}

@Component
struct ContentInfo {
  build() {
    Column({space: 10}) {
      ContentPiece()
      ContentPiece()
      ContentPiece()
    }.width('100%')
    .height(400)
    .layoutWeight(1)
    .justifyContent(FlexAlign.Center)
    .backgroundColor(Color.Pink)
  }
}

@Component
struct Footer {
  build() {
    Row() {
      Text('底部区域').fontColor(Color.White)
    }.width('100%')
    .height(60)
    .backgroundColor(Color.Blue)
  }
}

@Entry
@Component
struct CompDemo1 {
  build() {
    Column() {
      Header()
      ContentInfo()
    }
  }
}