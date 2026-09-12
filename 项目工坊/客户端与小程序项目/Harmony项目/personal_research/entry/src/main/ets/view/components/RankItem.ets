/*RankItem.ets
 单个排名列表
*/
import { ShowModel } from "../../data/ShowModel";
import { PixivImage } from "./PixivImage";
@Component
export struct RankItem {
  // @Prop show_model?: ShowModel  // 允许 undefined,防止使用了Prop在没有拿到数据的时候就开始渲染导致崩溃
  @Prop show_model: ShowModel

  build() {
    // 防崩
    // if (!this.show_model) {
    //   // ✅ 占位UI：你想显示啥都行
    //   Row() {
    //     Text('加载中...')
    //   }
    //   .width('100%')
    //   .height('100%')
    //   return
    // }

    // 单个排行榜列表
    Row() {
      // // 排行
      // Text(this.show_model.rank.toString())
      //   .width(20)
      //   .height(20)

      //设置单个栅栏控件
        // 设置圆点红标
        Badge({
          count: this.show_model.rank, // 数量为0不显示红标
          position: BadgePosition.RightTop, //设置小圆圈位置为右上角
          style: {
            badgeSize: 20,
            fontSize: 14,
            badgeColor: Color.Blue
          }
        })
        //设置栅栏控件的主要内容
        {
          // 正方形(图像)
          PixivImage({ url: this.show_model.image_url!})
            .width(100) // 宽高一致
            .height(100) // 宽高一致
            .backgroundColor(Color.Blue)
              // .border({ width: 1, color: Color.Grey, radius: 5 })
            .onClick(() => {console.info(JSON.stringify(this.show_model))})
            .borderRadius(100)
        }


      Column() {
        // 作品名
        Text(this.show_model.title)
          .width('100%')
          .fontSize(16)           // 设置字体大小
          .fontWeight(FontWeight.Bold)  // 设置字体粗细
          .fontColor(Color.Black)       // 设置字体颜色
          .fontStyle(FontStyle.Normal)  // 设置字体样式（正常/斜体）
        Row(){
          // 作者头像
          PixivImage({ url: this.show_model.author_img ?? "" })
            .width(30).height(30).borderRadius(25)
            // .backgroundColor(Color.Red)          // 作者名
          Text(this.show_model.author).width('50%')
            .fontSize(10)           // 设置字体大小
        }
        .justifyContent(FlexAlign.Start)
        .width('100%')
        // .backgroundColor(Color.Blue)
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceBetween)
      .margin({left: 10})
    }
    .width('100%')
    .height('100%')
    // .justifyContent(FlexAlign.Start)
    .borderWidth({ bottom: 3 })
    .borderColor({ bottom: Color.Gray })
  }
}