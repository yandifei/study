/*C.ets
 * 展示模型，需要展示的核心接口
 * 图片、排名、作者、图片名称
 */
export interface ShowModel{
  // 图片地址
  image_url:string;
  // 排名
  rank:number;
  // 作者
  author:string;
  // 图片名称
  image_name:string;
}