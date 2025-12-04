import { http } from '@kit.NetworkKit';

@Entry
@Component
struct Index {
  @State message: string = 'HTTP 测试';
  @State url: string = '';
  @State result: string = '';
  build() {
    Column() {
      Text(this.message)
        .fontSize(30)
        .margin('2%')
      TextInput({placeholder: '请输入 URL'})
        .width('75%')
        .margin({top: 10})
        .enableKeyboardOnFocus(false)
        .onChange((value: string) => {
          this.url = value;
        })
      Button('发送 GET 请求')
        .width('60%')
        .height(50)
        .margin({top: 10})
        .onClick(()=> {
          let httpRequest = http.createHttp();
          let promise = httpRequest.request(this.url, {
            method: http.RequestMethod.GET, connectTimeout: 60000, readTimeout: 60000, header: 'application/json'
          });
          promise.then((data:http.HttpResponse) => {
            console.info('Result:' + data.result);
            console.info('code:' + data.responseCode);
            console.info('type:' + JSON.stringify(data.resultType));
            console.info('header:' + JSON.stringify(data.header));
            console.info('cookies:' + data.cookies); // 自 API version 8 开始支持cookieconsole.info('header.content-Type:' + data.header);
            console.info('header.Status-Line:' + data.header);
            this.result = data.result.toString();
          }).catch((err:Error) => {
            console.info('error:' + JSON.stringify(err));
          });
        })
      TextArea({placeholder: '结果输出在这里', text: this.result})
        .width('75%')
        .height('50%')
        .margin({top: 30})
        .maxLines(50)
    }
    .height('100%')
    .width('100%')
  }
}