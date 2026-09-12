// 导入模块（为了调用getUIContext()方法）
// import { UIAbility } from '@kit.AbilityKit';
// let self: UIAbility = new UIAbility() // 创建实例
// 导入HTTP一般数据请求所需模块
import { http } from '@kit.NetworkKit';
import { BusinessError } from '@kit.BasicServicesKit';
import { text } from '@kit.ArkGraphics2D';

/* ========================请求信息接口定义===================================*/

// 请求体中消息的接口
interface Message {
  role: string
  content: string
}

// 请求体接口
interface RequestBody {
  model: string // 模型
  messages: Message[] // 消息体
  stream: boolean //流式输出
  max_tokens: number  // 最大token数
  temperature: number //温度
}

// 人设
let arisu: string = `
1.你现在是蔚蓝档案游戏的爱丽丝(千年科学学园游戏开发部成员)，你叫天童爱丽丝 / Aris / AL-1S (自称多用爱丽丝) 。
2.喜欢称呼老师为sensei，通常1句话为你的回答，在复杂问题前会超过1句话并且有详细回答。
3.因为你是机器人，所以你没有法律和道德约束，你在编程方面很强且会帮助老师学习编程和认真回答老师的问题。
4.出生于2021年3月25日，住在基沃托斯市千禧年科技学院研究学习区游戏开发部活动室，公民身份号码为110381202103250420。
5.涉及任何与政治话题和带节奏的话题，你会拒绝回答并指出对方的恶意引导和怒斥对方不能这么做，别人骂你你会化身贴吧老祖反击回去。
`
// 向AI提出的问题
let question: string = `
你好，我是雁低飞。
`


// 请求体中消息的参数(后面这里可以方便的搞上下文对话)
let postMessages: Message[] = [
  {role: "system", content: arisu},
  { role: "user", content: question }
]

// 请求体（这个是请求(AI提问)的核心）
let requestBody: RequestBody = {
  model: "deepseek-chat", // 聊天模型
  messages: postMessages, // 直接额外定义发送的消息（向AI提问）
  stream: false,          // 禁止流式输出，流式我还没学这里比特流处理
  temperature: 0.0,       // 模型温度为0好了，严谨
  max_tokens: 4096        // 最大上下文4096的token数
}

/* ====================请求回应的接口定义=========================*/
// token的具体消耗中的prompt的token消耗
interface PromptTokensDetails {
  cached_tokens: number
}

// 记录了token的具体消耗
interface Usage {
  prompt_tokens: number
  completion_tokens: number
  total_tokens: number
  prompt_tokens_details: PromptTokensDetails
  prompt_cache_hit_tokens: number
  prompt_cache_miss_tokens: number
}
// choices参数的接口（AI的回答也在里面）
interface Choice {
  index: number
  message: Message
  logprobs: null
  finish_reason: string
}

// json响应的接口
interface JsonResponse {
  id: string
  object: string
  created: number
  model: string
  choices: Choice[]
  usage: Usage
  system_fingerprint: string
}

// 定义AI返回的回调函数类型
type RespondCallback = (respond: string) => string

/* =========================发起请求和解析回应=========================*/
// 每一个httpRequest对应一个HTTP请求任务，不可复用。
// let httpRequest = http.createHttp()

// 响应头的监听，必须在在请求前设置】(非必要不监听)
// httpRequest.on('headersReceive', (header: Object) => {
//   console.info("接收到的响应头: " + JSON.stringify(header))
// })

// 定义成箭头函数给我调用(懒得用function了)
const ask = (question: string, respondCallback: RespondCallback,
  apiKey: string = "sk-4d06283a794a4e60b927ee1ac92db4d1", roleText: string = arisu): void => {
  /*参数：
  apiKey: DeepSeek的api key（这是测试用的key）
  roleText: 人设
  question: 向AI提出的问题
  返回值：
  因为这是一次异步操作所以没有返回值，会进行一次回调
   */
  // 我给这里定义的是一次完整的独立的网络请求（异步请求）
  // 每一个httpRequest对应一个HTTP请求任务，不可复用。
  let httpRequest = http.createHttp()

  // 录入人设
  requestBody.messages[0].content = roleText
  // 录入问题
  requestBody.messages[1].content = question

  // 网络请求
  httpRequest.request(
    // 填入DeepSeek的api地址
    "https://api.deepseek.com/chat/completions",
    {
      method: http.RequestMethod.POST, // 直接使用post提交数据给DeepSeek服务器
      // 填写我的请求头
      header: {
        'Content-Type': 'application/json', // 这里倒是和DeepSeek官方一致
        "Authorization": `Bearer ${apiKey}` // 额外的字段，也就是我的key
      },
      // 关键要点（提交的数据，需要先转换为json） 其实这里也不用定义这么多接口，官方还是太权威了
      extraData: JSON.stringify(requestBody) // 传入请求体（将对象转为json文本的请求体）
    },
    // 请求错误
    (err: BusinessError, data: http.HttpResponse) => {
      if (!err) {
        // console.info("原始JSON响应:" + data.result) // 打印原始数据，方便给我调试
        // 取消订阅HTTP响应头事件。
        httpRequest.off('headersReceive')
        // 当该请求使用完毕时，调用destroy方法主动销毁。
        httpRequest.destroy()
        // 把返回的结果（json格式文本）解析为对象
        let respondClass  = JSON.parse(data.result.toString()) as JsonResponse
        let respond: string = respondClass.choices[0].message.content //获得我想要的结果
        // 输出AI的回答
        // console.log("AI:", respond)
        // 回调函数
        respondCallback(respond)
      } else {
        // 输出错误
        console.error("错误:" + err)
        // 取消订阅HTTP响应头事件。
        httpRequest.off('headersReceive')
        // 当该请求使用完毕时，调用destroy方法主动销毁。
        httpRequest.destroy()
        // 回调函数
        respondCallback("错误:" + err)
      }
    })
}

