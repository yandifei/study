/*Homework8.java -- 本章作业*/
public class Homework8 {
	public static void main(String[] agrs) {
		//求出1-1/2+1/3-1/4....1/100的和
		//这个题目误导我了，1/2是1分之2
		
		double count = 0; for(int i=1,k=1;i <= 100; i++, k = 1) {if(i%2==0) {k=-1;} count += 1f/(i*k);}
	}
}
