/*Homework8.java -- 本章练习08*/
public class Homework8 {
	//给定一个Java程序的代码如下所示，则编译运行后，输出结果是()
	int count = 9;
	public void count1() {
		count = 10;
		System.out.println("count1=" + count);
	}
	public void count2() {
		System.out.println("count1=" + count++);
	}
	public static void main(String[] args) {
		new Homework8().count1();	//10
		Homework8 t1 = new Homework8();	//
		t1.count2();	//9
		t1.count2();	//10
	}
}