/*Array.java -- 数组学习*/
public class Array {
	public static void main(String[] agrs) {
		/*
		它们的体重分别是3kg,5kg，1kg,3.4kg,2kg,50kg。
		请问这六只鸡的总体重是多少?平均体重是多少?
		思路分析
		1. 定义六个变量double，求和得到总体重
		2. 平均体重=总体重/6
		3. 分析传统实现的方式问题 6->600->5666
		4. 引出新的技术 -> 使用数组来
		*/

		//传统方法
		double hen1 = 3;
		double hen2 = 5;
		double hen3 = 1;
		double hen4 = 3.4;
		double hen5 = 2;
		double hen6 = 50;
		double totalWeight = hen1 + hen2 + hen3 + hen4 + hen5 + hen6;
		double avgWeight = totalWeight / 6;
		System.out.println("总体重：" + totalWeight + " 平均体重：" + avgWeight);

		System.out.println();//换行

		//新的方法
		//定义一个数组
		//1. double[] 表示是double类型的数组，数组名是hens
		//2. {3, 5, 1, 3.4, 2, 50}; 表示的是数组的值/元素，依次表示数组的第几个元素
		double[] hens = {3, 5, 1, 3.4, 2, 50};
		//可以使用 数组名.length 得到数组的大小/长度
		System.out.println("数组的大小是：" + hens.length);

		//遍历数组得到数组的所有元素的和，使用for
		double totalWeight1 = 0;
		for(int i = 0; i < hens.length; i++) {
			System.out.println("第x个元素的值=" + hens[i]);
			totalWeight1 += hens[i];
		}
		System.out.println("总体重：" + totalWeight1 + " 平均体重：" + totalWeight1 / 6);


	}
}