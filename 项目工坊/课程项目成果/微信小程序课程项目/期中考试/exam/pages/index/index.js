// index.js
Page({
  data: {
    loading: true,          // 控制加载状态
    banners: [               // 轮播图数据
      { id:1, src:'/pages/images/index/广东粤剧.jpg' },
      { id:2, src:'/pages/images/index/广东醒狮.jpg' },
      { id:3, src:'/pages/images/index/广东早茶.jpg' },
    ],
    heat: 0,                // 进度条百分比
    cultureImages: [         // 文化图片数据
    { id:1, src:'/pages/images/index/广东粤剧2.jpg', title:'粤剧', content:'粤剧，又称广东大戏，是岭南文化的瑰宝，也是广东最具代表性的传统戏剧。它源自南戏，流行于广东、广西及港澳地区。粤剧不仅是人类非物质文化遗产，更融合了唱念做打、红船、南派武术等独特元素。粤剧的舞台脸谱与华丽戏服是广府人乡愁的寄托。' },
    { id:2, src:'/pages/images/index/广东醒狮2.jpg', title:'醒狮', content: '醒狮是中国狮舞中的南狮，集武术、舞蹈、音乐于一体，是广东民间节庆的灵魂担当。锣鼓一响，雄狮起舞，采青仪式寓意吉祥如意。醒狮展现了广东人敢为人先、勇于拼搏的精气神。'},
    { id:3, src:'/pages/images/index/广东早茶2.jpg', title:'早茶', content: '叹早茶是广东人独特的生活方式，一盅两件，一壶好茶配上几笼热气腾腾的点心。早茶经典点心中的三大天王是虾饺、肠粉、烧卖。'}
    ]
  },
  
  onLoad() {
    // 显示 loading，模拟加载过程
    wx.showLoading({ title: '加载中...' });

    // 启动进度条，接上计时器的异步
    this.startProgressAnimation(100);

    setTimeout(() => {
      wx.hideLoading();
      this.setData({ loading: false });   // 隐藏加载状态，显示内容
    }, 1500);
  },

  // 进度条推进
  startProgressAnimation(target) {
    let current = this.data.heat;
    const step = () => {
      if (current < target) {
        current++;
        this.setData({ heat: current });
        setTimeout(step, 20);  // 每 20ms 增加 1，2 秒左右到 100
      }
    };
    step();
  }
});