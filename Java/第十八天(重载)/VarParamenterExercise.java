/*VarParamenterExercise.java -- 可变参数练习*/
public class VarParamenterExercise {
	public static void main(String[] args) {
		// 有三个方法，分别实现返回姓名和两门课成绩（总分），返回姓名和三门课成绩（总
		// 分），返回姓名和五门课成绩（总分）。封装成一个可变参数的方法
		HspMethod hm = new HspMethod();
		System.out.println(hm.showScore("yandifei",90.1,80,100,50.5));
	}
}

class HspMethod {
	public String showScore(String name, double... score) {
		double totalScore = 0;
		for(int i = 0; i < score.length; i++) {
			totalScore += score[i];
		}
		return name + "有" + score.length + "门课的成绩总分为" + totalScore;
	}
}