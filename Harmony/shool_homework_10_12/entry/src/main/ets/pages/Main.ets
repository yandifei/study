// 定义接口 （每个列表项的数据结构）
interface friendList {
  imagePath: string // 好友图像路径
  name: string    // 好友名
  lastTime: string //最后的聊天时间
  lastMessage: string // 最后的消息
}
// 定义列表
let friend_list: friendList[] = []
// for来添加
for (let i = 1; i < 12; i++) {
  friend_list.push({
    imagePath: `/friend_image/f${i}.png`,
    name: `爱丽丝${i}`,
    lastTime: `10月${i}日`,
    lastMessage: "莫西莫西"
  })
}
// [
//   {imagePath: "1", name: "1", lastTime:"1", lastMessage: "1"},
//   {imagePath: "1", name: "1", lastTime:"1", lastMessage: "1"},
//   {imagePath: "1", name: "1", lastTime:"1", lastMessage: "1"},
//   {imagePath: "1", name: "1", lastTime:"1", lastMessage: "1"},
//   {imagePath: "1", name: "1", lastTime:"1", lastMessage: "1"},
//   {imagePath: "1", name: "1", lastTime:"1", lastMessage: "1"},
//   {imagePath: "1", name: "1", lastTime:"1", lastMessage: "1"},
// ]
@Entry
@Component
struct Main {
  // 导航头
  @State menuItems:Array<NavigationMenuItem> = [
    { value:'menuItem2', icon: $r("app.media.plus") }
  ]
  // 底部工具栏
  @State toolBar: Array<ToolbarItem> = [
    {
      "value": "消息",
      "icon": $r("app.media.message"),
      "action": () => {},
      // symbolIcon: new SymbolGlyphModifier($r('sys.symbol.ohos_lungs')),
      // "status": ToolbarItemStatus.ACTIVE,
      // "activeSymbolIcon": new SymbolGlyphModifier($r('app.media.message')).fontColor([Color.Red]).renderingStrategy(SymbolRenderingStrategy.MULTIPLE_COLOR),
    },
    {
      "value": "好友",
      "icon": $r("app.media.person_badge_plus"),
      "action": () => {}
    },
    {
      "value": "设置",
      "icon": $r("app.media.settings"),
      "action": () => {}
    }
  ]

  // 扩大搜索框的范围
  @State isSearchFocus: boolean = false

  //好友列表
  // @State friend_list: friendList[] = [{imagePath: "/friend_image/f1.png", name: "1", lastTime:"1", lastMessage: "1"}]
  @State friend_list: friendList[] = friend_list

  build() {
    Column(){
      Navigation() {
        Column() {
          // 搜索框
          Row() {
            // 搜索矢量图标设置高度和颜色
            Image($r("app.media.search")).height("3%").fillColor(Color.Gray)
              .padding({left: "40%"})
            TextInput({ placeholder: "搜索"}).backgroundColor(Color.Transparent)
              .padding({ left: 0 }) // 缩去和搜索图标的距离
              .defaultFocus(this.isSearchFocus)
              .focusOnTouch(true)
                // 确保当输入框获得焦点后，将isSearchFocus重置为false避免持续触发
              .onFocus(() => {
                this.isSearchFocus = false;
              })
          }
          .backgroundColor("#f4f6f5").borderRadius(20)
          .onClick(() => {
            console.log("1", this.isSearchFocus)
            this.isSearchFocus = true
            console.log("1", this.isSearchFocus)
          })
        }
        .padding({ left: 10, right: 10, bottom: 10})

        // 好友滚动列表
        List() {
          ForEach(this.friend_list, (item: friendList, index: number) => {
            // 单个好友列表
            ListItem() {
              Row() {
                Image(item.imagePath).width(40).borderRadius(5) // 好友头像
                Column({ space: 7 }) { // 好友名和最后消息的间隔
                  Row() {
                    Text(item.name).fontSize(17).fontWeight(FontWeight.Bold) // 好友名
                    Text(item.lastTime).fontColor("#8bcccccc") // 日期字体颜色要比最后消息淡
                  }.width("80%").justifyContent(FlexAlign.SpaceBetween)

                  // 最后消息为灰色(默认居左)
                  Text(item.lastMessage).width("80%").fontColor("#ccc").fontSize(14)
                }
              }
              .width("100%")
              // .margin(5)
              .padding(7)
              .border({
                width: {
                  left: 0,
                  right: 0,
                  top: 3,
                  bottom: 0
                }, //边框大小(必须配置边框大小)
                color: "#ccc", //颜色为红色
              })
              .justifyContent(FlexAlign.SpaceBetween) // 分隔对齐
            }
          })
        }
      }
      .mode(NavigationMode.Auto)
      .menus(this.menuItems)
      .toolbarConfiguration(this.toolBar)
      // .menus([{value: "", icon: "B:\\HarmonyStudy\\homework_10_12\\entry\\src\\main\\resources\\base\\media\\Main\\xmark_circle.svg", action: () => {}}])
      .title("通讯")
      .titleMode(NavigationTitleMode.Mini)
    }
    .linearGradient({
      /* angle这个参数用于指定渐变的方向。它的值以度（degrees）为单位。
      0: 渐变从左到右。
      90: 渐变从下到上。
      180: 渐变从上到下。这是您代码中使用的值。
      270: 渐变从右到左。
      */
      angle: 180, //视频里面是左上到右下的颜色过度
      // Explicitly define the color stops with their positions
      colors: [
        ['#46aeeac9', 0.1], ['#2fa295ae', 0.5], ['#9afee9e7', 1]
      ]
    })
  }
  // 禁用界面入场和出场有动画
  pageTransition() {
    PageTransitionEnter({ type: RouteType.None, duration: 0 })
    PageTransitionExit({ type: RouteType.None, duration: 0 })
  }
}