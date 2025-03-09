// 出票系统:根据淡旺季的月份和年龄，打印票价[课后练习
// 4 10 旺季:
	// 成人(18-60):60
	// 儿童(<18):半价
	// 老人(>60):1/3
// 淡季:
	// 成人:40
	// 其他:20
import java.util.Scanner;
public class Homework {
	public static void main(String[] agrs) {
		System.out.println("请输入当前月份");		//判断旺季还是淡季
		Scanner myScanner = new Scanner(System.in);	//创建扫描器的对象
		int month = myScanner.nextInt();	//接收月份
		int age = -1;
		if(month > 4 && month <10) {
			System.out.println("请输入你的年龄");
			age = myScanner.nextInt();	//接收年龄
			if(age >= 0 && age < 18) {
				System.out.println("旺季，儿童半价30");
			} else if(age >= 18 && age <= 60) {
				System.out.println("旺季，成人60");
			} else if(age > 60) {
				System.out.println("旺季，老人1/3，20元");
			} else {
				System.out.println("输入错误");
			}
		} else if(month >= 1 && month <= 4 || month >= 10 && month <= 12) {
			System.out.println("请输入你的年龄");
			age = myScanner.nextInt();	//接收年龄
			if(age >= 0 && age <= 40) {
				System.out.println("淡季，成人40");
			} else if(age > 40) {
				System.out.println("需要20元");
			} else {
				System.out.println("输入错误");
			}
		} else {
			System.out.println("输入错误");
		}
	}
}