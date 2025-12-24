import { http } from '@kit.NetworkKit';
import { ShowModel } from '../data/ShowModel';
import { Contents, RankDataModel } from '../data/RankDataModel';
import { IllustDetailResponse } from '../data/IllustDetailResponse';

/*有坑
 * 如果实例了这个类然后修改属性是无法修改其他url的属性
 * 所以必须设置set、get方法来实现访问和修改才能同步url
 */


// 请求类（封装get、post）
export class Requests {
  // 是否r18(r18必须加cookies)
  private _r18: boolean = false;

  public set r18(value: boolean) {
    this._r18 = value;
  }

  public get r18(): boolean {
    return this._r18;
  }

  // 页数，1页有50张图
  private _page: number = 1;

  public set page(value: number) {
    this._page = value;
  }

  public get page(): number {
    return this._page;
  }

  // 请求使用的url（默认每日）
  private _url: string = `https://www.pixiv.net/ranking.php?mode=daily${this._r18 ? "_r18" : ""}&content=illust&p=${this._page}&format=json`;

  public set url(value: string) {
    this._url = value;
  }

  public get url(): string {
    return this._url;
  }

  // 本日排行
  private _dailyUrl: string = `https://www.pixiv.net/ranking.php?mode=daily${this._r18 ? "_r18" : ""}&content=illust&p=${this._page}&format=json`;

  public set dailyUrl(value: string) {
    this._dailyUrl = value;
  }

  public get dailyUrl(): string {
    return this._dailyUrl;
  }

  // 本周排行
  private _weeklyUrl: string = `https://www.pixiv.net/ranking.php?mode=weekly${this._r18 ? "_r18" : ""}&content=illust&p=${this._page}&format=json`;

  public set weeklyUrl(value: string) {
    this._weeklyUrl = value;
  }

  public get weeklyUrl(): string {
    return this._weeklyUrl;
  }

  // 本月排行
  private _monthlyUrl: string = `https://www.pixiv.net/ranking.php?mode=monthly${this._r18 ? "_r18" : ""}&content=illust&p=${this._page}&format=json`;

  public set monthlyUrl(value: string) {
    this._monthlyUrl = value;
  }

  public get monthlyUrl(): string {
    return this._monthlyUrl;
  }

  // 新人排行
  private _rookieUrl: string = `https://www.pixiv.net/ranking.php?mode=rookie${this._r18 ? "_r18" : ""}&content=illust&p=${this._page}&format=json`;

  public set rookieUrl(value: string) {
    this._rookieUrl = value;
  }

  public get rookieUrl(): string {
    return this._rookieUrl;
  }

  // cookie
  private _cookie: string = "";

  public set cookie(value: string) {
    this._cookie = value;
  }

  public get cookie(): string {
    return this._cookie;
  }

  get(url: string): Promise<http.HttpResponse> {
    /**
     * url:pixiv网址
     * 返回响应对象
     */
    const request = http.createHttp(); // 每次请求一个实例

    return request.request(
      url, // 请求URL
      {
        method: http.RequestMethod.GET, // 请求方法：GET
        header: {
          // 请求头（模拟浏览器请求，我这里就极致参数，其他默认）
          // 用户代理（身份用我windows的chrome模拟）
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
          // 伪装请求来自合法来源（这个关键）
          "referer": "https://www.pixiv.net",
          // 添加cookies，模拟登录
          "cookie": this._cookie,
        }
      },
    ).finally(() => {
      request.destroy();
    }); // 请求结束，销毁实例
  }

  // 异步请求获取UI模型对象
  async get_show_model(url: string): Promise<ShowModel[]> {
    // 存放UI作品对象
    let show_model_arr: ShowModel[] = []
    // // 创建UI模型对象
    // let show_model: ShowModel
    // 创建请求实例
    // const requests = new Requests();
    const requests = this;
    try {
      // 发送请求
      let respond = await requests.get(url);
      // 解析单页JSON数据（排行榜），拿到所有插画内容对象
      const rank_data: RankDataModel = JSON.parse(respond.result.toString());
      console.info("pixiv", `共解析了${rank_data.contents.length}个插画内容对象`);

      // 遍历对象保存UI需要的数据，使用map创建一个包含50个Promise的数组
      const tasks = rank_data.contents.map(async (content: Contents) => {
        // 确保每个小任务内部是完成的
        await requests.get(`https://www.pixiv.net/ajax/illust/${content.illust_id}/pages?lang=zh`)
          .then((res) => {
            // 解析json成对象模型
            const illuset_detail_response: IllustDetailResponse = JSON.parse(res.result.toString());
            // console.log("pixiv", `原图地址：${illuset_detail_response.body[0].urls.original}`)
            // 添加数据
            show_model_arr.push({
              can_show: null,
              image_url: illuset_detail_response.body[0]!.urls.original, // 图片url
              rank: content.rank, // 排行
              user_name: content.user_name, // 作者
              title: content.title, // 图片名称
            });
          }
          )
      });
      // 让整个函数停在这里，直到 50 个请求全部完成
      await Promise.all(tasks);
      // console.debug("pixiv", JSON.stringify(show_model_arr)) // 打印整个UI模型数组
      // 对数组进行排序，因为是异步的，所以可能rank不是从1开始，所以要排序
      show_model_arr.sort((a: ShowModel, b: ShowModel) => a.rank - b.rank);
    } catch (e) {
      // Promise reject、网络错误、超时、2300023 等
      console.error("请求异常:", JSON.stringify(e));
    }
    // 最后都得返回模型数组（请求失败就是空了）
    return show_model_arr;
  }

  // 校验UI模型图片是否有效
  async check_show_model(show_model: ShowModel[]): Promise<ShowModel[]> {
    // 创建请求实例
    // const requests = new Requests();
    const requests = this;
    const tasks = show_model.map(async (item: ShowModel) => {
      await requests.get(item.image_url!).then(
        (res) => {
          // 响应成功
          if (res.responseCode == 200) {
            item.can_show = true;
          } else {
            item.can_show = false;
          }
        }
      )
    });
    // 等待任务完成
    await Promise.all(tasks);
    // 返回模型数组
    return show_model;
  }
}


// let requests = new Requests()
// requests.get_show_model(requests.url).then(
//   (show_model_arr) => {
//     // 图片有效校验
//     requests.check_show_model(show_model_arr)
//     // console.debug("pixiv", JSON.stringify(show_model_arr)) // 打印整个UI模型数组
//     // for(let item of show_model_arr) {
//     //   console.debug("pixiv", `是否有效：${item.can_show}`,`图片排名：${item.rank}，图片名称：${item.title}，图片地址：${item.image_url}，作者名称：${item.user_name}`);
//     // }
//   }
// )


// async function startProcess() {
//   const data = await requests.get_show_model(requests.url);
//   requests.check_show_model(data);
// }
// startProcess()


// get_show_model(url).then(
//   () => {
//     console.debug("pixiv", JSON.stringify(show_model_arr)) // 打印整个UI模型数组
//   }
// )
// console.debug("pixiv", JSON.stringify(show_model_arr)) // 打印整个UI模型数组

// let url: string = `https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=1&format=json`
//
// get_show_model(url).then(
//   (show_model_arr) => {
//     // console.debug("pixiv", JSON.stringify(show_model_arr)) // 打印整个UI模型数组
//     for(let item of show_model_arr) {
//       console.debug("pixiv", `图片排名：${item.rank}，图片名称：${item.title}，图片地址：${item.image_url}，作者名称：${item.user_name}`);
//     }
//   }
// )

