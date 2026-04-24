fetch('/status/json')
    .then(response => response.json())
    .then(data => {
        // 实时监控区域
        const monitorGrid = document.getElementById('monitor-grid');
        monitorGrid.innerHTML = '';

        data.monitor.forEach((link, index) => {
            const card = document.createElement('a');
            card.href = link;
            card.className = 'monitor-card';
            card.target = '_blank';
            card.innerHTML = `
                <div>实例 ${index + 1}</div>
                <small>实时画面</small>
            `;
            monitorGrid.appendChild(card);
        });

        // 截图区域
        const screenshotGrid = document.getElementById('screenshots-grid');
        screenshotGrid.innerHTML = '';

        data.screenshots.forEach((link, index) => {
            const card = document.createElement('a');
            card.href = link;
            card.className = 'screenshot-card';
            card.target = '_blank';
            card.innerHTML = `
                <div>实例 ${index + 1}</div>
                <small>最新截图</small>
            `;
            screenshotGrid.appendChild(card);
        });
    })
    .catch(err => {
        console.error('获取状态失败', err);
        // 可选：显示错误提示卡片
    });