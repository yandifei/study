//课堂练习
public class Execrise1 {
	public static void main(String[] agrs) {
		//1.需求：
		//假如还有59天放假，问:合xx个星期零xx天
		//2.思路分析：
		//(1)使用int型的days来放天数
		//(2)一个星期是7天，days/7 零多少天 day % 7
		//(3)输出
		//3.走代码
		int days = 59;
		int week = days / 7;
		int leftday = days % 7;
		System.out.println("还有"+week+"个星期"+leftday+"天");

	}
}