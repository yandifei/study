/*文字溢出省略号、行高
1.文字溢出省略（设置文本超长时的显示方式）
语法: .textOverflow({
  overflow:TextOverflow.XXX
})
注意：需要配合.maxLines(行数）使用
 */

let introduction: string = "ArkTS是HarmonyOS应用开发的官方高级语言。\n" +
  "ArkTS在TypeScript（简称TS）生态基础上做了进一步扩展，保持了TS的基本风格，同时通过规范定义强化开发期静态检查和分析，提升代码健壮性，并实现更好的程序执行稳定性和性能。对比标准TS的差异可以参考从TypeScript到ArkTS的适配规则。ArkTS同时也支持与TS/JavaScript（简称JS）高效互操作。\n" +
  "ArkTS基础类库和容器类库增强了语言的基础功能，提供包括高精度浮点运算、二进制Buffer、XML生成解析转换和多种容器库等能力，协助开发者简化开发工作，提升开发效率。\n" +
  "针对TS/JS并发能力支持有限的问题，ArkTS对并发编程API和能力进行了增强，提供了TaskPool和Worker两种并发API供开发者选择。另外，ArkTS进一步提出了Sendable的概念来支持对象在并发实例间的引用传递，提升ArkTS对象在并发实例间的通信性能。\n" +
  "方舟编译运行时（ArkCompiler）支持ArkTS、TS和JS的编译运行，目前主要分为ArkTS编译工具链和ArkTS运行时两部分。ArkTS编译工具链负责将高级语言编译为方舟字节码文件（*.abc），ArkTS运行时则负责在设备侧运行字节码文件，执行程序逻辑。\n" +
  "未来，ArkTS会结合应用开发/运行的需求持续演进，逐步提供并发能力增强、系统类型增强、分布式开发范式等更多特性。"

@Entry
@Component
struct Index {
  @State message: string = "你好雁低飞";
  // 构建 -> 界面
  build() {
    Column() {
      Text("ArkTS简介")
        .width("100%")
        .lineHeight(50)
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
      Text(introduction)
        .width("100%")
        .lineHeight(24) //设置文本的行高
          // textOverflow传入进去的是一个对象
        .textOverflow({
          // overflow: TextOverflow.Ellipsis //文字溢出就省略
          // Clip = None这两个效果式一样的
          // overflow: TextOverflow.Clip //文字溢出直接裁剪
          // overflow: TextOverflow.None //文字溢出直接裁剪
          //文字无论是否溢出都变成单行滚动来展示全部(神人啊，maxLines直接无效)
          overflow: TextOverflow.MARQUEE
        })
          // 必须配合maxLines才有效果
        .maxLines(2)
    }
    .width("100%")
  }
}