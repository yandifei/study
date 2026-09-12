/*计数器案例
核心思路：
1.准备状态变量→
@State count:number =1
2.注册点击事件onClick
3.点击时，修改状态变量
4.状态变量变化，界面自动更新
 */



@Entry
@Component
struct Index {
  // 计数器变量
  @State num: number = 1
  build() {
    // 只要修改了状态变量，自动触发界面（视图）的更新
    Row() {
      Button("+").onClick((event: ClickEvent) => {
        this.num += 1
      })
      Text(this.num.toString()).margin(10)
      Button("-").onClick((event: ClickEvent) => {
        this.num -= 1
      })
    }
    .width("100%")
    .height("100%")
    // .justifyContent(FlexAlign.SpaceBetween)
    .padding(20)
  }
}

