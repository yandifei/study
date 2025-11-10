@ObservedV2
class Manager {
  @Trace static count: number = 1;
}
@Entry
@ComponentV2
struct Index {
  build() {
    Column() {
      // 当点击改变 count 时，Text 组件会刷新
      Text(`${Manager.count}`)
        .onClick(() => {
          Manager.count++;
        })
    }
  }
}