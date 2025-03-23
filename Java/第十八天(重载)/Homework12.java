/*Homework12.java -- 章节练习12*/
public class Homework12 {
	public static void main(String[] args) {
	// 创建一个Employee类，属性有（名字，性别，年龄，职位，薪水)，提供3个构造方法，可以初始化
	//（1）（名字，性别，年龄，职位，薪水)，（2)（名字，性别，年龄）（3）(职位，薪水)，要求充分复用构造器
	Employee me = new Employee("yandifei",'男',50);
	}
}

class Employee { //这个没搞好
	String name;
	char sex;
	int age;
	String posts;
	double salary;

	//名字，性别，年龄，职位，薪水
	public Employee(String name, char sex, int age, String posts, double salary) {
		this(name,sex,age);
		//this(posts,salary); //不能用，重复了
		// this.name = name;
		// this.sex = sex;
		// this.age = age;
		this.posts = posts;
		this.salary = salary;
		
	}
	//名字，性别，年龄
	public Employee(String name, char sex, int age) {
		this.name = name;
		this.sex = sex;
		this.age = age;
	}
	//职位，薪水
	public Employee(String posts, double salary) {
		this.posts = posts;
		this.salary = salary;
	}
	
	

}