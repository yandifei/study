/*Homework7.java -- 本章练习07*/
public class Homework7 {
	public static void main(String[] args) {
	// 设计一个Dog类，有名字、颜色和年龄属性，定义输出方法show)显示其信息。
	// 并创建对象，进行测试、【提示this.属性】		
	Dog dog1 = new Dog("小白","白色",10);
	System.out.println(dog1.show());

	}
}

class Dog {
	String name;
	String color;
	int age;
	public Dog(String name, String color, int age) {
		this.name = name;
		this.color = color;
		this.age = age;
	}
	public String show() {
		return "名字:" + this.name + " 颜色:" + this.color + " 年龄:" + this.age;
	}
}