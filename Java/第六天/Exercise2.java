/*Exercise2 -- switch练习2*/
import java.util.Scanner; //导入包的扫描器对象
public class Exercise2 {
	public static void main(String[] agrs) {
		//对学生成绩进行判断：大于60输出“及格”，低于60输出“不及格”
		//输出成绩不能大于100
		System.out.println("请输入你的成绩");
		Scanner myScanner = new Scanner(System.in);
		double score = myScanner.nextDouble();
		if(score >= 0 && score <= 100) {
			switch((int)score / 60) {
			case 1 :
				System.out.println("你的成绩及格");
				break;
			case 0 :
				System.out.println("你的成绩不及格");
				break;
			// default :	//已经嵌套了if就这里可以不要了
			// 	System.out.println("输入错误");
			}
		} else {
				System.out.println("输入错误");
		}
		
		System.out.println("程序结束");
	}
}