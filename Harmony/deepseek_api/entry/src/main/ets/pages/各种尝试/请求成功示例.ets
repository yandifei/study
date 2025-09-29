// 导入模块（为了调用getUIContext()方法）
// import { UIAbility } from '@kit.AbilityKit';
// let self: UIAbility = new UIAbility() // 创建实例
// 导入HTTP一般数据请求所需模块
import { http } from '@kit.NetworkKit';
import { BusinessError } from '@kit.BasicServicesKit';
import { common } from '@kit.AbilityKit';


// 每一个httpRequest对应一个HTTP请求任务，不可复用。
let httpRequest = http.createHttp();

// 定义请求消息的接口
interface Message {
  role: string;
  content: string;
}


// 构建发送的消息
let postMessages: Message[] = [
  {role: "system", content: "你是DeepSeek，现在你面对的是使用Harmony Next的用户，你需要你提供最大的支持"},
  { role: "user", content: "你好" }
]

// 定义DeepSeek请求参数接口
interface ChatRequestParams {
  model: string;
  messages: Message[];
  stream: boolean;
  temperature?: number;
  max_tokens?: number;
}

// 请求头构建
const chatParams: ChatRequestParams = {
  model: "deepseek-chat",
  messages: postMessages, //直接额外定义发送的消息（向AI提问）
  stream: false,          // 禁止流式输出，流式我还没学这里比特流处理
  temperature: 0.0,       // 模型温度为0好了，严谨
  max_tokens: 4096        // 最大上下文4096的token数
};

// 保存结果
let respond: string = ""

// 网络请求
httpRequest.request(
  // 填入DeepSeek的api地址
  "https://api.deepseek.com/chat/completions",
  {
    method: http.RequestMethod.POST, // 直接使用post提交数据给DeepSeek服务器
    // 填写我的请求头
    header: {
      'Content-Type': 'application/json', // 这里倒是和DeepSeek官方一致
      "Authorization": "Bearer sk-dfebad3b27964b3fb62e603e71aa8d2c" // 额外的字段，也就是我的key
    },
    // 关键要点（提交的数据，需要先转换为json） 其实这里也不用定义这么多接口，直接写死字符串就好了，官方还是太权威了
    extraData: JSON.stringify(chatParams) // 传入消息对象

  }, (err: BusinessError, data: http.HttpResponse) => {
  if (!err) {
    // data.result为HTTP响应内容，可根据业务需要进行解析。
    console.info('结果:' + JSON.stringify(data.result));
    console.info('代码:' + JSON.stringify(data.responseCode));
    // data.header为HTTP响应头，可根据业务需要进行解析。
    console.info('请求头:' + JSON.stringify(data.header));
    console.info('cookies:' + JSON.stringify(data.cookies)); // 8+
    // 保存结果
    respond = '结果:' + JSON.stringify(data.result) + '代码:' + JSON.stringify(data.responseCode) +
      '请求头:' + JSON.stringify(data.header) + 'cookies:' + JSON.stringify(data.cookies)
    // 当该请求使用完毕时，调用destroy方法主动销毁。
    httpRequest.destroy();
  } else {
    console.error('错误:' + JSON.stringify(err));
    // 取消订阅HTTP响应头事件。
    httpRequest.off('headersReceive');
    // 当该请求使用完毕时，调用destroy方法主动销毁。
    httpRequest.destroy();
  }
}
);

@Entry
@Component
struct Index {
  @State message: string = respond;

  build() {
    RelativeContainer() {
      Text(this.message)
    }
    .height('100%')
    .width('100%')
  }
}