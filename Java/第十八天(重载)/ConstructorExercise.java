/*ConstructorExercise.java -- 构造器练习*/
public class ConstructorExercise {
	public static void main(String[] args) {
		// 第一个无参构造器：利用构造器设置所有人的age属性初始值都为18
		// 第二个带pName和pAge两个参数的构造器：使得每次创建Person对象的同
		// 时初始化对象的age属性值和name属性值。分别使用不同的构造器，创建对
		// 象.
		Person p1 = new Person();//无参构造器
		System.out.println("p1的信息 name=" + p1.name + "age=" + p1.age);
		Person p2 = new Person("scott", 50);
		//下面输出 name = scott，age = 50
		System.out.println("p2的信息 name=" + p2.name + " age=" + p2.age);
	}
}



class Person {
	String name;	//默认值 null
	int age;	//默认0
	public Person() {
		age = 18;
	}
	public Person(String pName, int pAge) {
		name = pName;
		age = pAge;
	}
}