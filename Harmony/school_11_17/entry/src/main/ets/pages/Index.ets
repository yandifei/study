import { router } from '@kit.ArkUI';
@Entry
@Component
struct Index {
  build() {
    Column({space: 10}) {
      Text('首页')
        .fontSize(60)
      Button('去编辑页')
        .onClick(() => {
          router.pushUrl({
            url: 'pages/EditPage' })
        })
      Button('去详情页')
        .onClick(() => {
          router.pushUrl({
            url: 'pages/DetailPage' })
        })
    }
  }
}