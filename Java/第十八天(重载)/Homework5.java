/*Homework5.java -- 本章练习05*/
public class Homework5 {
	public static void main(String[] args) {
		// 定义一个圆类Circle，定义属性：半径，提供显示圆周长功能的方法，提供显示圆面积的方法
		Circle c = new Circle();
		System.out.println(c.circumference(3));
		System.out.println(c.area(3));
	}
}

class Circle {
	//求圆的周长
	public double circumference(double radius) {
		return 2 * 3.1415926535 * radius;
	}

	public double area(double radius) {
		return 3.1415926535 * radius * radius;
	}
}
