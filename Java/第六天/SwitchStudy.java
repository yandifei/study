//switch分支学习	
import java.util.Scanner;
public class SwitchStudy {
	public static void main(String[] agrs) {
		/*
		请编写一个程序，该程序可以接收一个字符，比如:a,b,c,d,e,f,g
		a表示星期一，b表示星期二
		根据用户的输入显示相应的信息.要求使用 switch 语句完成I
		*/
		Scanner myScanner = new Scanner(System.in);	//创建一个扫描器对象
		System.out.println("请输入a,b,c,d,e,f,g其中的一个字符");
		char word = myScanner.next().charAt(0);	//获取输入的第一个字符
		switch(word) {
			case 'a' :
				System.out.println("星期一");
				break;
			case 'b' :
				System.out.println("星期二");
				break;
			case 'c' :
				System.out.println("星期三");
				break;
			case 'd' :
				System.out.println("星期四");
				break;
			case 'e' :
				System.out.println("星期五");
				break;
			case 'f' :
				System.out.println("星期六");
				break;
			case 'g' :
				System.out.println("星期天");
				break;
			default:
				System.out.println("输入错误");
		}
		System.out.println("程序结束了");
	}
}