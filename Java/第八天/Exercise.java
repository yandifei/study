//打印空心菱形
import java.util.Scanner;	//导入类对象
public class Exercise {
	public static void main(String[] agrs) {
		/*打印菱形
		   *			//1层，3空格(层数-1)，1星(2层数-1)
		  ***			//2层，2空格(层数-2)，3星(2层数-1)
		 *****			//3层，1空格(层数-3)，5星(2层数-1)
		*******	 //4层(中间层)，0空格(层数-0)，7星(2层数-1)
		 *****			//5层，1空格(层数-3)，5星(2层数-1)
		  ***			//6层，2空格(层数-2)，3星(2层数-1)
		   *			//7层，3空格(层数-1)，1星(2层数-1)
		*/
		System.out.println("请输入菱形的上半层数");
		Scanner myScanner = new Scanner(System.in);
		int level = myScanner.nextInt();	//接收用户给的菱形上半层数
		// level = 4; //菱形的上层数(测试为4层)
		for(int i = 1; i <= level; i++) {
			for(int j = 1; j <= level - i; j++) {
				System.out.print(" ");
			}
			for(int k = 1; k <= 2 * i - 1; k++) {
				System.out.print("*");
			}
			System.out.println(); //换行
		}
		// ***** 	1
		//  ***		2
		//   *		3
		for(int i = 1; i <= level - 1; i++) {
			for(int j = 0; j <= i - 1; j++) {	//打印空格
				System.out.print(" ");
			}
			for(int k = (level - 1) * 2 - 1; k >= 2 * i - 1; k--) {
				System.out.print("*");
			}
			System.out.println(); //换行
		}

	}
}