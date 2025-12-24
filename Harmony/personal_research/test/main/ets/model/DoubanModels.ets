export interface DoubanResponse {
  // 电影数量的20
  count: number;
  // 这个是核心（电影核心）
  items: MovieItem[];
  // tags这个是电影类型
  recommend_categories: RecommendCategory[];
  // 总数
  total: number;
}

export interface MovieItem {
  id: string;
  title: string;
  card_subtitle: string;
  pic: Pic;
  rating: Rating;
}

export interface Pic {
  large: string;
  normal: string;
}

export interface Rating {
  count: number;
  max: number;
  star_count: number;
  value: number;
}

export interface RecommendCategory {
  is_control: boolean;
  type: string;
  data: CategoryDataItem[];
}

export interface CategoryDataItem {
  default: boolean;
  text: string;
}

