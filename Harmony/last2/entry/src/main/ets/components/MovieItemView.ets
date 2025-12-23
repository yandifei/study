import { MovieItem } from '../model/DoubanModels';
import { RatingStar } from '../components/RatingStar';


@Component
export struct MovieItemView {
  @Prop movie: MovieItem;
  build() {
    Column() {
      Row() {
        Image(this.movie.pic?.normal ?? '')
          .width(100)
          .height(150)
          .objectFit(ImageFit.Contain)
          .margin({ right: 10 })
        Column() {
          Text(this.movie.title)
            .fontSize(18)
            .fontWeight(FontWeight.Bold)
            .fontColor('#ff2157d4')
          Text(this.movie.card_subtitle)
            .fontSize(15)
            .fontColor(Color.Black)
            .margin({ top: 8, bottom: 8 })
            .maxLines(3)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
          Row() {
            RatingStar({ rating: this.movie.rating?.star_count ?? 0 })
            Text(`${this.movie.rating?.value ?? 'N/A'}`)
              .fontSize(15)
              .fontColor(Color.Orange)
              .margin({ left: 5 })
          }
          .alignItems(VerticalAlign.Center)
        }.alignItems(HorizontalAlign.Start).layoutWeight(1)
      }.padding(10)
      Divider()
    }

  }
}
