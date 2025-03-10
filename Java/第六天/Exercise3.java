/*Exercise3 -- switch练习*/
import java.util.Scanner;
public class Exercise3 {
	public static void main(String[] agrs) {
		//指定月份，打印该月份所属的季节。3，4，5春季、6，7，8夏季、9，10，11秋季、12，1，2冬季
		//提示是使用穿透
		Scanner myScanner = new Scanner(System.in);
		System.out.println("请输入查询季节的月份");
		int month = myScanner.nextInt();
		switch(month) {
			case 3 :
			case 4 :
			case 5 :
				System.out.println("此月份为春季");
				break;
			case 6 :
			case 7 :
			case 8 :
				System.out.println("此月份为夏季");
				break;
			case 9 :
			case 10 :
			case 11 :
				System.out.println("此月份为秋季");
				break;
			case 12 :
			case 1 :
			case 2 :
				System.out.println("此月份为冬季");
				break;
			default :
				System.out.println("输入的月份错误(1-12)");
		}
		System.out.println("程序结束");
	}
}