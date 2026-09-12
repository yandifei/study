// 外部方法，
@Builder
export function PageOneBuilder(name: string, param: string) {
  // 外部组件UI导出(传递2个参数)
  PageOne({name: name, value: param})
}
@Component
export struct PageOne {
  pathInfos: NavPathStack = new NavPathStack()
  // 名字参数
  name: string = '';
  // 值的参数
  @State value: string = ''

  build() {
  NavDestination() {
    Column({space: 10}) {
      Text('Second Page')
        .width('100%')
        .fontSize(20)
      Text(`The param from previous page: ${this.value}`)
        .width('100%')
        .fontSize(20)
      Button('return')
        .width('40%')
        .height(40)
        .margin({top: 30})
        .onClick(() => {
          this.pathInfos.pop();
        })
    }
    .size({width: '100%', height: '100%'})
  }.title(`${this.name}`)
  .onReady((ctx: NavDestinationContext) => {
    this.pathInfos = ctx.pathStack
  })
}
}