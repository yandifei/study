/*Homework9.java -- 本章作业09*/
public class Homework9 {
	public static void main(String[] args)	 {
		// 定义Music类，里面有音乐名name、音乐时长times属性，并有播放play功能和返
		// 回本身属性信息的功能方法getlnfo
		Music music = new Music("你好",10000);
		music.play();
		System.out.println(music.getInfo());
	}
}

class Music {
	String name;
	double times;
	public Music(String name, double times) {
		this.name = name;
		this.times = times;
	}

	//播放功能play
	public void play() {
		System.out.println("音乐 " + name + " 正在播放.... 时长为" + times + "秒");
	}
	public String getInfo() {
		return "音乐名：" + this.name + " 音乐时长：" + this.times + "秒";
	}

}