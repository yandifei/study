/*Recursion.java -- 递归调用*/
public class Recursion {
	public static void main(String[] args) {
		//打印阶乘
		T t = new T();
		int result = t.factorial(5);
		System.out.println("递归的值是" + result);
	}
}

class T {
	public int factorial(int num) {
		if(num == 1) {
			return 1;
		} else {
			return factorial(num - 1) * num;
		}
	}
}