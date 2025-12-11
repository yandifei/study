@Entry
@Component
struct Index {
  @State message: string = 'My Video'
  // @State video: Resource = $rawfile('ihateai.mp4')
  @State video: string = 'https:\/\/vd3.bdstatic.com\/mda-pdc2kmwtd2vxhiy4\/cae_h264\/1681502407203843413\/mda-pdc2kmwtd2vxhiy4.mp4'
  controller: VideoController = new VideoController()
  build() {
    Row() {
      Column() {
        Text(this.message)
          .fontSize(40)
          .fontWeight(FontWeight.Bolder)
          .margin({bottom: 70})
        Video({
          src: this.video, currentProgressRate: 1, controller: this.controller
        }).height(300)
          .objectFit(ImageFit.Contain)
          .autoPlay(false)
          .controls(true)
          .onStart(() => {
            console.info('MediaDemo', "play video success")
          })
          .id("videoCard")
      }
      .width('100%')
    }
    .height('100%')
  }
}