@ObservedV2
class Father {
  @Trace name: string = "Tom";
}
class Son extends Father {
}
@Entry
@ComponentV2
struct Index {
  son: Son = new Son();
  build() {
    Column() {
      // 当点击改变 name 时，Text 组件会刷新
      Text(`${this.son.name}`)
        .onClick(() => {
          this.son.name = "Jack";
        })
    }
  }
}