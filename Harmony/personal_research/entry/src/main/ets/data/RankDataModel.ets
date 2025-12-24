/*RankDataModel.ets
 *排行榜数据模型
 *https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=1&format=json
 */

// 排行接口根数据结构
export interface RankDataModel {
  contents: Contents[]; // 排行内容列表
}

// 单条作品数据
export interface Contents {
  title: string; // 作品标题
  date: string; // 发布日期（格式示例："2025年12月21日 05:13"）
  tags: string[]; // 作品标签列表
  url: string; // 作品封面图片 URL
  illust_type: string; // 作品类型（0=插画，1=漫画，2=动图，字符串形式）
  illust_book_style: string; // 漫画阅读样式（通常为 "0"）
  illust_page_count: string; // 作品页数（字符串形式）
  user_name: string; // 作者昵称
  profile_img: string; // 作者头像 URL
  // illust_content_type: IllustContentType; // 作品内容属性标记
  illust_series: boolean; // 是否属于系列作品（false 表示未归入系列）
  illust_id: number; // 作品 ID
  width: number; // 原图宽度（像素）
  height: number; // 原图高度（像素）
  user_id: number; // 作者用户 ID
  rank: number; // 当前排名
  yes_rank: number; // 昨日排名
  rating_count: number; // 点赞（评分）数量
  view_count: number; // 浏览次数
  illust_upload_timestamp: number; // 发布时间戳（秒）
  attr: string; // 额外属性字段（通常为空字符串）
  is_masked: boolean; // 是否被平台打码/限制显示
  is_bookmarked: boolean; // 当前用户是否已收藏
  bookmarkable: boolean; // 当前用户是否可以收藏
}

// // 作品内容类型 / 敏感内容标记
// export interface IllustContentType {
//   sexual: number; // sex内容等级（0=无，1=轻度，数值越高越敏感）
//   lo: boolean; // 是否涉及未成年人
//   grotesque: boolean; // 是否包含猎奇/血腥内容
//   violent: boolean; // 是否包含暴力内容
//   homosexual: boolean; // 是否包含同性内容
//   drug: boolean; // 是否涉及毒品
//   thoughts: boolean; // 是否包含思想/精神异常相关内容
//   antisocial: boolean; // 是否包含反社会内容
//   religion: boolean; // 是否涉及宗教敏感内容
//   original: boolean; // 是否为原创作品
//   furry: boolean; // 是否为兽人题材
//   bl: boolean; // 是否为 BL（男男）
//   yuri: boolean; // 是否为百合（女女）
// }

