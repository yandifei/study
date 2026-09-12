/*Flex换行- wrap
wrap属性：Flex 是单行布局还是多行布局
1.FlexWrap.NoWrap   单行布局
2.FlexWrap.Wrap     多行布局
 */
@Entry
@Component
struct Index {
  build() {
    //Flex布局：伸缩布局。当子盒子的总和溢出父盒子，默认进行压缩显示。
    //4。换行wrap
    // FlexWrap.Wrap换行
    // FlexWrap.NoWrap不换行
    Flex({
      wrap: FlexWrap.Wrap
    }) {
      Text()
        .width(80).height(80)
        .backgroundColor(Color.Pink)
        .border({ width: 1, color: Color.Blue })
      Text()
        .width(80).height(80)
        .backgroundColor(Color.Pink)
        .border({ width: 1, color: Color.Blue })
      Text()
        .width(80).height(80)
        .backgroundColor(Color.Pink)
        .border({ width: 1, color: Color.Blue })
      Text()
        .width(80).height(80)
        .backgroundColor(Color.Pink)
        .border({ width: 1, color: Color.Blue })
      Text()
        .width(80).height(80)
        .backgroundColor(Color.Pink)
        .border({ width: 1, color: Color.Blue })
    }
    .width(300)
    .height(300)
    .backgroundColor('#5f9a5c')
  }
}