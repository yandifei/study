/* 61-条件渲染&京东加购案例.ets
条件渲染
条件渲染：使用if、else和elseif，可基于不同状态渲染对应不同UI内容。
*/


@Entry
@Component
struct Index {
  @State age: number = 10
  build() {
    //条件渲染：不同的条件，控制不同的UI界面展示
    Column() {
      if (this.age < 18) {
        Text("未成年，18岁以下")
      }
      else if (this.age < 60) {
        Text("成年人，18~60岁")
      }
      else {
        Text("老年人，60+")
      }
      Button("长大").onClick(() => {
        this.age += 5
      })
      Text(`当前年龄：${this.age}`)
    }
  }
}