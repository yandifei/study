//练习2	
public class Exercise2 {
	public static void main(String[] agrs) {
	//需求：
	//定义一个变量保存华氏温度，华氏温度转换摄氏温度的公式为:5/9*(华氏温度-100)
	//请求出华氏温度对应的摄氏温度。[234.5]
	//思路分析：
	//(1)先定义一个double变量HuaShi保存华氏温度
	//(2)根据给出的公式进行计算5/9*(华氏温度-100)
	//(3)将变量的结果报存到double变量HuaShi
	double HuaShi = 234.5;
	double SheShi = 5. / 9 * (HuaShi - 100);
	System.out.println("华氏温度："+HuaShi+"转摄氏温度："+SheShi);
	}
}