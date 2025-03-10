/*ForStudy1.java -- for语句学习*/
public class ForStudy1 {
	public static void main(String[] agrs) {
		//打印10句"hello world"
		//传统方法
		// System.out.println("hello world");
		// System.out.println("hello world");
		// System.out.println("hello world");
		// System.out.println("hello world");
		// System.out.println("hello world");
		// System.out.println("hello world");
		// System.out.println("hello world");
		// System.out.println("hello world");
		// System.out.println("hello world");
		// System.out.println("hello world");

		//循环条件必须是布尔值，不能是其他的（即i <= 10不能是i++）
		//int i = 1; 写在for的表达式里面就是代表这个i.
		for(int i = 1; i <= 10; i++) {
			 System.out.println("hello world "+i);
		}
		// System.out.println(i);	//这个是直接报错的，因为前面的int i仅仅是for循环体里面的而已
		//for(;循环判断条件;)
		//中的初始化和变量迭代可以写到其它地方，但是两边的分号不能省略
		int i2 = 1;	//循环变量初始化
		//条件为假的时候才退出循环
		for( ; i2 <= 10 ;) {
			System.out.println("hello world " + i2);
			i2++;
		}
		System.out.println(i2);	//这里是11

		//无限循环
		// for(;;) {	//表示的是一个无限循环(死循环)

		// }

		//循环初始值可以有多条初始化语句，但要求类型一样，并且中间用逗号隔开,
		//循环变量迭代也可以有多条变量迭代语句，中间用逗号隔开
		int count = 3;
		for(int i3 = 0, j = 0; i < count; i++, j += 2) {
			System.out.println("i=" + i + "j=" + j);
		}
		
	}
}