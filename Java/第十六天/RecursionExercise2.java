/*RecursionExercise2.java -- 递归练习*/
public class RecursionExercise2 {
	public static void main(String[] args) {
		// 猴子吃桃子问题：有一堆桃子，猴子第一天吃了其中的一半，并再多吃了一个！以后
		// 每天猴子都吃其中的一半，然后再多吃一个。当到第10天时，想再吃时（即还没吃）
		// 发现只有1个桃子了。问题：最初共多少个桃子？
		A a = new A();
		int b = a.monkey(1);
		System.out.println(b);


	}
}

class A {
	//1。day=10时 有 1个桃子
	// 2. day= 9 时 有(day10+ 1)*2

	public int monkey(int day) {
		if(day == 10) {
			return 1;
		} else if(day >= 1 &&  day <= 9){
			return (monkey(day + 1) + 1) * 2 ;
		} else {
			System.out.println("输入的范围是1-10");
			return -1;
		}
	}
}