//关系运算符的使用

public class RelationalOperator {
	public static void main(String[] agrs) {
		// System.out.println("hello world");
		int a = 10;
		int b = 8;
		System.out.println(a > b);//T
		System.out.println(a >= b);//T
		System.out.println(a < b);//F
		System.out.println(a <= b);//F
		System.out.println(a == b);//F
		System.out.println(a != b);//T
		boolean flag = a > b;
		System.out.println("flag:"+flag);
	}
}