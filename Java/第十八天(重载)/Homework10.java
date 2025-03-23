/*Homework10.java -- 本章练习*/
//试写出以下代码的运行结果0
class Demo {
	int i = 100;
	public void m () {
		int j = i++;
		System.out.println("i=" + i);
		System.out.println("j=" + j);
	}
}
class Homework10 {
	public static void main(String[] args){
		Demo d1 = new Demo(); //i=100
		Demo d2 = d1;
		d2.m(); //j=100 , i=101,输出101，100
		System.out.println(d1.i);	//101
		System.out.println(d2.i);	//101
	}		
}
