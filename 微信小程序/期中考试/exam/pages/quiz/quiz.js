// pages/quiz/quiz.js
Page({
  data: {
    dramaOptions: [
      { value: 'yueju', label: '粤剧', checked: false },
      { value: 'jingju', label: '京剧', checked: false },
      { value: 'yueju2', label: '越剧', checked: false }
    ],
    dimsumOptions: [
      { value: 'xiajiao', label: '虾饺', checked: false },
      { value: 'changfen', label: '肠粉', checked: false },
      { value: 'shaomai', label: '烧卖', checked: false },
      { value: 'xiaolongbao', label: '小笼包', checked: false }
    ],
    switchChecked: true,   // 判断题默认正确
    loveValue: 50,
    food: '',
    // 21个城市我全给你干齐，缺？不可能的
    cities: ['广州', '深圳', '佛山', '东莞', '珠海', 
    '中山', '江门', '肇庆', '惠州', '汕头', 
    '潮州', '揭阳', '汕尾', '湛江', '茂名', 
    '阳江', '云浮', '韶关', '清远', '梅州', '河源'],
    cityIndex: 0
  },

  cityChange(e) {
    this.setData({ cityIndex: e.detail.value });
  },

  // 表单提交，分数计算（看我阴你一手）
  submitQuiz(e) {
    const values = e.detail.value;
    // 
    let score = 0;

    // 单选题：正确答案 'yueju'（粤剧）
    if (values.drama === 'yueju') score += 30;

    // 多选题：完全正确（虾饺、肠粉、烧卖且不包含小笼包）
    const dimsum = values.dimsum || [];
    const correctSet = ['xiajiao', 'changfen', 'shaomai'];
    const wrongSelected = dimsum.includes('xiaolongbao');
    const allCorrect = correctSet.every(v => dimsum.includes(v));
    if (allCorrect && !wrongSelected) score += 40;

    // 判断题：switch 值为布尔，正确得20分
    if (values.cantonese) score += 20;   // true 为正确

    // 滑块：每10分加1分，上限10分
    const love = parseInt(values.love) || 0;
    score += Math.floor(love / 10);

    // 没选广州直接扣50分（广州下标为0）
    if (values.city !== 0) score -= 50;

    wx.showModal({  
      title: '测验结果',
      content: `你的总分是：${score} 分`,
      showCancel: false
    });
  },

  resetQuiz() {
    wx.showToast({
      title: '已重置',
      icon: 'success',
      duration: 1500
    });
  }
})