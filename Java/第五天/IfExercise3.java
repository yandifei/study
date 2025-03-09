// 参加歌手比赛，如果初赛成绩大于8.0进入决赛否则提示淘汰。并且根据性别提示
// 进入男子组或女子组。【可以让学员先练习下】，输入成绩和性别，进行判断和输出信息。
import java.util.Scanner;
public class IfExercise3 {
	public static void main(String[] agrs) {
		System.out.println("请输入你的成绩");
		Scanner myScanner = new Scanner(System.in);	//创建接收器对象
		double score = myScanner.nextDouble();	//接收成绩
		if(score > 8.0) {
			System.out.println("请输入你的性别");	
			char gender = myScanner.next().charAt(0);	//把输入的字符串转为一个字符
			if('男' == gender) {
				System.out.println("进入男子组");
			} else if('女' == gender) {
				System.out.println("进入女子组");
			} else {
				System.out.println("性别有误");
			}
		} else {
			System.out.println("你已经被淘汰");
		}
	}
}