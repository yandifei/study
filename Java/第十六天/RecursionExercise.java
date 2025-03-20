/*RecursionExercise.java -- 递归练习*/
public class RecursionExercise {
	public static void main(String[] args) {
		FibonacciSequence fibona = new FibonacciSequence();
		int n = 10;
		System.out.println("当n=7对应的斐波那契数" + fibona.Fibonacci(n));
		System.out.println("====================================");
		fibona.allFibonacci();
	}
}

class FibonacciSequence {
	/*
	请使用递归的方式求出斐波那契数1,1,2,3,5,8,13...给你一个整数n，求出它的值是多少
	1. 当n = 1 时斐波那契数是1
	2. 当n = 2 时斐波那契数是2
	3. 当n > 3 时斐波那契数是前2个数的和
	*/
	public int Fibonacci(int n) {
		if(n >= 1) {
			if(n == 1 || n == 2) {
				return 1;
			} else {
				return Fibonacci(n - 1) + Fibonacci(n - 2);
			}
		} else {
			System.out.println("要求输入n >= 1的数");
			return -1;
		}
	}


	//打印指定范围内的斐波那契数
	public void allFibonacci() {
		int a = 0, b = 1;
		while(b <= 100) {
			System.out.print(a + " ");
			a = a + b;
			b = a;
		}
	}
}
