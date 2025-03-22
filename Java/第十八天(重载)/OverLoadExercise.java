/*OverLoadExercise.java -- 重载练习*/
public class OverLoadExercise {
	public static void main(String[] args) {
		// 编写程序，类Methods中定义三个重载方法并调用。方法名为m。三个方法分
		// 别接收一个int参数、两个int参数、一个字符串参数。分别执行平方运算并输出
		// 结果，相乘并输出结果，输出字符串信息。在主类的main(方法中分别用参数
		// 区别调用三个方法。
		Methods calculator = new Methods();
		calculator.m(12);
		calculator.m(2,5);
		calculator.m("hello world");
		//测试
		System.out.println(calculator.max(11,1));
		System.out.println(calculator.max(0.11,0.22));
		System.out.println(calculator.max(0.99,0.77,1));
	}
}

class Methods {
	public void m(int a) {
		System.out.println(a * a);
	}
	public void m(int a, int b) {
		System.out.println(a * b);
	}
	public void m(String a) {
		System.out.println(a);
	}


	// 在Methods类，定义三个重载方法max()，第一个方法，返回两个int值中的最
	// 大值，第二个方法，返回两个double值中的最大值，第三个方法，返回三个
	// double值中的最大值，并分别调用三个方法。
	public int max(int n1, int n2) {
		return n1 > n2 ? n1 : n2;
	}
	public double max(double n1, double n2) {
		return n1 > n2 ? n1 : n2;
	}
	public double max(double n1, double n2, double n3) {
		return (n1 > n2 ? n1 : n2) > n3 ? (n1 > n2 ? n1 : n2) : n3;
	}

}