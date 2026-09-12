@Entry
@Component
struct Parent {
  @State showChild: boolean = true;
  @State btnColor: string = '#FF007DFF';
  // 组件生命周期
  aboutToAppear() {
    console.info('Parent aboutToAppear');
  }
  // 组件生命周期
  onDidBuild() {
    console.info('Parent onDidBuild');
  }
  // 组件生命周期
  aboutToDisappear() {
    console.info('Parent aboutToDisappear');
  }
  build() {
    Column() {
      // this.showChild 为 true，创建 Child 子组件，执行 Child aboutToAppear
      if (this.showChild) {
        Child()
      }
      Button('delete Child')
        .margin(20)
        .backgroundColor(this.btnColor)
        .onClick(() => {
          // 更 改 this.showChild 为 false ， 删 除 Child 子组件，执行ChildaboutToDisappear
          // 更改 this.showChild 为 true，添加 Child 子组件，执行Child aboutToAppearthis.showChild = !this.showChild;
        })
    }
  }
}
@Component
struct Child {
  @State title: string = 'Hello World';
  // 组件生命周期
  aboutToDisappear() {
    console.info('Child aboutToDisappear');
  }
  // 组件生命周期
  onDidBuild() {
    console.info('Child onDidBuild');
  }
  // 组件生命周期
  aboutToAppear() {
    console.info('Child aboutToAppear');
  }
  build() {
    Text(this.title)
      .fontSize(50)
      .margin(20)
      .onClick(() => {
        this.title = 'Hello ArkUI';
      })
  }
}
