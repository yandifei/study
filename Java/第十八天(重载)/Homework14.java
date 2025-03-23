/*Homework14.java -- 章节练习14*/
import java.util.Random; //导入随机数的包
public class Homework14 {
	public static void main(String[] args) {
	// 扩展题，学员自己做
	// 有个人Tom设计他的成员变量，成员方法，可以电脑猜拳。
	// 电脑每次都会随机生成0，1,2
	// 0表示石头 1表示剪刀 2表示布
	// 并要可以显示Tom的输赢次数（清单）
		Person Tom = new Person();
		Person challenger = new Person();
		System.out.println("轮次" + "\tTom" + "\tchallenger" + "\tTom赢的次数");
		for(int i = 1; i <= 10; i++) {
			if(Tom.Throw() == 0 && challenger.Throw() == 1) {
				Tom.winTimes ++;
				challenger.defeatTimes ++;
				System.out.println("第" + i + "轮\t赢\t输\t\t" + Tom.winTimes);
			} else if(Tom.Throw() == 1 && challenger.Throw() == 2)  {
				Tom.winTimes ++;
				challenger.defeatTimes ++;
				System.out.println("第" + i + "轮\t赢\t输\t\t" + Tom.winTimes);
			} else if(Tom.Throw() == 2 && challenger.Throw() == 0) {
				Tom.winTimes++;
				challenger.defeatTimes++;
				System.out.println("第" + i + "轮\t赢\t输\t\t" + Tom.winTimes);
			} else if(Tom.Throw() == challenger.Throw()) {
				Tom.drawTimes ++;
				System.out.println("第" + i + "轮\t平局\t平局\t\t" + Tom.winTimes);
				challenger.drawTimes ++;
			} else {
				Tom.defeatTimes ++;
				challenger.winTimes ++;
				System.out.println("第" + i + "轮\t输\t赢\t\t" + Tom.winTimes);
			}
		}
	}
}

class Person {
	long winTimes = 0; //初始化赢的次数
	long defeatTimes = 0; //初始化输的次数
	long drawTimes = 0; //初始化平局的次数
	public int Throw() {
		// return ((int)(Math.random() * 10)) / 3;
		// Random r = new Random();
		return new Random().nextInt(3);
	}
}
