//if嵌套语句学习
import java.util.Scanner;
public class IfStudy {
	public static void main(String[] agrs) {
		//编写一个程序,可以输入人的年龄,如果该同志的年龄大于18岁,
		//则输出:你年龄大于18,要对自己的行为负责,送入监狱
		Scanner myScanner = new Scanner(System.in);
		System.out.println("请输入年龄");
		int age = myScanner.nextInt();
		if(age > 18) {
			System.out.println("你的年龄大于18岁，要对自己的行为负责，送入监狱");
		}
		System.out.println("程序继续");
	}
}