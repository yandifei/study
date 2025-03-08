/**逻辑运算符 
 * 演示逻辑运算符的使用
 */
public class LogicOperator {
	public static void main(String[] agrs) {
		//&& 和 & 的演示(两个条件都为true，结果为true,其他皆为flase)
		//&&
		int age = 50;
		if(age > 20 && age < 90) {
			System.out.println("ok");
		}
		//&
		if(age > 20 & age < 90) {
			System.out.println("ok");
		}
		//区别
		int a = 4;
		int b = 9;
		//对于&&(短路与)，如果第一个条件为false，则后面的条件不再判断(执行)
		if(a < 1 && ++b < 50) {
			System.out.println("ok");
		}
		System.out.println("a:"+ a + "b:" + b);	//判断是否改变
		//对于&(逻辑与)，如果第一个条件为false，后面的条件仍然会判断(执行)
		if(a < 1 & ++b < 50) {
			System.out.println("ok");
		}
		System.out.println("a:"+ a + "b:" + b);	//判断是否改变


		//|| 和 | 的演示(只要有一个为true，结果为true,其他皆为flase)
		//||(逻辑或)
		int age2 = 50;
		if(age2 > 20 || age2 < 30) {
			System.out.println("ok");
		}

		//|(短路或)
		if(age2 > 20 | age2 < 30) {
					System.out.println("ok");
				}
		// | (逻辑或)和 || (短路或)的区别
		int a2 = 4;
		int b2 = 9;
		//|| (短路或)和上面一样，如果第一个条件为true则第二个条件不会判断
		if(a2 < 1 || ++b2 < 50) {
			System.out.println("ok");
		}
		System.out.println("a:"+ a2 + "b:" + b2);	//判断是否改变
		//对于|(逻辑或)，如果第一个条件为True，后面的条件仍然会判断(执行)
		if(a2 < 1 | ++b2 < 50) {
			System.out.println("ok");
		}
		System.out.println("a:"+ a2 + "b:" + b2);	//判断是否改变

		/**无论是逻辑与还是短路与，逻辑或还是短路或
		 * 短路的比逻辑的快
		 */
	}
}