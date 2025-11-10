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