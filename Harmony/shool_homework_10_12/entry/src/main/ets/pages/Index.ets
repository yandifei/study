import { router } from '@kit.ArkUI'; // 路由跳转

@Entry
@Component
struct Index {
  @State message: string = 'Hello World';

  build() {
    Column() {
      // log图标
      Image($r("app.media.logo"))
        .width("50%")

      // 文本控价
      Text("欢迎回来")
        .fontSize(FontWeight.Bolder)  // 字体加粗
        .fontSize(35)
        .margin({ top: 20, bottom: 20}) // 外边距

      // 账号输入区域
      Row() {
        //左侧图标
        Image($r("app.media.user"))
          .width("7%")
          .margin({ left: 10}) // 设置左边距
        // 账号输入框
        TextInput({ placeholder: "请输入用户名"})
          .placeholderColor("#c1c1c1") // 设置占位符颜色
          .placeholderFont({ size: 20, weight: FontWeight.Medium}) // 字体大小和让它稍微粗一点
          .backgroundColor(Color.Transparent) // 原来的输入框背景设置透明
          .margin({ right: 30})
      }
      .backgroundColor("#f4f6f5") // 设置为输入框的背景色
      .borderRadius(20)

      // 密码输入框区域
      Row() {
        //左侧图标
        Image($r("app.media.keyboard"))
          .width("7%")
          .margin({ left: 10}) // 设置左边距
        // 密码输入框
        TextInput({ placeholder: "请输入密码"})
          .type(InputType.Password) // 设置为密码类型的输入框
          .placeholderColor("#c1c1c1") // 设置占位符颜色
          .placeholderFont({ size: 20, weight: FontWeight.Medium}) // 字体大小和让它稍微粗一点
          .backgroundColor(Color.Transparent) // 原来的输入框背景设置透明
          .margin({ right: 30})
      }
      .width("100%") // 撑满空间
      .backgroundColor("#f4f6f5") // 设置为输入框的背景色
      .borderRadius(25)
      .margin({ top: 15, bottom: 15})

      // 注册和忘记密码区域
      Row() {
        // 立即注册
        Text("立即登陆")
          .backgroundColor("#fff") // 白色背景
          .fontColor("#ff5f5f5f") // 字体颜色（非纯黑）
        // 忘记密码
        Text("忘记密码")
          .backgroundColor("#fff") // 白色背景
          .fontColor("#ff5f5f5f") // 字体颜色（非纯黑）
      }
      .width('100%') // 必须设置宽度100%
      .justifyContent(FlexAlign.SpaceBetween) // 两侧对齐

      // 登陆按钮
      Button("登陆")
        .fontSize(20) // 字体大小20号
        .fontWeight(FontWeight.Bold) // 加粗
        .width("100%") // 撑满空间
        .margin({ top: 25, bottom: 200})
        // 点击登陆跳转到主界面
        .onClick(() => {
          this.getUIContext().getRouter().pushUrl({
            url: "pages/Main", // 目标url
          }, router.RouterMode.Standard, (err) => {
            if (err) {
              console.error(`跳转失败， 错误代码：${err.code}，错误信息 ${err.message}`);
              return;
            }
            console.info("跳转成功");
          })
        })

      // 其他的登陆方式
      Row() {
        // QQ
        Image($r("app.media.QQ"))
          .width("14%")
          .borderRadius(25) // 设置圆角
        // 微信
        Image($r("app.media.weixin"))
          .width("14%")
          .borderRadius(25) // 设置圆角
        // GitHub
        Image($r("app.media.github"))
          .width("14%")
          .borderRadius(25) // 设置圆角
        // Gitee
        Image($r("app.media.gitee"))
          .width("14%")
          .borderRadius(25) // 设置圆角
      }
      .width("80%")
      .justifyContent(FlexAlign.SpaceBetween) // 对齐撑开
    }
    .height('100%')
    .width('100%')
    .padding({ right: 20, left: 20}) // 外边距离
  }

  // 禁用界面入场和出场有动画
  pageTransition() {
    PageTransitionEnter({ type: RouteType.None, duration: 0 })
    PageTransitionExit({ type: RouteType.None, duration: 0 })
  }
}
