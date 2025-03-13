/*Homework3.java -- 本章练习*/
import java.util.Scanner;
public class Homework3 {
	public static void main(String[] agrs) {
		//判断一个年份是否为闰年
		//闰年的核心规则是：4年一闰，百年不闰，400年再闰。
		Scanner myScanner = new Scanner(System.in);
		System.out.println("请输入需要判断的年份");
		int year = myScanner.nextInt();
		if(year % 4 == 0) {
			if(year % 100 == 0) {
				if(year % 400 == 0) {
					System.out.println("是闰年");
				} else {
					System.out.println("不是闰年");
				}
			} else {
				System.out.println("是闰年");
			}
		} else {
			System.out.println("不是闰年");
		}
	}
}