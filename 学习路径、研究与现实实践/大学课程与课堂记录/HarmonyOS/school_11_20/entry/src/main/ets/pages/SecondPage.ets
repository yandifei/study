import { router } from '@kit.ArkUI';

@Entry
@Component
struct SecondPage {
  @State message: string = '第二个页面';
  @State show: boolean = true
  // 只有被@Entry 装饰的组件才可以调用页面的生命周期
  onPageShow() {
    console.info('LifeCycle123', 'Second Page 调用 onPageShow 函数');
  }
  // 只有被@Entry 装饰的组件才可以调用页面的生命周期
  onPageHide() {
    console.info('LifeCycle123', 'Second Page 调用 onPageHide 函数');
  }
  // 只有被@Entry 装饰的组件才可以调用页面的生命周期
  onBackPress() {
    // router.back()
    console.info('LifeCycle123', 'Second Page 调用 onBackPress 函数');
    return true // 返回 true 表示页面自己处理返回逻辑，不进行页面路由；返回false表示使用默认的路由返回逻辑，不设置返回值按照 false 处理
  }
  aboutToAppear(): void {
    console.log('LifeCycle123', 'Second Page 调用 aboutToAppear 函数')
  }
  aboutToDisappear(): void {
    console.log('LifeCycle123', 'Second Page 调用 aboutToDisAppear 函数')
  }
  onDidBuild(): void {
    console.log('LifeCycle123', 'Second Page 调用 onDidBuild 函数')
  }
  build() {
    RelativeContainer() {
      Text(this.message)
        .id('HelloWorld')
        .fontSize(50)
        .fontWeight(FontWeight.Bold)
        .alignRules({
          center: { anchor: '__container__', align: VerticalAlign.Top }, middle: { anchor: '__container__', align: HorizontalAlign.Center }
        })
      Button('切换子组件显示')
        .id('ShowHide')
        .alignRules({
          top: { anchor: 'HelloWorld', align: VerticalAlign.Bottom}, middle: { anchor: 'HelloWorld', align: HorizontalAlign.Center }
        })
        .onClick(() => {
          this.show = !this.show
        })
      if(this.show) {
        SonCom2()
          .id('SonCom')
          .margin(40)
          .alignRules({
            top: {anchor: 'ShowHide', align: VerticalAlign.Bottom},
            middle: { anchor: 'HelloWorld', align: HorizontalAlign.Center }
          })
      }
      Button('返回到上一页')
        .id('BackToPage1')
        .margin({top: 20})
        .alignRules({
          top: { anchor: 'SonCom', align: VerticalAlign.Bottom}, middle: { anchor: 'SonCom', align: HorizontalAlign.Center }
        })
        .onClick(() => {
          router.back()
        })
    }
    .height('100%')
    .width('100%')
    .onAppear(() => {
      console.log('LifeCycle123', 'Second Page 调用 组件挂载显示')
    })
  }
}
@Component
struct SonCom2 {
  aboutToAppear(): void {
    console.log('LifeCycle123', '第二个页面 SonCom 调用 aboutToAppear 函数')
  }
  aboutToDisappear(): void {
    console.log('LifeCycle123', '第二个页面 SonCom 调用 aboutToDisappear 函数')
  }
  onDidBuild(): void {
    console.log('LifeCycle123', '第二个页面 SonCom 调用 onDidBuild 函数')
  }
  build() {
    Column() {
      Text('我是第二个页面子组件')
        .fontColor(Color.White)
        .fontSize(30)
    }
    .width(200)
    .height(200)
    .backgroundColor(Color.Pink)
    .border({ width: 3 })
    .onAppear(() => {
      console.log('LifeCycle123', '第二个页面 SonCom 调用组件挂载显示')
    })
  }
}
