@Entry
@Component
struct EnterExitDemo {
  @State flag: boolean = true;
  @State control: string = 'hide';
  build() {
    Column() {
      Button(this.control).width(80).height(30).margin(30)
        .onClick(() => {
          // 点击 Button 控制 Image 的显示和消失
          if (this.flag) {
            this.control = 'show';
          } else {
            this.control = 'hide';
          }
          this.flag = !this.flag;
        })
      if (this.flag) {
        Image($r('app.media.wukong')).width(200).height(200)
          .transition(TransitionEffect.OPACITY
            .animation({ duration: 2000, curve: Curve.Ease })
            .combine(TransitionEffect.rotate({ z: 1, angle: 180 }))
          )
      }
    }.width('100%')
  }
}