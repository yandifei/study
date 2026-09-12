@ObservedV2
class Person {
  id: number = 0;
  @Trace age: number = 8;
}
@Entry
@ComponentV2
struct Index {
  person: Person = new Person();
  build() {
    Column() {
      // age 被@Trace 装饰，用在 UI 中可以触发 UI 刷新
      Text(`${this.person.age}`)
        .onClick(() => {
          this.person.age++; // 点击会触发 UI 刷新
        })
      // id 未被@Trace 装饰，用在 UI 中不会触发 UI 刷新
      Text(`${this.person.id}`) // 当 id 变化时不会刷新
        .onClick(() => {
          this.person.id++; // 点击不会触发 UI 刷新
        })
    }
  }
}