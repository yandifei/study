import { MovieItem } from '../model/DoubanModels';
import { MovieViewModel } from '../model/MovieViewModel';
@Entry
@Component
struct Index {
  @State vm: MovieViewModel = new MovieViewModel();
  build() {
    Column({ space: 10 }) {
      Row({ space: 10 }) {
        Button('刷新电影列表')
          .fontSize(20)
          .margin({ top: 30 })
          .width('50%')
          .height(50)
          .fontColor(Color.White)
          .onClick(() => {
            this.vm.fetchData(true);
          })
        Button('清除')
          .fontSize(20)
          .margin({ top: 30 })
          .height(50)
          .fontColor(Color.White)
          .onClick(() => {
            this.vm.movies = [];
          })
      }
      List({ space: 10 }) {
        ForEach(this.vm.movies, (item: MovieItem) => {
          ListItem() {
            Text(item.title + '，评分：' + item.rating?.value)
              .fontSize(18)
              .width('100%')
              .padding(10)
          }
        }, (item: MovieItem) => item.id)
      }
      .layoutWeight(1)
      .width('90%')
      .divider({ strokeWidth: 1, color: '#e0e0e0' })
    }
    .width('100%')
    .height('100%')
    .padding({ bottom: 10 })
  }
}