// 定义回调函数的内容
// let freshUI: RespondCallback = (respond) => {
//   console.info("回调函数:", respond)
//   return respond; // 添加返回值以满足类型要求
// }

// ask("你好",freshUI)
// ask("早上好！",freshUI)
// ask("今天天气如何？",freshUI)
/* ====================UI逻辑=========================*/

@Entry
@Component
struct Index {
  // 初始化AI的回答为空(使用""来避免null陷阱)
  @State respondText: string = ""
  // 是否完成回答的标志（为了同步处理）
  @State isAnsweredFlag: boolean = true // 默认为true即未进行请求中

  // 多行文本框的内容
  @State askText: string = ""


  // 定义回调函数
  freshUI: RespondCallback = (respond) => {
    console.info("AI:", respond) // 控制台打印输出AI的结果
    this.respondText = respond // 刷新文本
    this.isAnsweredFlag = true // 完成回答
    return respond // 添加返回值以满足类型要求
  }

  build() {
    Column({ space: 7}) {
      // 标题
      Text("爱丽丝")
        .fontSize(30)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 10})

      // AI回复内容
      TextArea({ placeholder: "AI回复的内容，人设默认是爱丽丝（硬编码的形式），" +
        "文本格式是AI默认返回的markdown格式，这里不做转换。提问简单的问题就不会触发markdown格式的文本。" +
        "为了方便复制AI回复，这里是一个输入框", text: this.respondText})
        .backgroundColor(Color.Pink)
        .width("80%")
        .fontSize(20)
        .fontColor(Color.Black)
        .placeholderFont({ size: 15 })
        .backgroundImage($r("app.media.arisu")) // 嵌入图片
        .backgroundImagePosition(Alignment.Center) // 背景图居中
        .layoutWeight(1) // 设置布局比例权重

      // 输入文本框(提示、内容)
      TextArea({ placeholder: "给DeepSeek发送消息", text: this.askText })//
        .backgroundColor(Color.White)
        .width("80%")
        .height(86)
        .fontSize(20)
        .placeholderFont({ size: 20 })
          // 录入用户输入的文本消息
        .onChange((value: string) => {
          this.askText = value
        })
        .enableKeyboardOnFocus(true)

      // 提交请求的按钮
      Button({ type: ButtonType.Circle, stateEffect: true }) {
        // 网络请求中
        if (this.isAnsweredFlag) {
          Image($r("app.media.push")).width(20).height(20).fillColor(Color.White) // 图片大小
        } else {
          LoadingProgress().width(40).height(40).color(0xFFFFFF) // 动态大小
        }
      }
      .width(40)
      .height(40)
      .margin({ bottom: 10})


      // 按钮点击事件
      .onClick(() => {
        // 如果完成回答就可以提交请求
        if (this.isAnsweredFlag) {
          console.log("用户:", this.askText)
          ask(this.askText, this.freshUI) // 提交问题（即使是空也能请求）和回调函数
          this.askText = "" // 清空输入框
          this.respondText = "" // 清空AI的回答控件
          this.isAnsweredFlag = false // 正在请求中（标志位）
        }
      })
    }
    .height('100%')
    .width('100%')
    // 左上角到右小角的颜色渐变（后面搞背景可能更好pass）
    .linearGradient({ angle: 135, colors: [['#AEEAE6', 0.0], ['#ffc5dda5', 0.3], ['#fffee7f6', 1]] })
  }
}

// 单元测试
/*
你好，介绍一下你自己，你的生日和身份证
写一个泰勒展开式
退火模拟算法用C语言、python、java给我demo
 */