import { http } from '@kit.NetworkKit';
import { rcp } from '@kit.RemoteCommunicationKit';
import { BusinessError } from '@kit.BasicServicesKit';
import axios, { AxiosError, AxiosResponse } from '@ohos/axios';

interface UserInfo {
  username: string
  password: string
}

@Entry
@Component
struct Index {
  @State message: string = 'HTTP 测试';
  // @State url: string = '';
  @State url: string = 'https://www.wanandroid.com/user/login';
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
        // .onClick(()=> {
        //   let httpRequest = http.createHttp();
        //   let promise = httpRequest.request(this.url, {
        //     method: http.RequestMethod.GET, connectTimeout: 60000, readTimeout: 60000, header: 'application/json'
        //   });
        //   promise.then((data:http.HttpResponse) => {
        //     console.info('Result:' + data.result);
        //     console.info('code:' + data.responseCode);
        //     console.info('type:' + JSON.stringify(data.resultType));
        //     console.info('header:' + JSON.stringify(data.header));
        //     console.info('cookies:' + data.cookies); // 自 API version 8 开始支持cookieconsole.info('header.content-Type:' + data.header);
        //     console.info('header.Status-Line:' + data.header);
        //     this.result = data.result.toString();
        //   }).catch((err:Error) => {
        //     console.info('error:' + JSON.stringify(err));
        //   });
        // })
        // .onClick(()=> {
        //   let httpRequest = http.createHttp();
        //   httpRequest.request(this.url, (err: Error, data: http.HttpResponse) =>{
        //     if (!err) {
        //       console.info('Result:' + data.result);
        //       console.info('code:' + data.responseCode);
        //       console.info('type:' + JSON.stringify(data.resultType));
        //       console.info('header:' + JSON.stringify(data.header));
        //       console.info('cookies:' + data.cookies);
        //       this.result = data.result.toString();
        //     } else {
        //       console.info('error:' + JSON.stringify(err));
        //     }
        //   });
        // })
        // .onClick(() => {
        //   let kHttpServerAddress = this.url;
        //   // 创建 Request 对象
        //   const request = new rcp.Request(kHttpServerAddress, "GET");
        //   // 创建会话
        //   const session = rcp.createSession();
        //   // 发起请求，并处理返回结果
        //   session.fetch(request).then((rep: rcp.Response) => {
        //     console.info(`Response succeeded: ${rep}`);
        //     if (rep != null) {
        //       this.result = `${rep}`;
        //     }
        //   }).catch((err: BusinessError) => {
        //     console.error(`Response err: Code is ${err.code}, messageis${JSON.stringify(err)}`);
        //   });
        // })
        // .onClick(()=> {
        //   const instance = axios.create();
        //   instance.get<string, AxiosResponse<string>, null>(this.url, {
        //     connectTimeout: 20000
        //   }).then((res: AxiosResponse) => {
        //     console.info(`AxiosTest status is: ${res ? res.status : ''}`);
        //     console.info(`AxiosTest data is: ${res ? JSON.stringify(res.data) : ''}`) ;
        //     this.result = `${res ? JSON.stringify(res.data) : 'nothing'}`
        //   }).catch((err: AxiosError) => {
        //     console.info(`AxiosTest err is: ${err.message}`) ;
        //   })
        // })
        // .onClick(()=> {
        //   const instance = axios.create();
        //   instance.request<string, AxiosResponse<string>, UserInfo>({
        //     url: this.url, method: 'post', data: {
        //       username: 'your name',
        //       password: 'abcd1234' },connectTimeout: 20000
        //   }).then((res: AxiosResponse) => {
        //     console.info(`AxiosTest status is: ${res ? res.status : ''}`);
        //     this.result = `${res ? JSON.stringify(res.data) : ''}`
        //   })
        // })
        .onClick(()=> {
          // https://www.wanandroid.com/user/login
          const instance = axios.create();
          instance.post<string, AxiosResponse<string>, UserInfo>(
            this.url, {
            username: 'yourname', password: 'abcd1234' },{
            connectTimeout: 20000
          }).then((res: AxiosResponse) => {
            console.info(`AxiosTest status is: ${res ? res.status : ''}`);
            this.result = `${res ? JSON.stringify(res.data) : 'nothing'}`;
          })
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