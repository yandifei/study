/*Homework1.java -- 本章作业*/
public class Homework1 {
	public static void main(String[] args) {
	//编写类A01，定义方法max，实现求某个double数组的最大值，并返回
	A01 a = new A01();
	double[] arr = { 1.2,1.3,1.5,0,1,9 };
	// System.out.println(a.max(1.2,1.3,1.5,0,1,9));
	Double res = a.max(arr);
	if(res != null) {
		System.out.println(a.max(arr));	
	} else {
		System.out.println("输入的数有误");
	}
	
	
	
	}
}

//先完成正常业务，然后再考虑代码健壮性
class A01 {
	public Double max(double... arr) {
		//先判断ar是否为nul1，然后再判断length是否>0
		if(arr != null && arr.length > 0) {
			//如果我设置第一个元素为0的话，数组的元素有可能是负数
			double max = arr[0];//假定第一个元素就是最大值
			for(int i = 1; i < arr.length; i++) {
				if(arr[i] > max) {
					max = arr[i];
				}
			}
			return max; //double
		} else {
			return null; //返回空
		}
		
	}
}