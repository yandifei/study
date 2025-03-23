/*Constructor.java -- 构造器*/
// 我们来看一个需求：前面我们在创建人类的对象时，是先把一个对象创建好后，再给
// 他的年龄和姓名属性赋值，如果现在我要求，在创建人类的对象时，就直接指定这个
// 对象的年龄和姓名，该怎么做？这时就可以使用构造器。
// 构造方法=构造器=构造函数=constructor
// 完成对对象的初始化
public class Constructor {
	public static void main(String[] args) {
		//当我们new一个对象时，直接通过构造器指定名字和年龄
		Person me = new Person("yandifei",25);
		System.out.println("me对象的信息如下");
		System.out.println("me对象的名字" + me.name);
		System.out.println("me对象的年龄" + me.age);

	}
}

class Person {
	String name;
	int age;
	//构造器
	//构造器没有返回值,也不能写void
	//构造器的名称和类Person一样
	//(String pName, int pAge)是构造器形参列表，规则和成员方法一样
	public Person(String pName, int pAge) {
		System.out.println("构造器被调用");
		name = pName;
		age = pAge;
	}
	//在创建人类的对象时，就直接指定这个对象的年龄和姓名
}