/*ThisDetail.java -- this指针细节*/
public class ThisDetail {
	public static void main(String[] args) {
		// T t = new T();
		// t.f2();
		 T t2 = new T();

	}
}

class T {
	// 细节：访问构造器语法：this（参数列表）；
	// 注意只能在构造器中使用（即只能在构造器中访问另外一个构造器）
	// 注意：访问构造器语法：this（参数列表）；必须放置第一条语句
	public T() {
		this("jack",100);
		System.out.println("T()构造器");
		//这里去访问 T(String name，int age)
	}
	public T(String name, int age) {
		System.out.println("T(String name, int age)构造器");
	}

	//细节：访问成员方法的语法：this·方法名（参数列表）;
	public void f1() {
		// this("jack",100); //这种写法只能用在构造器里面不能用在方法里面
		System.out.println("f1()方法.. ");
	}
	public void f2() {
		System.out.println("f2()方法.. ");
		//调用本类的f1
		//第一种方式
		f1();
		//第二种方式
		this.f1();
		/*具体的区别要到继承的时候才能说*/
	}
}