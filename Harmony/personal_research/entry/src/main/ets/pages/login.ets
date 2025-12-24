// import { http } from "@kit.NetworkKit";
// import { IllustDetailResponse } from "../test/IllustDetailResponse";
// import { NextDataModel } from "../test/NextDataModel";
// import { ShowModel } from "../data/ShowModel";
//
// console.log("开始测试")
//
// export class Requests {
//   get(url: string): Promise<http.HttpResponse> {
//     /**
//      * url:pixiv网址
//      * 返回响应对象
//      */
//     const request = http.createHttp(); // 每次请求一个实例
//
//     return request.request(
//       url, // 请求URL
//       {
//         method: http.RequestMethod.GET, // 请求方法：GET
//         header: {
//           // 请求头（模拟浏览器请求，我这里就极致参数，其他默认）
//           // 用户代理（身份用我windows的chrome模拟）
//           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
//           // 伪装请求来自合法来源（这个关键）
//           "referer": "https://www.pixiv.net"
//         }
//       },
//     ).finally(() => { request.destroy();}); // 请求结束，销毁实例
//   }
// }
//
// // 是否r18(r18必须加cookies)
// let r18: boolean = false;
// // 今日排行
// const  url: string = `https://www.pixiv.net/ranking.php?mode=daily${r18 ? "_r18" : ""}&content=illust&format=json`
// // 本周排行
// // url = `https://www.pixiv.net/ranking.php?mode=weekly{"_r18" if r18 else ""}&content=illust&format=json`
// // 本月排行
// // url = `https://www.pixiv.net/ranking.php?mode=monthly{"_r18" if r18 else ""}&content=illust&format=json`
// // 新人排行
// // url = `https://www.pixiv.net/ranking.php?mode=rookie&{"_r18" if r18 else ""}content=illust&format=json`
//
// // 存放UI作品对象
// let show_model_arr: ShowModel[] = []
// // 异步函数
// async function get_show_model(url: string){
//   // 创建请求实例
//   const requests = new Requests();
//   try {
//     // 发送请求
//     let respond = await requests.get(url);
//
//     // 请求状态码判断是否为有效请求
//     if (respond.responseCode !== 200) {
//       console.error("pixiv", `请求失败，状态码：${respond.responseCode}`);
//       return;
//     }
//
//     let responseText = respond.result.toString();
//     // 正则匹配数据
//     const match = responseText.match(/<script id="__NEXT_DATA__" type="application\/json">([\s\S]*?)<\/script>/);
//     // console.log("", match?.groups?.data) // 查看返回数据
//     // 判断是否存在匹配数据
//     if (!match) { throw new Error("pixiv: 未在 html 中找到 __NEXT_DATA__ 数据"); }
//     console.log("pixiv", match[1])
//     // 解析JSON数据（match[1]返回括号捕获内容，0返回全部捕获内容）
//     const nextData: NextDataModel = JSON.parse(match[1]);
//     // 拿到所有插画内容对象
//     const contents = nextData.props.pageProps.assign.contents;
//     console.log("pixiv", `共解析了${contents.length}个插画内容对象`);
//
//     // 遍历对象
//     for (const item of contents) {
//       // 藏着图片url的json地址
//       console.info("pixiv", `解析的url:https://www.pixiv.net/ajax/illust/${item.illust_id}?lang=zh`)
//       // json请求，真正的url在里面
//       let respond = await requests.get(`https://www.pixiv.net/ajax/illust/${item.illust_id}?lang=zh`)
//       // console.log("pivix", respond.result.toString()) // 查看json返回结果
//       // 解析json成对象模型
//       const illuset_detail_response: IllustDetailResponse = JSON.parse(respond.result.toString());
//       // illuset_detail_response.body.urls.original
//       //添加展示的UI视图数组
//       show_model_arr.push({
//         image_url: illuset_detail_response.body.urls.original, // 使用正确的属性名
//         rank: 0, // 提供所有必需的属性
//         author: "",
//         image_name: ""
//       });
//     }
//     // 打印整个UI模型数组
//     console.log("pixiv", JSON.stringify(show_model_arr))
//
//
//   } catch (e) {
//     // Promise reject、网络错误、超时、2300023 等
//     console.error("请求异常:", JSON.stringify(e));
//   }
// }
//
// get_show_model(url)
