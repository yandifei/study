/*ConstructorDetail.java -- 构造器细节*/
public class ConstructorDetail {
	public static void main(String[] args) {
		//构造器本身就是一个方法，当然可以重载（不能添加任何返回类型和方法名字必须和类名相同而已）
		Person p1 = new Person("yandifei", 32); //第一个构造器
		Person p2 = new Person("jack"); //第二个构造器
		//构造器不能被调用
		// p1.Person(); //这个是错误的
	}
}

class Person {
	String name; 
	int age; //默认0 
	//第一个构造器
	public Person(String pName, int pAge) {
		name = pName;
		age = pAge;
	}
	//第二个构造器，只指定人名，不指定年龄
	public Person(String pName) {
		name = pName;
	}
}


class Dog {
	//如果程序员没有定义构造器，系统会自动给类生成一个默认无参构造器（也叫默认构造器）
	/*
		默认构造器
		Dog() {
	
		}
	*/
	//使用javap指令反编译看看
	//javac是把代码文件(.java)编译成字节码文件(.class), javap是吧字节码文件(.class)返编译为代码文件(.java)
	//javap -c Dog.class //反汇编
	// 一旦定义了自己的构造器，默认的构造器就覆盖了，就不能再使用默认的无
	// 参构造器，除非显式的定义一下，即：Dog00写
}