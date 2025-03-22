/*OverLoad.java -- 运算符重载*/
//案例:类：MyCalculator方法：calculate
// calculate(int n1,int n2)//两个整数的和
// calculate(intn1,doublen2)//一个整数，一个double的和
// calculate(doublen2,int n1)//一个double,一个Int和
// calculate(int n1,int n2,int n3)//三个int的和
public class OverLoad {
	public static void main(String[] args) {
		MyCalculator mc = new MyCalculator();
		System.out.println(mc.calculate(1, 2));
		System.out.println(mc.calculate(1.1, 2));
	}
}


class MyCalculator {
	public int calculate(int n1, int n2) {
		return n1 + n2;
	}
	public double calculate(int n1, double n2) {
		return n1 + n2;
	}
	public double calculate(double n1, int n2) {
		return n1 + n2;
	}
	public int calculate(int n1, int n2, int n3) {
		return n1 + n2 + n3;
	}
}