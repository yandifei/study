/*BubbleSort.java -- 冒泡排序*/
import java.util.Scanner;
public class BubbleSort {
	public static void main(String[] args) {
	Scanner myScaner = new Scanner(System.in);
	//后面一定有机会改的，这里就留着吧

	int[] arr = {11, 54, 12, 99, 88, 1};
	//打印初始数组
	System.out.println("未排序的数组:");	//换行
	for(int i = 0; i < arr.length; i++) {
		System.out.print(arr[i] + " ");
	}
	System.out.println();	//换行

	//开始排序
	// temp//临时存储
	for(int i = 1; i <= arr.length - 1; i++) {	//需要排序4次
		for(int index = 0, temp = 0; index < arr.length - i; index++, temp = 0) { //每次排序比较单前的排序次数
			if(arr[index] > arr[index + 1]) {
				temp = arr[index + 1];	//把小的数保存到临时变量里面
				arr[index + 1] = arr[index]; //把大的数往后挪一个位置
				arr[index] = temp; //把小的数挪到前一位去
			}
		}
	}

	//打印排序结果
	for(int i = 0; i < arr.length; i++) {
		System.out.print(arr[i] + " ");
	}
	}
}