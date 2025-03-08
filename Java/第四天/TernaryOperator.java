//三元运算符（三目运算符，中文里面的目代表的是操作数）
public class TernaryOperator {
	public static void main(String[] agrs) {
		/**运算规则
		 * 语法：条件表达式?表达式1：表达式2;
		 * 1. 如果条件表达式为true则运算后的结果是表达式1
		 * 2. 如果条件表达式为false则运算后的结果是表达式2
		*/
		int a = 10;
		int b = 99;
		int result = a > b ? a++ : b--;
		System.out.println("result:"+result+"b:"+b);
		/**使用细节2
		 *表达式1和表达式2要为可以赋给接收变量的类型(或可以自动转换
		*/
		int a1 = 3;
		int b1 = 8;
		// int c1 = a1 > b1 ? 0.1 : 4.1; //会报错
		// int c2 = a1 > b1 ? (int)0.1 : (int)4.1; //强制转换后就没问题
		double c3 = a1 > b1 ? a1 : b1; //这个也是没有问题的，满足int -> double
		int c4 = a1 > b1 ? a1 : b1;
		//三元运算符可以转换成if-else语句
		if(a1 > b1) result=a1++;
		else result = --b1;
		//个人总结就是java没有提供布尔值和其他类型的自动转换那就意味着三元常用了
		//如对返回值做处理：
		boolean d = a > b ? true : false; //表达式不能为空
		System.out.println(d);


	}
}