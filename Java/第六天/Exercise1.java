//switch 练习
import java.util.Scanner;
public class Exercise1 {
	public static void main(String[] agrs) {
		//char类型转为大写（键盘输入。只转换a->A,b->B,c->C,d,e,f
		//其它均输出"other"
		System.out.println("请输入a-f之间的一个字符");
		Scanner myScanner = new Scanner(System.in);		//创建一个扫描器对象
		char word = myScanner.next().charAt(0);
		switch(word) {
			case 'a' :
				System.out.println('A');
				break;
			case 'b' :
				System.out.println('B');
				break;
			case 'c' :
				System.out.println('C');
				break;
			case 'd' :
				System.out.println('D');
				break;
			case 'e' :
				System.out.println('E');
				break;
			case 'f' :
				System.out.println('F');
				break;
			default :
				System.out.println("输入错误");
		}
		System.out.println("程序结束");
	}
}