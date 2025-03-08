public class AssignOperator {
	public static void main(String[] agrs) {
		//赋值运算符的使用
		int a = 10;
		a += 4; //等价于 a = a + 10;
		//特别注意的是
		//复合赋值运算符会进行类型转换
		byte b = 3;
		b += 2;	//等价于 b = (byte)(b + 2);
		b++;	//理论上是b = b + 1;实际上是 b = (type)(b + 1)
		byte c = 1;
		//过程应该是先计算，byte类型的c加1这个计算自动把c的类型转为了int型
		c = (byte)(c + 1);	//最后把计算的结果int型又转回byte型

		System.out.println(c);
	}
}