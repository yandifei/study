// 等待页面加载完成后执行
window.onload = function () {
    let index = 0; // 设置当前显示的图片索引
    let mytime;    // 设置定时器全局变量

    // 1. 获取所有的 DOM 元素
    let imgs = document.querySelectorAll(".carousel-img"); // 获取所有图片容器
    let ul = document.querySelector(".carousel-select-ul"); // 获取小圆点的父容器
    let leftBtn = document.querySelector(".turn-left");    // 获取左按钮
    let rightBtn = document.querySelector(".turn-right");  // 获取右按钮

    // 2. 动态生成小圆点（根据图片的数量）
    for (let i = 0; i < imgs.length; i++) {
        let li = document.createElement("li");
        li.classList.add("carousel-select-ul-li");
        li.dataindex = i; // 给 li 绑定自定义属性记录索引
        ul.appendChild(li);
    }

    // 获取刚生成的圆点列表
    let lis = document.querySelectorAll(".carousel-select-ul-li");

    // 3. 核心功能函数

    // 隐藏所有图片和重置圆点样式
    function hideall() {
        for (let i = 0; i < imgs.length; i++) {
            // 通过修改 opacity 实现淡入淡出（配合 CSS 中的 transition）
            imgs[i].style.opacity = "0";
            // 恢复圆点默认样式
            lis[i].style.backgroundColor = "#00000050";
            lis[i].style.boxShadow = "none";
        }
    }

    // 显示当前索引对应的图片和圆点
    function showindex() {
        hideall(); // 先隐藏全部
        imgs[index].style.opacity = "1"; // 显示当前图片
        // 设置当前圆点高亮样式
        lis[index].style.backgroundColor = "white";
        lis[index].style.boxShadow = "0 0 0 3px #00000020";
    }

    // 自动播放函数
    function play() {
        mytime = setInterval(function () {
            index++;
            if (index >= imgs.length) {
                index = 0; // 播到最后一张后回到第一张
            }
            showindex();
        }, 3000); // 每3秒切换一次
    }

    // 停止播放函数
    function stop() {
        clearInterval(mytime);
    }

    // 4. 事件绑定

    // 鼠标移入图片区域停止播放，移出恢复
    for (let i = 0; i < imgs.length; i++) {
        imgs[i].onmouseover = stop;
        imgs[i].onmouseleave = play;
    }

    // 圆点点击/悬浮切换
    for (let i = 0; i < lis.length; i++) {
        lis[i].onmouseover = function () {
            stop();
            index = this.dataindex; // 更新索引为当前圆点索引
            showindex();
        };
        lis[i].onmouseleave = play;
    }

    // 左按钮点击切换
    leftBtn.onclick = function () {
        stop();
        index--;
        if (index < 0) {
            index = imgs.length - 1; // 回到最后一张
        }
        showindex();
        play();
    };

    // 右按钮点击切换
    rightBtn.onclick = function () {
        stop();
        index++;
        if (index >= imgs.length) {
            index = 0; // 回到第一张
        }
        showindex();
        play();
    };

    // 5. 初始化执行
    showindex(); // 初始显示第一张
    play();      // 开始自动播放
};