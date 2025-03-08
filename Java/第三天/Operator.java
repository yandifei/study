public class Operator {
	public static void main(String[] agrs) {
		//和python不一样，这里整数相除不会自动转换为浮点数
		System.out.println(1/3);
		int a = 1/3;
		System.out.println(a);
		//取模的符号是根据第一个数（被取模数）决定的，如果第一个数是负数者取模的数值为负数
		//被取模数为负数或正数都和结果的符号无关
		System.out.println(10 % 3);		//1
		System.out.println(-10 % 3);	//-1
		System.out.println(10 % -3);	//1
		System.out.println(-10 % -3);	//-1
		//自增和自减
		int i = 10;
		i++;	//自增 等价于 i = i + 1; => i = 11
		++i;	//自增 等价于 i = i + 1; => i = 12
		System.out.println(i);
		int j = 8;
		// int k = ++j;	//等价j = j + 1; k = j;
		int k = j++;	//等价k = j; j = j + 1;
		System.out.println("k="+k+"j="+j);
		
	}
}