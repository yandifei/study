/*Exercise.java -- 克隆对象*/
public class Exercise {
	public static void main(String[] args) {
		//编写一个方法copyPerson,可以复制一个Person对象，返回复制的对象，克隆对象
		//注意要求得到的新对象和原来的对象是独立的对象，只是他们的属性相同
		Person p = new Person();
		p.name = "yandifei";
		p.age = 21;
		MyTools tools = new MyTools();
		Person p2 = tools.copyPerson(p);

		//到此p 和 p2是Person两个独立的对象
		System.out.println("P:" + p.age + " " + p.name);
		System.out.println("P2:" + p2.age + " " + p2.name);

		//通过输出对象的hashCode看看对象是否一致
		System.out.println(p);
		
	}
}

class Person {
	String name;
	int age;
}

class MyTools {
	public Person copyPerson(Person p) {
		//创建一个新的对象
		Person p2 = new Person();
		p2.name = p.name;	//把原来对象的名字赋给p2.name
		p2.age = p.age;	//把原来对象的年龄赋给p2.age
		return p2;


	}
}