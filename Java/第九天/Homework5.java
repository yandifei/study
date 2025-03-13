/*Homework5.java -- 本章练习*/
import java.util.Scanner;
public class Homework5 {
	public static void main(String[] agrs) {
		//输出1-100之间的不能被5整除的数，每5个一行
		int count = 0; //统计5个换行
		System.out.println("1-100之间的不能被5整除的数：");
		for(int num = 1; num <= 100; num++) {
			if(num % 5 != 0) {
				System.out.print(num+"\t");
				count++;
				if(5 == count) {	//不用清零就是count % 5 == 0
					System.out.println();//换行
					count = 0; //重新计数
				}
			}
		}
	}
}

