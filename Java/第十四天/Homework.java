/*Homework.java -- 本章作业3*/
public class Homework {
	public static void main(String[] args) {
		/*已知有个升序的数组，要求插入一个元素，该数组顺序依然是升序，比如：
		[10, 12, 90, 45] 添加23后，数组为[10, 12, 23, 45, 90]*/

		/*扩容数组*/
		int[] arr = {10, 12, 90, 45}; //扩容前的数组
		int add = 23; //扩容的值
		//打印最开始的数组
		System.out.println("最开始的数组："); 
		for(int i = 0; i < arr.length; i++) {
			System.out.print(arr[i] + " "); //打印最开始的数组
		}
		System.out.println(""); //换行

		int[] arrNew = new int[arr.length + 1]; //扩容后的数组
		for(int i = 0; i < arr.length; i++) {	//把原来数组的值给扩容后的数组
			arrNew[i] = arr[i];
		}
		arrNew[arr.length] = add;	//把扩容后的数值给新的数组
		arr = arrNew; //把arrNew地址给arr(arr的地址被替换后原来的数组占用的内存就会被回收)
		System.out.println("扩容后的数组："); 
		for(int i = 0; i < arr.length; i++) {
			System.out.print(arr[i] + " "); //打印扩容后的数组
		}
		System.out.println(""); //换行


		/*排序(冒泡排序)*/
		//打印排序前的数组
		System.out.println("排序前的数组："); 
		for(int i = 0; i < arr.length; i++) {
			System.out.print(arr[i] + " "); //打印排序前的数组
		}
		System.out.println(""); //换行

		for(int i = 0; i < arr.length - 1; i++) {
			for(int j = 0, temp = 0; j < arr.length - i - 1; j++, temp = 0) {
				if(arr[j] > arr[j + 1]) {
					temp = arr[j + 1];	//把小的数组放到缓冲变量
					arr[j + 1] = arr[j];	//把大的值往前挪	
					arr[j] = temp;	//把大的值往后挪
				}
			}
		}
		//打印排序后的数组
		System.out.println("排序后的数组："); 
		for(int i = 0; i < arr.length; i++) {
			System.out.print(arr[i] + " "); //打印排序后的数组
		}
		System.out.println(""); //换行
	}
}