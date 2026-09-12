import { router } from '@kit.ArkUI'
// import { router } from '@kit.ArkUI'
// import router from '@ohos.router'
@Entry
@Component
struct LoginPage {
  build() {
    Column() {
      Text('登录页')
        .fontSize(80)
      Button('登录到首页').onClick(() => {
        router.pushUrl({ url: 'pages/Index' })
      })
    }
  }
}