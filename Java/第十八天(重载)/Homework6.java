/*Homework6.java -- 本章练习06*/
public class Homework6 {
	public static void main(String[] args) {
	// 编程创建一个Cale计算类，在其中定义2个变量表示两个操作数
	// 定义四个方法实现求和、差、乘、商（要求除数为0的话，要提示）并创建两个对象，分别测试
	Cale cale1 = new Cale();
	System.out.println(cale1.sum(4,2));
	System.out.println(cale1.difference(4,2));
	Cale cale2 = new Cale();
	System.out.println(cale2.product(4,2));
	System.out.println(cale2.quotient(4,2));
	}
}

class Cale {
	//和
	public double sum(double operand1, double operand2) {
		return operand1 + operand2;
	}
	//差
	public double difference(double operand1, double operand2) {
		return operand1 - operand2;
	}
	//乘（积）
	public double product(double operand1, double operand2) {
		return operand1 * operand2;
	}
	//商
	public double quotient(double operand1, double operand2) {
		if(0 == operand2) {	//除数为0返回-1
			return -1;
		}
		return operand1 / operand2;
	}
}
