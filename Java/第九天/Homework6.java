/*Homework6.java -- 本章练习*/
import java.util.Scanner;
public class Homework6 {
	public static void main(String[] agrs) {
		Scanner myScanner = new Scanner(System.in);
		//输出小写的a-z以及大写的Z-A
		// System.out.println("请输入")
		//我这里的思路是ASCII码，第65为A，第97是a,差了32位
		for(int i = 0; i < 26; i++) {		//打印26个字母
			char j = 65, k = 97;
			j += i;
			k += i;
			// System.out.print(j + " ");		//特别注意如果System.out.print(j + k + " ");就会有问题
			System.out.print(" " + k + " " + j);
		}
		System.out.println();
		for(char i = 64, j = 96, k = 1; k <= 26; k++) {
			System.out.print(" " + (char)(i + k) + " " + " " + (char)(j + k));
		}
	}	
}
/*
for(char c1 ='a'; c1 <= 'z';c1++){
	System.out.print(c1 + " ");
}
*/