/*状态管理
之前构建的页面多为静态界面。
但如果希望构建一个动态的、有交互的界面，就需要引入“状态”的概念
 点击交互触发了文本状态变更，状态变更引起了UI渲染

普通变量：只能在初始化时渲染，后续将不会再刷新。
状态变量：
需要装饰器装饰，改变会引起UI的渲染刷新
（必须设置类型和初始值）

注意点:
1，普通变量，只能在初始化时渲染，后续变化了，也不会引起更新
2，状态变量，被装饰器修饰，值的改变，会[自动]引起界面的刷新
 */

// 组件外的普通变量
let myName: string = "吕布"

@Entry
@Component
struct Index {
  // 组件内的普通变量 this.xxx
  myAge: number = 18

  // 组件内的状态变量 this.XXX
  @State myMsg: string = "hello yandifei"

  build() {
    Column() {
      // UI界面没有更新但是控制台有更新
      Text(myName).onClick(() => {
        myName = "貂蝉"
        console.log('myName', myName)
      })
      // UI界面没有更新但是控制台有更新
      Text(this.myAge.toString()).onClick(() => {
        this.myAge = 200
        console.log("myAge", this.myAge)
      })
      // 这个是组件内的状态变量（我的个人理解就是只有装饰器才有函数回调进行UI更新）
      Text(this.myMsg).onClick(() => {
        this.myMsg= "你好 状态"
      })
    }
  }
}

/*
 弹幕里面提到了这就是vue3的动态响应机制和非动态响应机制
 */