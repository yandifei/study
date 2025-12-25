import './login';
import { Requests } from '../logic/requests';
import { ShowModel } from '../data/ShowModel';
import { ImageKnife, ImageKnifeComponent, ImageKnifeOption } from '@ohos/imageknife';
import { RankItem } from '../view/components/RankItem';
import { PixivImage } from '../view/components/PixivImage';

// // 如果需要用文件缓存，需要提前初始化文件缓存
// ImageKnife.getInstance().initFileCache(context, 256, 256 * 1024 * 1024)
// 初始化UI资源数组
async function initShowModelArr() {
  // 使用本地实例requests
  const requests = new Requests()
  let show_model_arr: ShowModel[] = await requests.get_show_model(requests.url)
  // // 赋值后，@State 会自动触发 build() 重新渲染
  // console.info(JSON.stringify(show_model))
  // show_model_arr.forEach((value: ShowModel) => {
  //   console.info("pixiv", value.image_url)
  // })
  return show_model_arr
}

// 加载中的渲染兜底
const PLACEHOLDER_SHOW: ShowModel = {
  rank: 0,
  title: '加载中...',
  image_url: '',
  // 其他字段按你 ShowModel 实际结构补齐
} as ShowModel

@Entry
@Component
struct Index {
  // 建议初始化为空数组 [] 而不是 null，这样可以省去很多非空判断
  @State show_model_arr: ShowModel[] = []
  @State is_show_img: boolean = false
  @State img_index: number = 0
  private requests: Requests = new Requests()

  async updateRequests() {
    // 重启请求url
    this.show_model_arr = await this.requests.get_show_model(this.requests.url)
  }
  async aboutToAppear() {
    // // 这里的 requests 建议使用本地实例,赋值后，@State 会自动触发 build() 重新渲染
    // this.show_model_arr = await this.requests.get_show_model(this.requests.url)
    this.show_model_arr = await initShowModelArr()
    // console.info("pixiv", this.show_model_arr.length)
    // console.info(JSON.stringify(show_model))
  }

  build() {
    Stack() {
      if (!this.is_show_img) {
        Column() {
          // Image(`https://webcnstatic.yostar.net/ba_cn_web/prod/upload/wallpaper/dTTcmJH0.jpeg`)
          //   .width('100%')
          //   .height(200)
          //   .objectFit(ImageFit.Contain)
          //   .backgroundColor(Color.Red)
          // Button("切换为R18")
          //   .onClick(() => {
          //     // 切换r18状态
          //     if (this.requests.r18) {
          //       this.requests.update_requests(1,false)
          //     } else {
          //       this.requests.update_requests(1,true)
          //     }
          //     // 刷新网址
          //     console.info("pixiv", this.requests.url, this.requests.r18)
          //     // // 刷新数据（真不想用页面启动的生命周期回调函数，但是再写一个异步函数除了浪费空间没有意义）
          //     // this.aboutToAppear()
          //     this.updateRequests()
          //   })
          Select([{ value: '每日榜单'},{ value: '每周榜单'},{ value: '每月榜单'},{ value: '新人榜单'}])
            .selected(0)
            .value("榜单类型")
              // .font({ size: 16, weight: 500 })
              // .fontColor('#182431')
              // .selectedOptionFont({ size: 16, weight: 400 })
              // .optionFont({ size: 16, weight: 400 })
              // .space(10)
              // .arrowPosition(ArrowPosition.END)
              // .menuAlign(MenuAlignType.START, { dx: 0, dy: 0 })
              // .optionWidth(200)
              // .optionHeight(300)
            .onSelect((index: number) => {
              // 刷新url
              switch (index) {
                case 0:
                  this.requests.url = this.requests.dailyUrl
                  break;
                case 1:
                  this.requests.url = this.requests.weeklyUrl
                  break;
                case 2:
                  this.requests.url = this.requests.monthlyUrl
                  break;
                case 3:
                  this.requests.url = this.requests.rookieUrl
                  break;
              }
              // 刷新控件
              this.updateRequests()
            })
          // Button("切换为每日榜单")
          //   .onClick(() => {
          //     this.requests.url = this.requests.dailyUrl
          //     // // 刷新数据（真不想用页面启动的生命周期回调函数，但是再写一个异步函数除了浪费空间没有意义）
          //     // this.aboutToAppear()
          //
          //   })
          // Button("切换为每周榜单")
          // .onClick(() => {
          //   this.requests.url = this.requests.weeklyUrl
          //   // // 刷新数据（真不想用页面启动的生命周期回调函数，但是再写一个异步函数除了浪费空间没有意义）
          //   // this.aboutToAppear()
          //   this.updateRequests()
          // })
          // Button("切换为每月榜单")
          //   .onClick(() => {
          //     this.requests.url = this.requests.monthlyUrl
          //     // // 刷新数据（真不想用页面启动的生命周期回调函数，但是再写一个异步函数除了浪费空间没有意义）
          //     // this.aboutToAppear()
          //     this.updateRequests()
          //
          //   })
          // Button("切换为新人榜单")
          //   .onClick(() => {
          //     this.requests.url = this.requests.rookieUrl
          //     // // 刷新数据（真不想用页面启动的生命周期回调函数，但是再写一个异步函数除了浪费空间没有意义）
          //     // this.aboutToAppear()
          //     this.updateRequests()
          //   })
          // // 异步渲染（等待数据加载完毕）
          // ForEach( this.show_model_arr, (show_model: ShowModel, index: number) => {
          //   // 自定义的单行排行榜列表
          //   RankItem({show_model: this.show_model_arr[0]}).width('100%').height("100");
          // })
          // List() {
          // RankItem({ show_model: this.show_model_arr[0] ?? PLACEHOLDER_SHOW })
          //   .width('100%')
          // }


          List() {
            // 异步循环渲染
            ForEach(this.show_model_arr, (show_model: ShowModel, index: number) => {
              // 自定义的单行排行榜列表
              RankItem({show_model: show_model})
                .width('100%').height("100")
                .id(index.toString())
                .onClick(() => {
                  this.is_show_img = !this.is_show_img
                  this.img_index = index
                })
            })

          }
          .width('100%')
          .height('100%')
          .onScrollIndex(async (start, end) => {
            console.info("pixiv", start, end, `列表：${start} - ${end}`)
            // // 触发刷新
            // if (start >= this.show_model_arr[-1].rank - 15) {
            //   // 更新网络请求url（下一页的url）
            //   this.requests.refreshUrls(Math.ceil(this.show_model_arr[-1].rank / 50) + 1, false)
            //   console.info("pixiv", this.requests.url)
            //   // 补充列表数据(下一页)
            //   this.show_model_arr.push(...await this.requests.get_show_model(this.requests.url))
            // }
            console.info("pixiv", this.show_model_arr.length, start, end)
            // 触发刷新
            if (end >= this.show_model_arr.length - 1) {
              this.requests.refreshUrls(Math.ceil(this.show_model_arr.length / 50) + 1, false)
              console.info("pixiv", this.requests.url)
              // 补充列表数据(下一页)
              this.show_model_arr.push(...await this.requests.get_show_model(this.requests.url))
            }
          })
        }
        .width('100%')
        .height('100%')
      }
      else {
        Column() {
          PixivImage({ url: this.show_model_arr[this.img_index].image_url ?? "" })
        }
        .width('100%')
        .height('100%')
        .onClick(() => {
          this.is_show_img = !this.is_show_img
        })
      }
    }
      .width('100%')
      .height('100%')
      .backgroundColor(Color.White)

  }
}