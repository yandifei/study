import { http } from '@kit.NetworkKit';
import { IllustDetailResponse } from './IllustDetailResponse';
import { NextDataModel, Contents } from './NextDataModel';
import { ShowModel } from '../entry/src/main/ets/data/ShowModel';



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

// 今日排行
const  url: string = `https://www.pixiv.net/ranking.php?mode=daily${r18 ? "_r18" : ""}&content=illust`
// 本周排行
// url = f"https://www.pixiv.net/ranking.php?mode=weekly{"_r18" if r18 else ""}&content=illust"
// 本月排行
// url = f"https://www.pixiv.net/ranking.php?mode=monthly{"_r18" if r18 else ""}&content=illust"
// 新人排行
// url = f"https://www.pixiv.net/ranking.php?mode=rookie&{"_r18" if r18 else ""}content=illust"

// 存放UI作品对象
let show_model_arr: ShowModel[] = []


let httpRequest = http.createHttp();

function request_get(url: string, callback_function: (err: Error, response: http.HttpResponse) => void = () => {}) {
  /**
   * url:pixiv网址
   * callback_function:可选参数，回调函数
   */
  // 创建请求实例
  httpRequest.request(
    url, // 请求URL
    {
      method: http.RequestMethod.GET, // 请求方法：GET
      header: { // 请求头（模拟浏览器请求，我这里就极致参数，其他默认）
        // 用户代理（身份用我windows的chrome模拟）
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        // 伪装请求来自合法来源（这个关键）
        "referer": "https://www.pixiv.net"
      }
    },
    // 请求回调函数
    (err, response) => {
      // 调用回调函数处理结果
      // const result = callback_function(err, response);
      callback_function(err, response);
      // // 在请求完成后销毁实例
      // httpRequest.destroy();
      // // 把回调函数的结果返回
      // return result;
    }
  );
}
const pic_url_callback = (err: Error, response: http.HttpResponse) => {
  if (!err) {
    // 解析json成对象模型
    const illuset_detail_response: IllustDetailResponse = JSON.parse(response.result.toString());
    // illuset_detail_response.body.urls.original
    // //添加展示的UI视图数组
    // show_model_arr.push({
    //   image_url: illuset_detail_response.body.urls.original, // 使用正确的属性名
    //   rank: 0, // 提供所有必需的属性
    //   author: "",
    //   image_name: ""
    // });
  } else {
    console.log("pixiv", `请求失败，错误信息:${JSON.stringify(err)}`)
  }
}

const callback_function_1 = (err: Error, response: http.HttpResponse) => {
  // 存放Contents对象的数组
  let contents: Contents[] =  []
  // console.log("pixiv", `请求状态码:${response.responseCode}`)
  if (!err) {
    // 获取响应数据
    const responseText: string = response.result.toString();
    // 正则匹配数据
    const match = responseText.match(/<script id="__NEXT_DATA__" type="application\/json">([\s\S]*?)<\/script>/);
    // // 查看返回数据
    // console.log("", match?.groups?.data)
    // 判断是否存在匹配数据
    if (!match) { throw new Error("pixiv: 未在 html 中找到 __NEXT_DATA__ 数据"); }
    console.log("pixiv", match[1])
    // 解析JSON数据（match[1]返回括号捕获内容，0返回全部捕获内容）
    const nextData: NextDataModel = JSON.parse(match[1]);
    // 拿到所有插画内容对象
    const contents = nextData.props.pageProps.assign.contents;
    console.log("pixiv", `共解析了${contents.length}个插画内容对象`);
    // 遍历对象
    for (const item of contents) {
      // 藏着图片url的json地址
      console.log("pixiv", `解析的url:https://www.pixiv.net/ajax/illust/${item.illust_id}?lang=zh`)
      // json请求，真正的url在里面
      request_get(`https://www.pixiv.net/ajax/illust/${item.illust_id}?lang=zh`, pic_url_callback)
    }

  } else {
    console.log("pixiv", `请求失败，错误信息:${JSON.stringify(err)}`)
  }
}

// 发送HTTP GET请求
request_get(url, callback_function_1)
//

// 在请求完成后销毁实例
httpRequest.destroy();