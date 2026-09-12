import { ImageKnife, ImageKnifeComponent, ImageKnifeOption } from '@ohos/imageknife'
// https://webcnstatic.yostar.net/ba_cn_web/prod/upload/wallpaper/dTTcmJH0.jpeg
// https://cdn-img.gitcode.com/de/ba/7315666de01ba46266833c478fd395f40b3f9d6827d06ea4f9ffbd26d463cdd1.png

@Entry
@Component
struct Index {
  @State imageKnifeOption: ImageKnifeOption = {
    loadSrc: 'https://cdn-img.gitcode.com/de/ba/7315666de01ba46266833c478fd395f40b3f9d6827d06ea4f9ffbd26d463cdd1.png',
    // placeholderSrc: $r('app.media.background'),
    // errorholderSrc: $r('app.media.background'),
    // 可选：如果你也配置了 headerOption，库通常会把它转换后传到 customDownload 的 headers 参数里
    headerOption: [{
      // 用户代理（身份用我windows的chrome模拟）
      key: "user-agent", value: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    }, {
      // 伪装请求来自合法来源（这个关键）
      key:"referer", value:  "https://www.pixiv.net"
    }],
    // customGetImage: customDownload,
    objectFit: ImageFit.Auto
  };

  build() {
    Column() {
      ImageKnifeComponent({ imageKnifeOption: this.imageKnifeOption })
        .width(200)
        .height(200);
    }
  }
}

// @Entry
// @Component
// struct PixivImageKnifeDemo {
//   build() {
//     Column() {
//       // ImageKnifeComponent({
//       //   imageKnifeOption: {
//       //     loadSrc:"https://cdn-img.gitcode.com/de/ba/7315666de01ba46266833c478fd395f40b3f9d6827d06ea4f9ffbd26d463cdd1.png",
//       //     placeholderSrc: $r("app.media.pixiv"),
//       //     errorholderSrc: $r("app.media.pixiv"),
//       //     objectFit: ImageFit.Auto
//       //   }
//       // }).width(100).height(100).backgroundColor(Color.Red)
//       // ImageKnifeComponent({
//       //   imageKnifeOption: {
//       //     loadSrc: $r("app.media.app_icon"),
//       //     placeholderSrc: $r("app.media.loading"),
//       //     errorholderSrc: $r("app.media.app_icon"),
//       //     objectFit: ImageFit.Auto
//       //   }
//       // }).width(100).height(100)
//
//     }
//   }
// }

// ImageKnifeComponent({
//   imageKnifeOption:{
//     loadSrc:"http//xx.xx",
//     customGetImage:custom
//   }
// })

// // 自定义实现图片获取方法，如自定义网络下载
// @Concurrent
// async function custom(context: Context, src: string | PixelMap | Resource): Promise<ArrayBuffer | undefined> {
//   console.info("ImageKnife::  custom download：" + src)
//   // 举例写死从本地文件读取，也可以自己请求网络图片
//   return context.resourceManager.getMediaContentSync($r("app.media.bb").id).buffer as ArrayBuffer
// }




// // 自定义下载方法
// @Concurrent
// async function custom(context: Context, src: string | PixelMap | Resource,headers?: Record<string,Object>): Promise<ArrayBuffer | undefined> {
//   return new Promise((resolve,reject)=>{
//     if (typeof src == "string") {
//       let session = GetSession.session
//       let req = new rcp.Request(src,"GET");
//       session.fetch(req).then((response)=>{
//         if(response.statusCode == 200) {
//           let buffer = response.body
//           resolve(buffer)
//         } else {
//           reject("rcp code:"+response.statusCode)
//         }
//       }).catch((err:BusinessError)=>{
//         reject("error rcp src:"+src+",err:"+JSON.stringify(err))
//       })
//     }
//   })
// }