//键盘输入学习
//如果要使用这个键盘输入功能就必须创建一个实例（即为使用类对象），如果要是类对象就必须导包
import java.util.Scanner;	//表示把包java.util下的Scanner的类导入
public class Input {
	public static void main(String[] agrs) {
		//1. Scanner表示的是简单的文本扫描器，在java.util这个包里面
		//2. 创建Scanner对象，new创建一个
		Scanner myScanner = new Scanner(System.in);
		//3. 接收用户输入，使用的是相关的方法
		System.out.println("请输入名字");
		String name = myScanner.next();	//接收输入
		System.out.println("请输入年龄");
		int age = myScanner.nextInt();	//接收输入
		System.out.println("请输入薪水");
		double salary = myScanner.nextDouble();	//接收输入
		System.out.println("名字"+name+"年龄"+age+"薪水"+salary);
	}
}