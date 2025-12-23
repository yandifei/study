/*
 * IllustDetailResponse
 * https://www.pixiv.net/ajax/illust/{作品id}?lang=zh
 * 获取作品详情，从NextDataMode拿到作品id
 */
export interface IllustDetailResponse {
  // error: boolean;
  // message: string;
  body: body;
}
export interface body {
  // 作品id
  id: string;
  // 图片地址
  urls: urls;
}

// 图片地址（这才是最终提取的）
export interface urls {
  // 超小方形预览图 (48x48)
  mini: string;
  // 方形缩略图 (250x250)
  thumb: string;
  // 小尺寸预览图
  small: string;
  // 常规尺寸展示图
  regular: string;
  // 原始尺寸原图（无压缩）
  original: string;
}

