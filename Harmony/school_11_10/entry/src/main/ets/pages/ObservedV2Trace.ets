@ObservedV2
class Son {
  @Trace age: number = 100;
}
class Father {
  son: Son = new Son();
}
@Entry
@ComponentV2
struct Index {
  father: Father = new Father();
  build() {
    Column() {
      // 当点击改变 age 时，Text 组件会刷新
      Text(`${this.father.son.age}`)
        .onClick(() => {
          this.father.son.age++; // 第二层属性的变化
        })
    }
  }
}
