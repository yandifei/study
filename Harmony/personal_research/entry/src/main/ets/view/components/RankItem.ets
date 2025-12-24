/*RankItem.ets
 单个排名列表
*/
import { ShowModel } from "../../data/ShowModel";
import { PixivImage } from "./PixivImage";

@Component
export struct RankItem {
  @Prop show_model: ShowModel;

  build() {
    // 单个排行榜列表
    Row() {
        PixivImage({ url: this.show_model.image_url ?? "" })
          .width('100%')
          .backgroundColor(Color.Blue)
          .border({ width: 1, color: Color.Grey, radius: 5 })
    }
    .width('100%')
    .height('100%')
  }
}