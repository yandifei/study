@Entry
@Component
struct Index {
  // 创建一个导航路由路径栈的实例(可以理解为1个路由界面)
  pathInfos: NavPathStack = new NavPathStack()
  @State message: string = '第一个界面，点击我';
  build() {
    Column() {
      // 创建路由导航(参数：需要跳转的界面)
      Navigation(this.pathInfos) {
        Column({space: 10}) {
          Text(this.message)
            .fontSize(16)
            .fontWeight(FontWeight.Bold)
          Button('跳转界面2')
            .onClick(() => {
              this.pathInfos.pushPathByName('第二个界面', '第二个界面的参数')})
        }
      }
      .width('100%')
      .mode(NavigationMode.Auto)
      .title('第一个界面')
    }
    .height('100%')
    .width('100%')
  }
}