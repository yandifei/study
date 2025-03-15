/*Homework9.java -- 本章作业*/
public class Homework9 {
	public static void main(String[] agrs) {
	//求1+ (1+2) + (1+2+3) + (1+2+3+4)+...+(1+2+3+...+100)的结果
		int count = 0;
		for(int i = 1, j = 0; i <= 100; i++) {
			j += i;
			count += j;
		}
		System.out.println(count);
	}
}
