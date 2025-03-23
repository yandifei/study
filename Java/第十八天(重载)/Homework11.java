/*Homework11.java -- 章节练习*/
public class Homework11 {
	public static void main(String[] args) {
	// 在测试方法中，调用method方法，代码如下，编译正确，试写出method方法的
	// 定义形式，调用语句为:System.out.println(method(method(10.0,20.0),100);	
	//函数定义
	Homework11 a = new Homework11();
	}
	public double method(double num1, double num2) {
		return num1 + num2;
	}
	{
		System.out.println(method(method(10.0,20.0),100));
	}
}
