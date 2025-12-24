import { HttpRequestOption, ImageKnifeComponent, ImageKnifeOption } from "@ohos/imageknife";

// import http from '@ohos.net.http';
// import type Context from '@ohos.app.ability.common';
//
// @Concurrent
// export async function customDownloadWithTimeout(
//   context: Context,
//   src: string | PixelMap | Resource,
//   headers?: Record<string, Object>,
//   httpOption?: HttpRequestOption // 有些版本会传这个参数；你不用也可以保留签名兼容
// ): Promise<ArrayBuffer | undefined> {
//   if (typeof src !== 'string') return undefined;
//
//   const httpRequest = http.createHttp();
//
//   // 1) 先准备基础 header（string 类型更稳）
//   const header: Record<string, string> = {
//     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
//     'Referer': 'https://www.pixiv.net',
//   };
//
//   // 2) 合并 ImageKnife 传进来的 headers（不用 for..in）
//   if (headers) {
//     const keys = Object.keys(headers);
//     for (let i = 0; i < keys.length; i++) {
//       const k = keys[i];
//       const v = headers[k];
//       header[k] = (v === undefined || v === null) ? '' : String(v);
//     }
//   }
//
//   const options: http.HttpRequestOptions = {
//     method: http.RequestMethod.GET,
//     connectTimeout: 10_000,
//     // readTimeout: 20_000,
//     header, // ✅ 这里放最终 header
//   };
//
//   try {
//     const res = await httpRequest.request(src, options);
//     if (res.responseCode === http.ResponseCode.OK) {
//       return res.result as ArrayBuffer;
//     }
//     throw new Error(`HTTP Code: ${res.responseCode}`);
//   } catch (e) {
//     // ArkTS 不允许 throw 任意类型：统一成 Error
//     const err = (e instanceof Error) ? e : new Error(String(e));
//     throw err;
//   } finally {
//     httpRequest.destroy();
//   }
// }


/*我自己的，没有受AI污染的*/
// 使用@Component装饰器定义一个UI组件，当作Image使用
@Component
export struct PixivImage {
  // 定义图片URL，使用@Prop装饰器表示这是从父组件传递过来的属性
  @Prop url: string;
  // 外部传入：cookie（可为空）
  @Prop cookie: string = "";
  // 图片没加载出来的占位图
  private static readonly placeholder_src = $r("app.media.pixiv");
  // 图片加载失败的占位图
  private static readonly errorholder_src = $r("app.media.pixiv");

  // 构造1个方法，为的是headerOption
  private makeOption(): ImageKnifeOption {
    // 创建一个ImageKnifeOption对象，用于传递给ImageKnifeComponent
    return {
      loadSrc: this.url || $r("app.media.pixiv"),
      placeholderSrc: PixivImage.placeholder_src,
      errorholderSrc: PixivImage.errorholder_src,
      headerOption: [
        // 用户代理（身份用我windows的chrome模拟）
        { key: "User-Agent", value: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36", },
        // 伪装请求来自合法来源（这个关键）
        { key: "Referer", value: "https://www.pixiv.net" },
        // cookie值
        { key: "Cookie", value: this.cookie ?? "" },
      ],
      // // 关键：使用自定义的、支持超时设置的下载函数
      // customGetImage: customDownloadWithTimeout,
      // 缩放策略
      objectFit: ImageFit.Auto,

    };
  }

  build() {
    ImageKnifeComponent({ imageKnifeOption: this.makeOption() }, )
      .width(100)
      .height(100)
  }
}

