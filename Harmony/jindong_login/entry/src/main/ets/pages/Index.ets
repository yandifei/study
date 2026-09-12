/*
最新版的鸿蒙有系统安全区域，所以上下有留白很正常
 */

@Entry
@Component
struct Index {
  build() {
    Column() {
      //顶部区域
      Row() {
        Image($r('app.media.ic_xmark'))
          .width(20)
          .fillColor("#666")
        Text("帮助")
          .fontColor("#666")
      }
      .width("100%")
      .justifyContent(FlexAlign.SpaceBetween)


      // Logo标志
      Image($r("app.media.default_avatar")) //这里的logo很大
        .width(100)  // 宽度占满父容器
        .height(100) // 长度占满父容器
         // 因为图片大小不同，我自己添加的外边距
        .margin(20)

      // 国家/地址（自己画）
      Row() {
        Text("国家/地址")
          .layoutWeight(1) //这是比例占比
          .fontColor("#666") //调整颜色
        Text("中国(+86)")
          .margin(5) // 设置外边距
          .fontColor("#666") //调整颜色
        Image($r("app.media.ic_chevron_right"))
          .width(12) // 我这里设置12，视频是20
          .fillColor("#666")
      }
      .width("100%")
      .height(40)
      .backgroundColor("#fff")
      .borderRadius(20)
      .padding({ left: 15, right: 15})

      // 手机号（输入框）
      TextInput({
        placeholder: "请输入手机号"
      })
        //为了和上面一样调整高度和圆角
        .height(40)
        .borderRadius(20)
        .backgroundColor("#fff") // 默认灰色，设置和上一个输入框一致即为纯白
        .margin({ top: 20}) // 设置边距
        .placeholderColor("#666") // 设置占位符颜色

      // 已阅读并同意
      Row() {
        // 复选框
        Checkbox()
          .width(10)
          .margin({ top:7 }) //微调复选框和文本的上下对齐
        //一段文本中，有文本样式需要单独定制，Text包裹Span
        Text() {
          Span("我已经阅读并同意")
          Span("《京东隐私政策》").fontColor("#3274f6")  // 设置颜色蓝色
          Span("《京东用户服务协议》").fontColor("#3274f6")// 设置颜色蓝色
          Span("未注册的手机号讲自动创建京东账号")
        }
          .fontSize(12)
          .fontColor("#666")
          .lineHeight(20) //设置行高为20
      }
      // 文本和复选框顶端对齐
      .alignItems(VerticalAlign.Top  )

      // 登录
      Button("登陆")
        .width("100%")
        .backgroundColor("#bf2838")
        .margin({ top: 25})

      // 新用户注册等链接
      Row({ space: 25}) {
        Text("新用户注册").fontSize(14).fontColor("#666")
        Text("账户密码登陆").fontSize(14).fontColor("#666")
        Text("无法登陆").fontSize(14).fontColor("#666")
      }
      .margin({ top: 15 }) // 顶部外边距为15

      //填充组件；作用：填充空白区域,像弹簧
      Blank()

      //底部其他登录方式
      Column() {
        Text("其他登陆方式")
          .height(22)
          .fontSize(14)
          .margin({ bottom: 28})
          .fontColor("#666")
        Row() {
          Image($r("app.media.huawei")).width(34).borderRadius(17).fillColor('#56a44a')
          Image($r("app.media.weixin")).width(34).borderRadius(17).fillColor('#56a44a')
          Image($r("app.media.weibo_logo")).width(34).borderRadius(17).fillColor('#56a44a')
          Image($r("app.media.QQ")).width(34).borderRadius(17).fillColor('#56a44a')
        }
        .width("100%")
        .margin({ bottom: 30  })
        .justifyContent(FlexAlign.SpaceAround)
      }
        .width('100%')

    }
    .padding(20)
    .width("100%")
    .height("100%")
    // 这里我没有使用视频里面的背景图作为背景颜色（问了十几次AI的成果）
    // linearGradient的api学习：https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-universal-attributes-gradient-color#lineargradient
    //.linearGradient()是一个修饰符（modifier）
    .linearGradient({
      /* angle这个参数用于指定渐变的方向。它的值以度（degrees）为单位。
      0: 渐变从左到右。
      90: 渐变从下到上。
      180: 渐变从上到下。这是您代码中使用的值。
      270: 渐变从右到左。
      */
      angle: 135, //视频里面是左上到右下的颜色过度
      // Explicitly define the color stops with their positions
      colors: [
      // 左上角的浅青色
        ['#AEEAE6', 0.0],
        // 渐变到中间的白色
        ['#FFFFFF', 0.3],
        // 底部和右侧的浅桃色
        ['#FEE9E7', 1]
      ]
    })
  }
}