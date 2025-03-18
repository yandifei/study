/*AccessModifiers.java -- 访问修饰符*/
public class AccessModifiers {
	public static void main(String[] args) {
		//创建Persion对象（Hunam更加强调生物、物种上的人，person指的是社会的人）
		//p1是对象名(对象引用)
		//new Person() 创建的对象空间(数据)才是真正的对象
		Person p1 = new Person();
		//对象的属性默认值，遵守数组规则：
		//int 0, short 0, byte 0, long 0, float 0.0, double 0.0, char \u0000, boolean false
		System.out.println("\n当前这个人的信息");
		System.out.println("age=" + p1.age + " name=" + p1.name + " sal=" + p1.sal + " isPass=" + p1.isPass);
	}
}

class Person {
	//四个属性
	int age;
	String name;
	double sal;
	boolean isPass;
}