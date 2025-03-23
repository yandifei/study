/*VarParameter.java -- 可变参数*/
public class VarParameter {
	public static void main(String[] args) {
		HspMethod m = new HspMethod();
		System.out.println(m.sum(1,5,100));
		int[] a = {1, 5, 100};
		System.out.println(m.sum(a));

	}
}

class HspMethod {
	//可以计算 2个数的和，3个数的和，4。5,
	//可以使用方法重载
	// public int sum(int n1, int n2) {//2个数的和
	// 	return n1 + n2;
	// }
	// public int sum(int n1,int n2,int n3) {//3个数的和
	// 	return n1 + n2 + n3;
	// }
	// public int sum(int n1,int n2, int n3,int n4) {//4个数的和
	// 	return n1 + n2 + n3 + n4;
	// }
	//上面的三个方法名称相同，功能相同，参数个数不同->使用可变参数优化
	//1.int...表示接受的是可变参数,类型是int即可以接收多个int(0-多)
	//2.使用可变参数时可，可以当做数组来使用 即nums可以当作数组来使用
	//遍历nums求和
	public int sum(int... nums) {
		System.out.println("接收的参数个数=" + nums.length);
		int res = 0;
		for(int i = 0; i < nums.length; i++) {
			res += nums[i];
		}
		return res;
	}
}