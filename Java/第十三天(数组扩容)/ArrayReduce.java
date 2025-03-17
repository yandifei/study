/*ArrayReduce.java -- 数组减少*/
import java.util.Scanner;
public class ArrayReduce {
	public static void main(String[] args) {
		// 有一个数组（1，2，3，4，5}，可以将该数组进行缩减，提示用户是否继续缩
		// 减，每次缩减最后那个元素。当只剩下最后一个元素，提示，不能再缩减。
		int[] arr = {1, 2, 3, 4, 5};
		//打印数组
		System.out.println("当前前数组：");
		for(int i = 0; i < arr.length; i++) {
			System.out.print(arr[i] + " ");
		}
		System.out.println();	//换行
		
		//循环减少
		Scanner myScanner = new Scanner(System.in);
		while(true) {
			System.out.println("是否缩减元素？ y/n");
			char answer = myScanner.next().charAt(0);
			if(answer == 'y') {
				if(arr.length - 1 < 0) {
					System.out.println("已经是最后一个元素了，无法缩减");
					break;
				}
				int[] arrNew = new int[arr.length - 1];
				for(int i = 0; i < arr.length - 1; i++){
					arrNew[i] = arr[i];
				}
				arr = arrNew; //把改变后的地址给会数组
				//打印缩减后的数组
				System.out.println("缩减后的数组：");
				for(int i = 0; i < arr.length; i++) {
					System.out.print(arr[i] + " ");
				}
			} else {	//退出缩减
				break;
			}
		}
		
	}
}