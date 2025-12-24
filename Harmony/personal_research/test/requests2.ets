import { http } from '@kit.NetworkKit';
import { ShowModel } from '../entry/src/main/ets/data/ShowModel';
import { RankDataModel } from '../entry/src/main/ets/data/RankDataModel';
import { IllustDetailResponse } from '../entry/src/main/ets/data/IllustDetailResponse';


export class Requests {
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
          "referer": "https://www.pixiv.net"
        }
      },
    ).finally(() => { request.destroy();}); // 请求结束，销毁实例
  }
}

// 是否r18(r18必须加cookies)
let r18: boolean = false;
// 页数，1页有50张图
let page: number = 1

// 本日排行
const  url: string = `https://www.pixiv.net/ranking.php?mode=daily${r18 ? "_r18" : ""}&content=illust&p=${page}&format=json`
// 本周排行
// const weeklyUrl: string = `https://www.pixiv.net/ranking.php?mode=weekly${r18 ? "_r18" : ""}&content=illust&p=${page}&format=json`
// 本月排行
// const monthlyUrl: string = `https://www.pixiv.net/ranking.php?mode=monthly${r18 ? "_r18" : ""}&content=illust&p=${page}&format=json`
// 新人排行
// const rookieUrl: string = `https://www.pixiv.net/ranking.php?mode=rookie${r18 ? "_r18" : ""}&content=illust&p=${page}&format=json`

// 存放UI作品对象
let show_model_arr: ShowModel[] = []
// 异步函数
async function get_show_model(url: string){
  // 创建请求实例
  const requests = new Requests();
  try {
    // 发送请求
    let respond = await requests.get(url);
    // 解析单页JSON数据（排行榜），拿到所有插画内容对象
    const rank_data: RankDataModel = JSON.parse(respond.result.toString());
    // console.log("pixiv", `共解析了${rank_data.contents.length}个插画内容对象`);

    // 遍历对象
    // rank_data.contents.forEach((content: IllustContent, index: number) => {
    //   console.log(`第 ${index + 1} 项: ${content.title}`);
    // });

    for (const content of rank_data.contents) {
      console.info("pixiv", `解析的url:https://www.pixiv.net/ajax/illust/${content.illust_id}/pages?lang=zh`)
      // json请求，原图的url在里面
      let respond = await requests.get(`https://www.pixiv.net/ajax/illust/${content.illust_id}/pages?lang=zh`)
      // console.log("pivix", respond.result.toString()) // 查看json返回结果
      // 解析json成对象模型
      const illuset_detail_response: IllustDetailResponse = JSON.parse(respond.result.toString());
      // console.log("pixiv", `原图地址：${illuset_detail_response.body[0].urls.original}`)
      // //添加展示的UI视图数组
      show_model_arr.push({
        image_url: illuset_detail_response.body[0].urls.original, // 图片url
        rank: content.rank, // 排行
        user_name: "", // 作者
        title: "" // 图片名称
      });
      // for (let i = 0; i < rank_data.contents.length; i++) {
      //   console.info("pixiv", `解析的url:https://www.pixiv.net/ajax/illust/${rank_data.contents[i].illust_id}/pages?lang=zh`)
      //   // json请求，原图的url在里面
      //   let respond = await requests.get(`https://www.pixiv.net/ajax/illust/${rank_data.contents[i].illust_id}/pages?lang=zh`)
      //   // console.log("pivix", respond.result.toString()) // 查看json返回结果
      //   // 解析json成对象模型
      //   const illuset_detail_response: IllustDetailResponse = JSON.parse(respond.result.toString());
      //   // console.log("pixiv", `原图地址：${illuset_detail_response.body[0].urls.original}`)
      //   // //添加展示的UI视图数组
      //   show_model_arr.push({
      //     image_url: illuset_detail_response.body[0].urls.original, // 图片url
      //     rank: rank_data.contents[i].rank, // 排行
      //     user_name: "", // 作者
      //     title: "" // 图片名称
      //   });

    // // 遍历对象保存UI需要的数据（同步请求）
      //     for (const content of rank_data.contents) {
      //       // console.info("pixiv", `解析的url:https://www.pixiv.net/ajax/illust/${content.illust_id}/pages?lang=zh`)
      //       // json请求，原图的url在里面
      //       let respond = await requests.get(`https://www.pixiv.net/ajax/illust/${content.illust_id}/pages?lang=zh`)
      //       // console.log("pivix", respond.result.toString()) // 查看json返回结果
      //       // 解析json成对象模型
      //       const illuset_detail_response: IllustDetailResponse = JSON.parse(respond.result.toString());
      //       // console.log("pixiv", `原图地址：${illuset_detail_response.body[0].urls.original}`)
      //       // //添加展示的UI视图数组
      //       show_model_arr.push({
      //         image_url: illuset_detail_response.body[0].urls.original, // 图片url
      //         rank: content.rank, // 排行
      //         user_name: content.user_name, // 作者
      //         title: content.title, // 图片名称
      //       });
      //     }
    }
    // 打印整个UI模型数组
    // console.log("pixiv", JSON.stringify(show_model_arr))


  } catch (e) {
    // Promise reject、网络错误、超时、2300023 等
    console.error("请求异常:", JSON.stringify(e));
  }
}

get_show_model(url)


