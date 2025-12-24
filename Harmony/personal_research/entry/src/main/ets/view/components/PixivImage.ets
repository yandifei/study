import { ImageKnifeComponent, ImageKnifeOption } from "@ohos/imageknife";

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
      // 缩放策略
      objectFit: ImageFit.Auto,
    };
  }

  build() {
    ImageKnifeComponent({ imageKnifeOption: this.makeOption() })
      .width(100)
      .height(100);
  }
}

