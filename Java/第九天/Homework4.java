/*Homework4.java -- 本章练习*/
import java.util.Scanner;
public class Homework4 {
	public static void main(String[] agrs) {
		// 判断一个整数是否是水仙花数，所谓水仙花数是指一个3位数，其各个位上数字立方和等于其本身
		// 例如:153=1*1*1+3*3*3+5*5*5
		/*先得到 n的百位，十位
		各位的数字，使用 if 判断他们的立方和是否相等
		n的百位 =n/100
		n的十位 =n%100
		Math.pow()立方
		*/
		Scanner myScanner = new Scanner(System.in);
		System.out.println("请输入需要判断的水仙花数");
		int num =  myScanner.nextInt();
		if((int)(Math.pow(num / 100,3)+Math.pow((num % 100)/10,3)+Math.pow(num % 10,3)) == num) {
			System.out.println("这是一个水仙花数");
		} else {
			System.out.println("这不是水仙花数");
		}
		
	}
}