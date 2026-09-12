/*【阶段综合】-生肖抽卡

阶段案例一生肖抽奖卡-初始布局
知识点：
1.Badge角标组件
2.Grid布局（其实这里就是Qt的栏珊布局
Grid布局的基本使用：规则的行列布局中非常常见，3行4列

阶段案例-生肖抽奖卡-数据动态渲染
每个列表项-两个数据：
1.图片的地址
2.抽中的数量

阶段案例一生肖抽奖卡-抽卡遮罩层
思路分析：
1.布局角度：层叠布局Stack
2.结构角度：Column > TextImage + Button

阶段案例一生肖抽奖卡-显隐效果控制
需求1：点击抽卡，才显示遮罩层
需求2：图片，要有缩放显示动画
遮罩显隐控制：
1. 透明度opacity：0=> 1
2.层级zIndex:-1 => 99
图片动画：
缩放scale:0=> 1

阶段案例一生肖抽奖卡一随机卡片
需求：
1．取随机数 Math.random
2.控制展示（换图）
3.点击收下，卡片数累加

价段案例-生肖抽奖卡一抽大奖遮罩层
思路分析：
1.布局角度：层叠布局Stack
2.结构角度：Column > Text +Image + Button

阶段案例-生肖抽奖卡-抽大奖遮罩层
思路分析：
1.布局角度：层叠布局Stack
2.结构角度：Column > Text + Image + Button

阶段案例-生肖抽奖卡-抽大奖显隐控制
需求说明：六张卡片集齐，显示-中大奖页面
思路：
1.准备一个变量，控制显隐
2.每次收下卡片，判断是否集齐，集齐显示中奖页面

阶段案例一生肖抽奖卡一随机奖品品&再来一次
需求1：奖品随机
需求2：再来一次
思路：
1．奖品随机→准备一个奖品数组，Math.random随机取下标
2.再来一次→重置数据
 */

/* 注意事项
 弹幕：我自己是api10研究半天发现得用hitTestBehavior这个触摸测试控制东西才可以做，
 而且需要额外做一个布尔值去控制状态，hit_status默认值为false，两个按键翻转hit_status的状态就好了
 我自己是api10研究半天发现得用hitTestBehavior这个触摸测试控制东西才可以做，而且需要额外做一个布尔值去控制状态

跟着视频里面做之后，发现点击事件也就是切换抽卡界面和抽卡后的界面(遮罩)不成功，后面发现是按钮点击事件写错了，需要注意
位置，视频里面展开第一个界面的速度很快，我没有看清，这里需要注意。

黑马视频里面使用透明度和zIndex来对抽卡和抽卡后的界面进行切换，实际上我看到zIndex这个方法后就知道这个才是关键，
这个是用来控制界面层级顺序的，它的透明度本质是为了配合它的动画，如果不要动画直接zIndex这一个就够了

scale用来控制动态缩放，Qt亦有记载

弹幕：直接加一个translation属性，然后包进animateTo()里面，组件创建时会自动播放入场动画
可以去看官方文档的转场动画，其实这个很方便的，直接定义一个boolean值，用animateTo包起来，再给组件加translation属性就可以了

专场动画:https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-fair-use-animation#section1150051943714

这个抽卡索引也是神人啊！！！，直接改字符串，图片命名规则玩是吧？
//0 1 2 3 4 5
[0,1) * 6 => [0,6)
求随机数:Math.random
向下取整：Math.floor
console.log('随机数',Math.random * 6)

弹幕：数组替换肯定不行，说白了监听的是对象地址，你把对象都换了，监听就丢失了
 */

//1.定义接口 （每个列表项的数据结构）
interface ImageCount {
  url: string
  count: number
}

@Entry
@Component
struct Index {
  // 随机的生肖卡序号
  @State randomIndex: number = -1 // 表示还没开始抽卡

  // 控制中大奖遮罩的显隐
  @State isGet:boolean = false

  // 大奖池
  @State arr: string[] = ["prize0", "prize1", "prize2", "prize3"]
  // 自己的大奖池奖品名变幻（映射处理）
  @State prizeMap: Map<string, string> = new Map<string, string>([
    ["prize0", "勇者爱丽丝"], ["prize1", "女仆爱丽丝"],
    ["prize2", "中秋爱丽丝"], ["prize3", "星空爱丽丝"]])
  // @State prize_name: string[] = []
  @State prize: string = "" // 默认为空即没有中奖


