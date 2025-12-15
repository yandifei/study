import http from '@ohos.net.http';
import { DoubanResponse, MovieItem } from '../model/DoubanModels';

// 说明当数据变化的时候，界面 UI 中用 @State 修饰的的变量可以响应其中的数据变化并通知界面更新
@Observed
@Entry
@Component
struct Index {
  @State counter: number = 0;
  build() {
    Column() {
      Button() {
        Text('下载电影')
          .fontSize(20)
      }
      .margin({ top: 30 })
      .width('60%')
      .height(50)
      .fontColor(Color.White)
      // 修改 onClick 函数的响应代码
      .onClick(async () => {
        const url ='https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=0&count=20&selected_categories=%7B%22%E7%B1%BB%E5%9E%8B%22:%22%E5%96%9C%E5%89%A7%22%7D&uncollect=false&score_range=0,10&tags=%E5%96%9C%E5%89%A7';
        let httpRequest = http.createHttp();
        console.info(`Starting network request to: ${url}`);
        try {
          const response = await httpRequest.request(url, {
            method: http.RequestMethod.GET,
            header: {
              'accept': 'application/json, text/plain, */*',
              'accept-language': 'zh-CN,zh;q=0.9',
              'origin': 'https://movie.douban.com',
              'priority': 'u=1, i',
              'referer': 'https://movie.douban.com/explore',
              'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143","NotA(Brand";v="24"',
              'sec-ch-ua-mobile': '?0',
              'sec-ch-ua-platform': '"Linux"',
              'sec-fetch-dest': 'empty',
              'sec-fetch-mode': 'cors',
              'sec-fetch-site': 'same-site',
              'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
          });
          if (response.responseCode === http.ResponseCode.OK) {
            let resultStr = typeof response.result === 'string'?response.result : JSON.stringify(response.result);
            const doubanData: DoubanResponse = JSON.parse(resultStr);if (doubanData && doubanData.items) {
              console.info('--- 开始遍历电影列表 ---');
              doubanData.items.forEach((item: MovieItem) => {
                console.info(` 电 影 : ${item.title}, 星级:${item.rating?.star_count ?? '无'}`);
              });
            } else {
              console.info('未找到电影项目或返回数据格式不正确');
            }
          } else {
            console.info(`Request failed. Response code:${response.responseCode}, message: ${JSON.stringify(response.header)}`);}
        } catch (err) {
          console.info(`Request error: ${JSON.stringify(err)}`);
        } finally {
          httpRequest.destroy();
        }
      })
    }
    .width('100%')
    .height('100%')
  }
}
