//if语句循环学习（单分支、双分支、多分支）
public class IfStudy2 {
	public static void main(String[] agrs) {
		//一个if只能有一个入口或没有入口
		int num1 = 100, num2 = 200;
		if(num1 > 99) {
			System.out.println("有钱");
		} else if(num1 < 200) {
			System.out.println("穷");
		} else {	//else去掉就可能是没有入口了
			System.out.println("你是什么鬼？");
		}
	}
}