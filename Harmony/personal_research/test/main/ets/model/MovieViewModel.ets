import http from '@ohos.net.http';
import { DoubanResponse, MovieItem, RecommendCategory } from './DoubanModels';

@Observed
export class MovieViewModel {
  movies: MovieItem[] = [];
  typeCategory: RecommendCategory | null = null;
  regionCategory: RecommendCategory | null = null;
  selectedType: string = '喜剧';
  selectedRegion: string = '华语';
  isLoading: boolean = false;
  isRefreshing: boolean = false;
  private start: number = 0;
  private count: number = 20;
  private total: number = 0;
  fetchData(isRefresh: boolean): void {
    console.info(`[DoubanMovie VM] fetchData called. isRefresh: ${isRefresh},isLoading: ${this.isLoading}, movies.length: ${this.movies.length}`);if (this.isLoading) {
      console.info(`[DoubanMovie VM] Already loading, returning.`);
      return ;
    }
    if (isRefresh) {
      this.start = 0;
    }
    this.isLoading = true;
    let httpRequest = http.createHttp();
    const selectedCategories: Record<string, string> = {
      "类型": this.selectedType === '全部类型' ? '' : this.selectedType,"地区": this.selectedRegion === '全部地区' ? '' : this.selectedRegion};
    const activeTags: string[] = [];
    if (this.selectedType !== '全部类型') {
      activeTags.push(this.selectedType);
    }
    if (this.selectedRegion !== '全部地区') {
      activeTags.push(this.selectedRegion);
    }
    const tags = activeTags.join(',');
    const url =
      `https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=${this.start}&count=${this.count}&selected_categories=${encodeURIComponent(JSON.stringify(selectedCategories))}&uncollect=false&score_range=0,10&tags=${encodeURIComponent(tags)}`;
    console.info(`[DoubanMovie VM] Requesting URL: ${url}`);
    httpRequest.request(
      url,
      {
        method: http.RequestMethod.GET,
        header: {
          'accept': 'application/json, text/plain, */*',
          'accept-language': 'zh,zh-CN;q=0.9,en;q=0.8',
          'origin': 'https://movie.douban.com',
          'priority': 'u=1, i',
          'referer': 'https://movie.douban.com/explore',
          'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131","Not_ABrand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Linux"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-site',
          'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
      },
      (err, data) => {
        this.isLoading = false;
        if (!err) {
          console.info(`[DoubanMovie VM] Request successful. Data resulttype:${typeof data.result}`);
          try {
            const doubanResponse: DoubanResponse = JSON.parse(data.result as string);
            console.info(`[DoubanMovie VM] JSON parsed successfully. Itemslength:${doubanResponse.items.length}, Categories length:${doubanResponse.recommend_categories.length}`);
            if (isRefresh) {
              this.movies = doubanResponse.items;
              if (!this.typeCategory || !this.regionCategory) {
                this.typeCategory = doubanResponse.recommend_categories.find(c=>c.type === '类型') ?? null;
                this.regionCategory = doubanResponse.recommend_categories.find(c=> c.type === '地区') ?? null;
              }
            } else {
              this.movies.push(...doubanResponse.items);
            }
            this.start += this.count;
            this.total = doubanResponse.total;
            console.info(`[DoubanMovie VM] Movies array updated. Newlength:${this.movies.length}, total: ${this.total}`);
          } catch (e) {
            console.error(`[DoubanMovie VM] JSON parsing failed:${JSON.stringify(e)}`);
          }
        } else {
          console.error(`[DoubanMovie VM] Request failed:${JSON.stringify(err)}`);
        }
        httpRequest.destroy();
      }
    );
  }
  async loadMore() {
    if (this.start < this.total) {
      await this.fetchData(false);
    }
  }

}
