import { MovieItemView } from '../components/MovieItemView';
import { CategoryDataItem, MovieItem } from '../model/DoubanModels';
import { MovieViewModel } from '../model/MovieViewModel';
@Entry
@Component
struct Index {
  @State vm: MovieViewModel = new MovieViewModel();
  async aboutToAppear() {
    await this.vm.fetchData(true);
  }

  build() {
    Column({ space: 10 }) {
      Row() {
        if (this.vm.typeCategory && this.vm.regionCategory) {
          Row({ space: 5 }) {
            Text('类型:')
            Select(this.vm.typeCategory?.data.map((item: CategoryDataItem)=>({value: item.text,
              text: item.text
            } as SelectOption)) ?? [])
              .value(this.vm.selectedType === '' ?(this.vm.typeCategory?.data[0]?.text ?? '') : this.vm.selectedType)
              .selected(this.vm.selectedType === '' ? 0:(this.vm.typeCategory?.data.findIndex(item => item.text ===this.vm.selectedType) ?? -1))
              .onSelect(async (index: number) => {
                console.info(`[DoubanMovie Index] Type selected. Newindex:${index}`);
                this.vm.selectedType = index === 0 ? '':this.vm.typeCategory?.data[index]?.text ?? '';
                await this.vm.fetchData(true);
              })
              .fontColor(Color.Black)
              .selectedOptionFontColor(Color.Blue)
              .backgroundColor(Color.White)
            // 地区抉择
            Select(this.vm.regionCategory?.data.map((item: CategoryDataItem)=>({value: item.text,
              text: item.text
            } as SelectOption)) ?? [])
              .value(this.vm.selectedRegion === '' ?(this.vm.regionCategory?.data[0]?.text ?? '') : this.vm.selectedRegion)
              .selected(this.vm.selectedRegion === '' ? 0:(this.vm.regionCategory?.data.findIndex(item => item.text ===this.vm.selectedRegion) ?? -1))
              .onSelect(async (index: number) => {
                console.info(`[DoubanMovie Index] Type selected. Newindex:${index}`);
                this.vm.selectedRegion = index === 0 ? '':this.vm.regionCategory?.data[index]?.text ?? '';
                await this.vm.fetchData(true);
              })
              .fontColor(Color.Black)
              .selectedOptionFontColor(Color.Blue)
              .backgroundColor(Color.White)
          }.alignItems(VerticalAlign.Center)
        }
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceEvenly)
      .padding(10)
      .height(60)
      .backgroundColor('#f0f0f0')
      List({ space: 10 }) {
        ForEach(this.vm.movies, (item: MovieItem) => {
          // 电影列表
          MovieItemView({ movie: item })
        }, (item: MovieItem) => item.id)
        // MovieItemView({ movie: this.vm.movies[0] })
      }
      .layoutWeight(1)
      .width('90%')
      .divider({ strokeWidth: 1, color: '#e0e0e0' })
      .onScrollIndex(async (start, end) => {
        if (!this.vm.isLoading && end === this.vm.movies.length -1){await this.vm.loadMore();
        }
      })


    }
    .width('100%')
    .height('100%')
    .padding({ bottom: 10 })
  }
}