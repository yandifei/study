/*67-ForEach渲染控制
ForEach-渲染控制
ForEach可以基于数组的个数，渲染组件的个数。（简化代码）
循环渲染列表结构
*/
//超级爽 ，不过我得要手动指定item的数据类型，我估计编译器确实没办法对item这个类型进行静态检查
//ForEach中的item参数还真是我第一个见到需要我进行类型断言的参数

// ForEach案例一新闻列表，因为我没有黑马那边的资料所以这个内容我没法写（视频里面也把源代码给合起来了，我没没法抄UI样式过来了）
// 这里缺少了这个新闻列表案例，实际也不重要，拿现在之前写的案例拼凑练练手


@Entry
@Component
struct Index {
  // 定义一个需要渲染的数组
  @State titles: string[] = ["电子产品", "精品服饰", "母婴产品", "影音娱乐", "海外旅游"]
  build() {
    Column() {
      // 核心代码
      //this.titles是一个数组,后面一个参数就相当于一个元组(数组的元素，数组的下标)，最后一个参数就是一个模板
      ForEach(this.titles, (item: string, index: number) => {
        //这里就相当于一个样本（我记得我在PyQt6里面也这么干过）
        Text(`${index} ${item}`)
          .fontSize(24)
          .fontWeight(700)
          .fontColor(Color.Orange)
          .padding(15)
          .width("100%")
      })
    }
  }
}