  // 基于接口，准备数据
  @State images: ImageCount[] = [
    { url: "app.media.sercet1", count: 0},
    { url: "app.media.sercet2", count: 0},
    { url: "app.media.sercet3", count: 0},
    { url: "app.media.sercet4", count: 0},
    { url: "app.media.sercet5", count: 0},
    { url: "app.media.sercet6", count: 0},
  ]

  // 控制遮罩的显示和隐藏
  @State maskOpacity: number = 0 // 透明度
  @State maskZIndex: number = -1 // 显示层级

  // 控制图片缩放
  @State maskImgX: number = 0 //水平方向缩放比
  @State maskImgY: number = 0 //垂直方向缩放比

  // 再来一次（数据重置）

  build() {
    // 层叠布局Stack，用来封装2个界面就不用做界面跳转了(抽出卡后的界面就很合适)
    Stack() {
      //抽卡界面
      Column() {
        //这个控件加个width("100%")和背景没有显示出来，这确实是一个神奇的容器
        // GridItem印证了我的猜想，仅当被使用的时候才有占位
        Grid() {
          ForEach(this.images, (item: ImageCount, index: number) => {
            //设置单个栅栏控件
            GridItem() {
              // 设置圆点红标
              Badge({
                count: item.count, // 数量为0不显示红标
                position: BadgePosition.RightTop, //设置小圆圈位置为右上角
                style: {
                  badgeSize: 20,
                  fontSize: 14,
                  badgeColor: "#fa2a2d"
                }
              })
              //设置栅栏控件的主要内容
              {
                Image($r(item.url))
                  .width(100)
                  .height(100)
                  .borderRadius(10)
                    // 因为我是透明图所以这里就必须给爱丽丝设置背景
                  .backgroundColor(Color.Blue)
              }
            }
          })
        }
        //设置横向占比
        .columnsTemplate('1fr 1fr 1fr')
        //设置纵向占比
        .rowsTemplate('1fr 1fr')
        //设置Grip格子之间的宽度
        .columnsGap(5)
        .rowsGap(5)
        .width("100%")
        .height(250)
        // 设置Grid背景
        // .backgroundColor(Color.Pink)
        // 设置间隙
        .margin({ top: 100 })

        //设置抽卡按钮
        Button("立即抽卡")
          .width(200)
          .backgroundColor("#ed5b8c")
          .margin({ top: 50})
          .onClick(() => {
            // 点击时，修改遮罩参数，让抽卡后的界面显示（遮罩姐界面）
            this.maskOpacity = 1
            //点击按钮后层级为99
            this.maskZIndex = 99
            //点击图片时，图片需要缩放
            this.maskImgX = 1
            this.maskImgY = 1
            //计算随机数Math.random [0,1) * (n + 1) , 我这里+1是因为我没有下标为1的图片
            this.randomIndex = Math.floor(Math.random() * 6) + 1
          })
        // 我写的一个作弊按钮(黑马直接改对象数组的数据)
        Button("作弊按钮，集齐卡片")
          .width(200)
          .margin({ top: 50})
          .backgroundColor(Color.Blue)
          .onClick(() => {
            // // 遍历数组
            // for (let item of this.images) {
            //   item.count = 1 //抽卡数量全部变成1
            // }
            // 开销控件,但是只有在当前结构才能刷新控件
            this.images = [
              { url: "app.media.sercet1", count: 99},
              { url: "app.media.sercet2", count: 99},
              { url: "app.media.sercet3", count: 99},
              { url: "app.media.sercet4", count: 99},
              { url: "app.media.sercet5", count: 99},
              { url: "app.media.sercet6", count: 99},
            ]
          })
      }
      .width("100%")
      .height("100%")
      //这个渐变背景直接抄之前写的（京东登陆）
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

      // 抽卡后的界面==抽卡遮罩层(弹层)
      Column({ space: 30}) { //3个控件加点间距
        Text("获得野生的爱丽丝")
          .fontColor("#f5ebcf") //金色传说
          .fontSize(25)
          .fontWeight(FontWeight.Bold)
        Image($r(`app.media.${this.randomIndex}`)) //神人替换
          .width(350)
          // 控制元素的缩放
          .scale({
            x: this.maskImgX,
            y: this.maskImgY
          })
          .animation({
            duration: 200 //图片缩放为500毫秒
          })
          //自己加的圆角
          .borderRadius(10)

        Button("开心收下")
          .width(200)
          .height(50)
          .backgroundColor(Color.Transparent) //设置这个按钮的背景色为透明
          .border({ width: 2, color: "#fff9e0" })  // 设置边框颜色
          .onClick(() => {
            // 点击时，修改透明度参数，让抽卡界面显示
            this.maskOpacity = 0
            //点击按钮后层级为0,显示抽卡界面
            this.maskZIndex = -1
            //点击收下时，图片需要恢复缩放
            this.maskImgX = 0
            this.maskImgY = 0

            //开心收下，对象数组的情况需要更新，需要修改替换整个对象
            // this.images[this.randomIndex].count ++
            // -1 是因为抽到卡片的下标是从1开始的
            this.images[this.randomIndex - 1] = {
              url: `app.media.${this.randomIndex}`,
              count: this.images[this.randomIndex - 1].count + 1
            }
            // console.log("",this.images[this.randomIndex - 1].count)

            // 每次收完卡片，需要进行简单检索，判断是否集齐了
            //需求：判断数组项的count，是否都大于0，只要有一个等于0，就意味着没集齐
            let flag: boolean = true // 假设集齐
            //验证是否集齐
            for (let item of this.images) {
              if (item.count == 0) {
                flag = false //没集齐
                break //后面没必要判断了
              }
            }
            // 设置是否中大奖的标志
            this.isGet = flag

            // 判断是否中奖了，如果是需要抽奖
            if (flag) {
              //我这里有3个大奖图片 (向下取整)
              let randomIndex: number = Math.floor(Math.random() * 4)
              // 我设置的数组里面有4个元素(图片)
              this.prize = this.arr[randomIndex]
            }

          })
      }
      //这是这3个控件居中
      .justifyContent(FlexAlign.Center)
      .width("100%")
      .height("100%")
      // 设置抽卡后的界面背景为黑色(颜色十六进制色值，如果是八位，前两位，就是透明度)
      .backgroundColor("#cc000000")
      // 设置层级(这才是关键，用来切换抽卡界面和非抽卡界面)
      .zIndex(this.maskZIndex)
      // 设置抽卡后界面的透明度(透明度是用来配合动画显示的)
      .opacity(this.maskOpacity)
      // 动画animation
      .animation({
        duration: 500 // 界面切换的时间(其实是透明度变化的时间)
      })


      // 抽大奖的遮罩层(仅在大奖时出现)
      if (this.isGet) {
        Column({ space: 20}) {
          // 从我的奖品里拿到对应的语句展示给用户
          Text(`恭喜获得${this.prizeMap.get(this.prize)}`)
            .fontColor("#f5ebcf") // 金色传说
            .fontSize(25)
            .fontWeight(700)
          Image($r(`app.media.${this.prize}`))
            .width(300)
            .borderRadius(10)
          Button("再来一次")
            .width(200)
            .height(50)
            .backgroundColor(Color.Transparent)
            .border({ width: 2, color: "# fff9e0"})
            // 点击事件
            .onClick(() => {
              this.isGet = false  // 重置中大奖标志为false
              this.prize = "" // 重置大奖的奖品为空
              // 视频里面是这样重置数组，这里实际上就是重新创建一个数组，对空间开销大，
              // 但是也只有这样能够刷新卡片控件
              this.images = [
                { url: "app.media.sercet1", count: 0},
                { url: "app.media.sercet2", count: 0},
                { url: "app.media.sercet3", count: 0},
                { url: "app.media.sercet4", count: 0},
                { url: "app.media.sercet5", count: 0},
                { url: "app.media.sercet6", count: 0},
              ]
              // // 遍历奖励池(重置数组)
              // for (let item of this.images) {
              //   item.count = 0 // 重置抽卡次数
              // }
            })
        }// 抽大奖的遮罩层
        .justifyContent(FlexAlign.Center) //整体布局居中
        .width("100%")
        .height("100%")
        .backgroundColor("#cc000000")
      }
    }
  }
}