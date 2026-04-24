document.querySelector('.theme-toggle')?.addEventListener('click', (e) => {
    const html = document.documentElement;
    const btn = e.currentTarget; // 获取当前点击的按钮

    if (html.getAttribute('data-theme') === 'light') {
        html.setAttribute('data-theme', 'dark');
        btn.textContent = '🌙 切换主题'; // 切换为太阳
    } else {
        html.setAttribute('data-theme', 'light');
        btn.textContent = '☀️ 切换主题'; // 切换为月亮
    }
});

// 刷新页面
setInterval(function() {
    location.reload();
}, 1000); // 1000毫秒 = 1秒

// 简易主题切换（可选）
// document.querySelector('.theme-toggle')?.addEventListener('click', () => {
//     const html = document.documentElement;
//     if (html.getAttribute('data-theme') === 'light') {
//         html.setAttribute('data-theme', 'dark');
//     } else {
//         html.setAttribute('data-theme', 'light');
//     }
// });