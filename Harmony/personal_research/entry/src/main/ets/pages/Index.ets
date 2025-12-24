import './login';
import { Requests } from '../logic/requests';
import { ShowModel } from '../data/ShowModel';
import { ImageKnife, ImageKnifeComponent, ImageKnifeOption } from '@ohos/imageknife';
import { RankItem } from '../view/components/RankItem';

// // 如果需要用文件缓存，需要提前初始化文件缓存
// ImageKnife.getInstance().initFileCache(context, 256, 256 * 1024 * 1024)
// 建议初始化为空数组 [] 而不是 null，这样可以省去很多非空判断
async function customDownload() {
  // 这里的 requests 建议使用本地实例
  let requests = new Requests()
  requests.r18 = true
  let show_model = await requests.get_show_model(requests.url)
  // // 赋值后，@State 会自动触发 build() 重新渲染
  // console.info(JSON.stringify(show_model))
  show_model.forEach((value: ShowModel) => {
    console.info("pixiv", value.image_url)
  })
}
// customDownload()

@Entry
@Component
struct Index {
  // 建议初始化为空数组 [] 而不是 null，这样可以省去很多非空判断
  @State show_model_arr: ShowModel[] = []
  private requests: Requests = new Requests()

  async aboutToAppear() {
    // 这里的 requests 建议使用本地实例,赋值后，@State 会自动触发 build() 重新渲染
    this.show_model_arr = await this.requests.get_show_model(this.requests.url)
    // console.info("pixiv", this.show_model_arr.length)
    // console.info(JSON.stringify(show_model))
  }


  build() {
    Column() {
      // Image(`https://webcnstatic.yostar.net/ba_cn_web/prod/upload/wallpaper/dTTcmJH0.jpeg`)
      //   .width('100%')
      //   .height(200)
      //   .objectFit(ImageFit.Contain)
      //   .backgroundColor(Color.Red)
      Button("切换为R18")
        .onClick(() => {
          // 切换r18状态
          this.requests.r18 = !this.requests.r18
          // 刷新网址
          console.info("pixiv", this.requests.url)

          // 刷新数据（真不想用页面启动的生命周期回调函数，但是再写一个异步函数除了浪费空间没有意义）
          this.aboutToAppear()
        })
      Button("切换为每日榜单")
        .onClick(() => {
          this.requests.url = this.requests.dailyUrl
          // 刷新数据（真不想用页面启动的生命周期回调函数，但是再写一个异步函数除了浪费空间没有意义）
          this.aboutToAppear()
        })
      Button("切换为每周榜单")
      .onClick(() => {
        this.requests.url = this.requests.weeklyUrl
        // 刷新数据（真不想用页面启动的生命周期回调函数，但是再写一个异步函数除了浪费空间没有意义）
        this.aboutToAppear()
      })
      Button("切换为每月榜单")
        .onClick(() => {
          this.requests.url = this.requests.monthlyUrl
          // 刷新数据
          this.aboutToAppear()
        })
      Button("切换为新人榜单")
        .onClick(() => {
          this.requests.url = this.requests.rookieUrl
          // 刷新数据
          this.aboutToAppear()
        })
      List() {
        // 异步循环渲染
        ForEach(this.show_model_arr, (show_model: ShowModel, index: number) => {
          // 自定义的单行排行榜列表
          RankItem({show_model: show_model}).width('100%').height("100");
        })
      }
      .width('100%')
      .height('100%')
    }
    .width('100%')
    .height('100%')
  }
}