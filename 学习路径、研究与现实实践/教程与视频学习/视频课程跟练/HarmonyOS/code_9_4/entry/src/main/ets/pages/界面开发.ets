

/*界面开发起步
今天是9.17，我看黑马的鸿蒙开发，由于我的DevEco Studio版本是最新的，所以和视频中构建初始的界面源码不同
视频build下面是有Row()等关键字的，我这里就仅仅只有RelativeContainer()，弹幕说是加了这个相对布局控件。
相对布局控件有自动对齐
 */
@Entry
@Component
struct Index {
  @State message: string = "你好雁低飞";
  // 构建 -> 界面
  build() {
    //相对布局控件(相对容器)
    RelativeContainer() {
      /* 文本 函数名(参数) 对象.方法名(参数)
      【其实这里就是链式调用，第一次见到如此逆天的多级方法调用，还真没认出来】
      */
      Text(this.message)
        .id('HelloWorld')
          //设置字体大小(默认值:$r('app.float.page_text_font_size'))
        .fontSize(70)
          //字体粗细(默认值：FontWeight.Bold 其实这个默认值就是一个枚举类型【我干脆叫映射或字典更好】)
        .fontWeight(FontWeight.Bolder)
          /*这里在源代码外给他加多一个颜色*/
        .fontColor(Color.Blue)  //设置文本颜色为蓝色
          // 对齐规则(黑马没有讲这里，其实到这里和CSS样式表极其的相似)
        .alignRules({
          center: { anchor: '__container__', align: VerticalAlign.Center },
          middle: { anchor: '__container__', align: HorizontalAlign.Center }
        })
          // 点击后就进行一个函数的回调(界面的文本改变，黑马没讲)【这里居然没有信号和槽，Qt思想报废】
        .onClick(() => {
          this.message = 'Welcome';
        })
    }
    //界面大小(黑马没讲  )
    .height('100%')
    .width('100%')
  }
}