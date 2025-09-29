/*swiper 轮播组件
swiper 是一个容器组件，当设置多个子组件后，可以对这些子组件进行轮播显示。（文字、图片....）
学习目录：
1. Swiper 的基本用法
2. Swiper 的常见属性
3. Swiper 样式自定义
4. 案例：小米有品
5. 作业： 手机淘宝
*/


/* Swiper样式自定义

 */

/*需求：使用上述属性，将刚刚的轮播图调整为：
1. 自动播放
2. 播放间隔： 4秒钟
3. 纵向滑动
 */
@Entry
@Component
struct Index {

  build() {
    Column() {
      // Swiper 轮播组件的基本使用
      // 1. Swiper 包内容
      // 2. Swiper 设尺寸
      Swiper() {
        Text("1")
          .backgroundColor(Color.Orange)
        Text("2")
          .backgroundColor(Color.Yellow)
        Text("3")
          .backgroundColor(Color.Brown)
      }
      .width("100%")
      .height(100)
      // .loop(false) // 是否执行循环轮播（）
      .autoPlay(true) //开启自动轮播
      .interval(1500) //设置自动轮播的时间（默认3秒）
      .vertical(true) // 纵向轮播

      Swiper() {
        Image($r("app.media.arisu1"))
        Image($r("app.media.arisu2"))
        Image($r("app.media.arisu3"))
        Image($r("app.media.arisu4"))
        Image($r("app.media.arisu5"))
      }
      .width("100%")
      .height(300)
      // 设置轮播下面的原点样式（颗粒度控制强）
      .indicator(
        Indicator.dot()
          .itemWidth(20)
          .itemHeight(20)
          .color(Color.Blue)  //设置原点颜色
      )


    }
    .height('100%')
    .width('100%')
  }
}

