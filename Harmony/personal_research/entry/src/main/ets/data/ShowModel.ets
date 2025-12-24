/*C.ets
 * 展示模型，需要展示的核心接口
 * 图片、排名、作者、图片名称
 */
export interface ShowModel {
  // 是否能展示（有些图片必须要登陆与年龄无关）
  can_show: boolean |  null;

  // 图片地址
  image_url: string |  null;

  // 排名
  rank: number;

  // 作者名称
  user_name: string;

  // 作品标题
  title: string;
}