/*ArrayReverse.java -- 数组倒装*/
public class ArrayReverse {
	public static void main(String[] args) {
		// 思考2min
		// 方式1：通过找规律反转专【思路分析】
		// 方式2：使用逆序赋值方式【思路分析，学员自己完成

		//方法一规律
		//1. 把arr[0]和arr[5]进行交换{66,22,33,44,55,11}
		//2.把arr[1]和arr[4]进行交换{66,55,33,44,22,11}
		//3.把arr[2]和arr[3] 进行交换{66,55,44,33,22,11}
		//4.一共要交换3次 = arr。length/ 2
		//5.每次交换时，对应的下标是arr[i]和arr1[arr。length-1-i]

		//打印最开始的数组
		int[] arr = {11, 22, 33, 44, 55, 66, 80};
		System.out.println("原来的数组：");
		for(int i = 0; i < arr.length; i++) {
			System.out.print(arr[i] + " ");
		}
		System.out.println();	//换行

		//方式1
		int temp = 0;
		int len = arr.length;
		for(int i = 0; i < len / 2; i++) {	//不用担心因为精度丢失导致循环次数不对，这里丢失了中间的数就不用倒转了
			temp = arr[len - 1 - i];
			arr[len - 1 - i] = arr[i];
			arr[i] = temp;
		}
		for(int i = 0; i < arr.length; i++) {
			System.out.print(arr[i] + " ");
		}
		System.out.println();	//换行


		//方式2
		int[] arrReverse = new int[arr.length]; //创建一个和arr空间大小一样的数组
		for(int i = 0; i < arr.length; i++) {
			arrReverse[i] = arr[arr.length - i -1];		//不加减1会导致溢出
		}
		System.out.println("倒转后的数组：");
		for(int i = 0; i < arrReverse.length; i++) {
			System.out.print(arrReverse[i] + " ");
		}
	}
}