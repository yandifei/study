// 监听页面load事件，在页面所有元素加载完成后才触发该事件
window.onload=function(){
	// 获取HTML文档中的元素，并赋值给声明的变量
	var wrap= ,
		pic= ,
		list= ,
		index=0,
		timer=null;
		
	// 定义图片切换函数
	function changePic (curIndex) {
		for (var i = 0; i < pic.length; ++i) {
			pic[i].style.display = ;
			list[i].className = ;
		}
		pic[curIndex].style.display = ;
		list[curIndex].className = ;
	}
	
	// 定义自动播放函数
	function autoPlay () {
		//计算下一张图片id，超限则从第一张开始
		if (++index >= pic.length) {
			
		}
		//切换图片
		
	}
 
	// 调用自动播放函数
	timer = ;	// 设置定时器，按照指定的周期（2秒）调用自动播放函数autoPlay
 
	// 鼠标划过整个轮播图区域时停止自动播放
	wrap.onmouseover = function () {
						// 取消setInterval设置的定时器
	}
 
	// 鼠标离开整个容器时继续播放至下一张
	wrap.onmouseout = function () {
		timer = ;
	}
	
	// 遍历所有数字导航实现划过切换至对应的图片
	for (var i = 0; i < list.length; i++) {
		list[i].onmouseover = function () {
			//停止自动播放
			
			//计算图片的index
			index = this.innerText - 1;
			//切换图片
			
		}
	}
}