/*Homework2.java -- 本章练习*/
import java.util.Scanner;
public class Homework2 {
	public static void main(String[] agrs) {
		//实现判断一个整数，属于哪个范围:大于0;小于0;等于0Homework02.java
		Scanner myScanner = new Scanner(System.in);
		System.out.println("请输入一个整数");
		int num = myScanner.nextInt();
		if(num > 0) {
			System.out.println("输入的数大于0");
		} else if(0 == num) {
			System.out.println("输入的数为0");
		} else if(num < 0) {
			System.out.println("输入的数小于0");
		}
	}
}