//if练习
import java.util.Scanner;
public class IfExersice1 {
	public static void main(String[] agrs) {
		Scanner myScanner = new Scanner(System.in);
		//假定信用为int
		System.out.println("请输入信用分(1-100)");
		//==>如果输入的不是整数，而是其他类型如：hello那该怎么办？
		//后面用异常处理机制搞定
		int grade = myScanner.nextInt();	//接受信用分
		//对输入的数据做一个有效判断（防止bug产生）
		if(grade >= 1 && grade <= 100) {
			//下面的判断有bug，就是如果输入的信用分超过100就判定不及格
			if(grade == 100) {
				System.out.println("信用极好");
			} else if(grade > 80 && grade <= 99) {
				System.out.println("信用优秀");
			} else if(grade >= 60 && grade <= 80) {
				System.out.println("信用一般");
			} else {
				System.out.println("信用不及格");
			}	
		} else {
			System.out.println("信用分需要在1-100，请重新输入:)");
		}
	}
}