/*Homework1.java -- 本章练习*/
public class Homework1 {
	public static void main(String[] agrs) {
		/*某人有100,000元,每经过一次路口，
		需要交费,规则如下:
		1)当现金>50000时,每次交5%
		2)当现金<=50000时,每次交1000
		编程计算该人可以经过多少次路口,要求: 使用 while break方式完成*/
		double money = 100000; //初始化当前的费用
		int count1 = 0; //用来统计当现金>50000时,每次交5%的次数
		int count2 = 0; //用来统计当现金<=50000时,每次交1000
		while(true) {
			if(money > 50000) {
				money *= 0.95;	//交5%的税就是 1-(1*0.05)=0.95
				count1++;
			} else if(money <= 50000 && money >= 1000) {	//特别注意money要>=1000,0都不行
				money -= 1000; //每次-1000
				count2++;
			} else {
				break;
			}	
		}
		System.out.println("总共交了"+(count1+count2)+"次税");
		System.out.println("5%交了"+count1+"次税，"+"1000交了"+count2+"次税");
	}
}