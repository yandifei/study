/* 界面开发布局思路
 ArkUI（方舟开发框架）是一套构建鸿蒙应用界面的框架。
构建页面的最小单位就是“组件”。

组件分类：
①基础组件：界面呈现的基础元素。
如：文字、图片、按钮等。
②容器组件：控制布局排布。
如：Row行、Column列等。
布局思路：先排版，再放内容。
 */

/*组件语法：
①容器组件：行Row、列Column
容器组() {
  内容
}
基础组件：文字Text、图片
基础组件（参数）
 */


/*组件的属性方法
需求：美化组件外观效果→组件的属性方法
基础组件不需要{}，容器组件才加{}
组件() {}
  .属性方法1（参数）
  .属性方法2（参数）
  .属性方法3（参数）
  ......
 */

@Entry
@Component
struct Index {
  @State message: string = 'Hello World';
  //构建->界面
  build() {
    // 布局思路：先排版，再内容
    Column() {
      //内容
      Text("小说简介")
        .width("100%")  //Text控件的宽度大小(默认居中于Column)
        .height(40)
        .backgroundColor(Color.Gray)  //设置背景色
        .fontSize(20)
          // .fontWeight(FontWeight.Bold)
        .fontWeight(700) //100-900 ,加粗700 默认400

      Row() {
        Text("都市")
          .width(50)
          .height(30)
          .backgroundColor(Color.Orange)
        Text("生活")
          .width(50)
          .height(30)
          .backgroundColor(Color.Pink)
        Text("情感")
          .width(50)
          .height(30)
          .backgroundColor(Color.Yellow)
        Text("男频")
          .width(50)
          .height(30)
          .backgroundColor(Color.Gray)
      }
      .width("100%")

    }
    //背景色
    .backgroundColor(Color.Pink)
    //这个容器在整个屏幕中的百分比
    .width("100%") //也可以直接给数值(我估计数值是px单位)
  }
}
