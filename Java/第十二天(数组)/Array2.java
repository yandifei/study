/*Array2.java -- 数组学习*/
import java.util.Scanner;
public class Array2 {
	public static void main(String[] agrs) {
		//演示数据类型数组名[]=new数据类型[大小]
		//循环输入5个成绩，保存到double数组，并输出
		Scanner myScanner = new Scanner(System.in);
		// double[] scores = new double[5];

		double[] scores;
		scores = new double[5];

		for(int i = 0; i < scores.length; i++) {
			System.out.println("请输入第"+ (i + 1) + "个元素的值");
			scores[i] = myScanner.nextDouble();
		}
		for(int i = 0; i < scores.length; i++) {
			System.out.println("第" + (i + 1) + "个元素的值为" + scores[i]);
		}
	}
}