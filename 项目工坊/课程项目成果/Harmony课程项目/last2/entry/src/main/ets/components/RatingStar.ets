
// 使用@Component装饰器定义一个UI组件
@Component
// 导出RatingStar结构体
export struct RatingStar {
  // 定义静态常量：单个星星的高度(11vp)
  private static readonly STAR_HEIGHT: number = 11;
  // 定义静态常量：星星图片的宽度(55vp)
  private static readonly STAR_IMG_WIDTH: number = 55;
  // 定义静态常量：星星图片的总高度(121vp)，包含11行星星图像，每行11vp
  private static readonly STAR_IMG_HEIGHT: number = 121; // 11 rows * 11vp/row
  
  // 定义组件属性：评分值，使用@Prop装饰器表示这是从父组件传递过来的属性
  @Prop rating: number;
  
  // 计算星星图像在垂直方向上的偏移量的方法
  calculateStarRowOffset(ratingValue: number): number {
    // 检查评分值是否为空或NaN，如果是则返回0偏移量(显示0星)
    if (ratingValue == null || isNaN(ratingValue)) {
      return 0;
    }
    
    // 将评分值限制在有效范围内(0-5星)
    const clampedRating = Math.min(Math.max(ratingValue, 0), 5);
    
    // 计算星图偏移量：
    // 1. 将评分值乘以2得到星级索引(支持半星显示)
    // 2. 用10减去星级索引得到行索引(图片从下往上显示不同星级)
    // 3. 乘以STAR_HEIGHT得到实际的像素偏移量
    const starIndex = Math.round(clampedRating * 2);
    const rowIndex = -(10 - starIndex) * RatingStar.STAR_HEIGHT;
    
    // 返回计算后的偏移量
    return rowIndex;
  }
  
  // 构建UI界面
  build() {
    // 使用Stack布局容器
    Stack() {
      // 显示星星图片资源
      Image($r('app.media.ic_rating_s'))
        // 设置图片宽度
        .width(RatingStar.STAR_IMG_WIDTH)
        // 设置图片高度
        .height(RatingStar.STAR_IMG_HEIGHT)
        // 设置图片垂直偏移量，通过calculateStarRowOffset方法计算得出
        .offset({
          y: this.calculateStarRowOffset(this.rating ?? 0)
        })
    }
    // 设置Stack内容对齐方式为顶部对齐
    .align(Alignment.Top)
    // 设置Stack宽度
    .width(RatingStar.STAR_IMG_WIDTH)
    // 设置Stack高度
    .height(RatingStar.STAR_HEIGHT)
    // 启用裁剪，只显示当前星级对应的星星图像部分
    .clip(true)
  }
}