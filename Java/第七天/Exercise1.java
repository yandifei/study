//打印乘法口诀
public class Exercise1 {
	public static void main(String[] agrs) {
		
		for(int a = 1; a <= 9; a++) {
			for(int b = 1;a >= b; b++) {
				System.out.printf("\t" + b + " * " + a + " =" + a * b);	//print是不会换行的
			}
			System.out.println();//用来换行的
		}
	}
}