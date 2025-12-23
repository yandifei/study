/*NextDataModel.ets
解析html
<script id="__NEXT_DATA__" type="application/json">
的内容，实际为json，目的是拿到排行的json接口的url(需要这里获取后拼接)
["props"]["pageProps"]["assign"]["contents"]
https://www.pixiv.net/ranking.php?mode=daily&content=illust
*/

// 【顶层json解析】
export interface NextDataModel{
  props: Props
}
// 【第一层解析】json->props->pageProps
export interface Props{
  pageProps: PageProps
}

// 【第二层解析】json->props->pageProps->assign
export interface PageProps{
  assign: Assign
}

// 【第一次url只是要拿到contents[]数量】json->props->pageProps->assign->contents
export interface Assign{
  contents: Contents[]
}

// 【第二次需要拿到illust_id去拼接字符串】json->props->pageProps->assign->contents->数据
export interface Contents {
  // 作品标题
  title: string;
  // 发布日期字符串 (例如: "2025年12月20日 00:29")
  date: string;
  // 标签列表
  tags: string[];
  // 预览图/缩略图链接地址
  url: string;
  // 插画类型 ("0": 插画, "1": 漫画, "2": 动图)
  illust_type: string;
  // 书籍样式 (用于区分单页或多页投稿)
  illust_book_style: string;
  // 作品包含的页面总数
  illust_page_count: string;
  // 作者用户名
  user_name: string;
  // 作者头像链接
  profile_img: string;
  // 是否属于某个插画系列
  illust_series: boolean;
  // 作品的唯一数字 ID
  illust_id: number;
  // 原始图片宽度 (像素)
  width: number;
  // 原始图片高度 (像素)
  height: number;
  // 作者的唯一用户 ID
  user_id: number;
  // 当前在排行榜中的名次 (1-50)
  rank: number;
  // 该作品在昨日排行榜中的名次
  yes_rank: number;
  // 综合评分/收藏计数统计
  rating_count: number;
  // 该作品的总浏览次数
  view_count: number;
  // 上传时间的时间戳 (秒级)
  illust_upload_timestamp: number;
  // 作品属性标签 (通常为空字符串或特定标识)
  attr: string;
  // 是否因为安全/屏蔽设置被隐藏
  is_masked: boolean;
  // 当前登录用户是否已收藏
  is_bookmarked: boolean;
  // 该作品是否开放收藏功能
  bookmarkable: boolean;
  // 收藏记录 ID (未收藏时为 null)
  bookmark_id: string | null;
  // 收藏限制 (如公开或私密，未收藏为 null)
  bookmark_illust_restrict: string | null;
  // // 作品内容详细分级对象 (包含 R18、AI 等判断)
  // illust_content_type: IllustContentType;
}
//
// // 【作品详细分级与内容判定接口】json->props->pageProps->assign->contents->illust_content_type->数据
// export interface IllustContentType {
//   // 是否为 R-18 (0:全年龄, 1:R-18)
//   sexual: 0 | 1;
//   // 是否涉及幼态
//   lo: boolean;
//   // 是否涉及血腥恐怖
//   grotesque: boolean;
//   // 是否包含暴力
//   violent: boolean;
//   // 是否涉及同性向
//   homosexual: boolean;
//   // 是否涉及药物
//   drug: boolean;
//   // 是否涉及特定思想
//   thoughts: boolean;
//   // 是否涉及反社会
//   antisocial: boolean;
//   // 是否涉及宗教
//   religion: boolean;
//   // 是否为原创作品
//   original: boolean;
//   // 是否为兽人 (Furry)
//   furry: boolean;
//   // 是否为 BL (Boys' Love)
//   bl: boolean;
//   // 是否为百合 (Yuri)
//   yuri: boolean;
// }
//
// // PixivResponse->body
// export interface PixivResponseBody {
//   // 使用 Record 工具类型代替索引签名
//   // 考虑到部分 ID 对应的值为 null，这里使用了 Illustration | null
//   illusts: Record<string, Illustration | null>;
//   novels: never[]; // 确保数组为空且类型安全
// }
// // PixivResponse->body->illusts 中的具体插画对象
// export interface Illustration {
//   id: string;                 // 插画ID
//   title: string;              // 插画标题
//   illustType: number;         // 插画类型 (0: 普通插画, 1: 动图等)
//   xRestrict: number;          // 年龄限制 (0: 无限制)
//   restrict: number;           // 限制级别
//   sl: number;                 // 未知参数
//   url: string;                // 插画缩略图URL
//   description: string;        // 插画描述
//   tags: string[];             // 标签列表
//   userId: string;             // 作者ID
//   userName: string;           // 作者名称
//   width: number;              // 图片宽度
//   height: number;             // 图片高度
//   pageCount: number;          // 页面数量/图片张数
//   isBookmarkable: boolean;    // 是否可以收藏
//   bookmarkData: null;         // 收藏数据 (目前总是为null)
//   alt: string;                // 替代文本描述
//   titleCaptionTranslation: TitleCaptionTranslation; // 标题和说明的翻译
//   createDate: string;         // 创建日期
//   updateDate: string;         // 更新日期
//   isUnlisted: boolean;        // 是否未列出
//   isMasked: boolean;          // 是否被屏蔽
//   aiType: number;             // AI生成类型 (1: 非AI生成)
//   visibilityScope: number;    // 可见范围
//   profileImageUrl: string;    // 作者头像URL
// }
//
// /**
//  * 标题与说明的翻译结构
//  */
// export interface TitleCaptionTranslation {
//   workTitle: string | null;    // 翻译后的作品标题
//   workCaption: string | null;  // 翻译后的作品说明
// }