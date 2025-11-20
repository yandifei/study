import { router } from '@kit.ArkUI'

@Component
struct SonCom {
  aboutToAppear(): void {
    console.log('LifeCycle123', 'SonCom 调用 aboutToAppear 函数')
  }
  aboutToDisappear(): void {
    console.log('LifeCycle123', 'SonCom 调用 aboutToDisappear 函数')
  }
  build() {
    Column() {
      Text('我是子组件')
        .fontColor(Color.White)
        .fontSize(30)
    }
    .width(200)
    .height(200)
    .backgroundColor(Color.Blue)
    .border({ width: 3 })
  }
}

@Entry
@Component
struct Index {
  aboutToAppear(): void {
    console.log('LifeCycle123', 'Index Page 调用 aboutToAppear 函数')
  }
  aboutToDisappear(): void {
    console.log('LifeCycle123', 'Index Page 调用 aboutToDisAppear 函数')
  }
  onDidBuild(): void {
    console.log('LifeCycle123', 'Index Page 调用 onDidBuild');
  }

  // 只有被@Entry 装饰的组件才可以调用页面的生命周期
  onPageShow() {
    console.info('LifeCycle123', 'Index Page 调用 onPageShow 函数');
  }
  // 只有被@Entry 装饰的组件才可以调用页面的生命周期
  onPageHide() {
    console.info('LifeCycle123', 'Index Page 调用 onPageHide 函数');
  }
  // 只有被@Entry 装饰的组件才可以调用页面的生命周期
  onBackPress() {
    console.info('LifeCycle123', 'Index Page 调用 onBackPress 函数');
    return true // 返回 true 表示页面自己处理返回逻辑，不进行页面路由；返回false表示使用默认的路由返回逻辑，不设置返回值按照 false 处理
  }

  @State message: string = 'Hello World';

  @State show: boolean = true

  build() {
    RelativeContainer() {
      Text(this.message)
        .id('HelloWorld')
        .fontSize($r('app.float.page_text_font_size'))
        .fontWeight(FontWeight.Bold)
        .alignRules({
          center: { anchor: '__container__', align: VerticalAlign.Top },
          middle: { anchor: '__container__', align: HorizontalAlign.Center }
        })
        .onClick(() => {
          this.message = 'Welcome';
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
        SonCom()
          .id('SonCom')
          .margin(40)
          .alignRules({
            top: {anchor: 'ShowHide', align: VerticalAlign.Bottom}, middle: { anchor: 'HelloWorld', align: HorizontalAlign.Center }
          })
          .onAppear(() => {
            console.log('LifeCycle123', 'SonCom 调用 组件挂载显示')
          })
      }
      Button('跳转到页面二')
        .id('JumpToPage2')
        .margin({top: 20})
        .alignRules({
          top: { anchor: 'SonCom', align: VerticalAlign.Bottom}, middle: { anchor: 'SonCom', align: HorizontalAlign.Center }
        })
        .onClick(() => {
          router.pushUrl({url: 'pages/SecondPage'})
        })



    }
    .height('100%')
    .width('100%')


    .onAppear(() => {
      console.log('LifeCycle123', 'Index Page 调用 组件挂载显示')
    })
  }

}