/*ArrayAdd.java -- 数组扩容*/     
import java.util.Scanner;
public class ArrayAdd {
	public static void main(String[] args) {
		// 要求：实现动态的给数组添加元素效果，实现对数组扩容。ArrayAddjava
		// 1）原始数组使用静态分配int[]arr={1,2,3}
		// 2）增加的元素，直接放在数组的最后arr={1，2,3,4}
		// arrNew={1,2,3,4}
		// 3)用户可以通过如下方法来决定是否继续添加，添加成功，是否继续？y/n
		
		// int[] arr = {1, 2, 3};
		// int arr[4] = 5;	//包报错的

		// 思路分析
		// 1. 定义初始数组int[]arr={1,2,3}//下标0-2
		// 2. 定义一个新的数组int[]arrNew= newint[arr。length+1];
		// 3.遍历arr数组，依次将arr的元素拷贝到arrNew数组
		// 4.将 4赋给arrNew[arrNew。length-1]= 4;把4赋给arrNew最后一个元素
		// 5.让arr指向arrNew；arr =arrNew;那么原来arr数组就被销毁
		int[] arr = {1, 2, 3};
		Scanner myScanner = new Scanner(System.in);
		while(true) {
			System.out.println("是否添加元素？y/n");
			char answer = myScanner.next().charAt(0);
			if(answer == 'y') {
				int[] arrNew = new int[arr.length + 1];
				//遍历arr数组，依次将arr的元素拷贝到arrNew数组
				for(int i = 0; i < arr.length; i++) {
					arrNew[i]= arr[i];
				}
				System.out.println("请输入你要添加的元素");
				int input = myScanner.nextInt();
				arrNew[arrNew.length - 1] = input;
				arr = arrNew;	//把arrNew的地址给arr，arr原来的地址会被当成垃圾销毁
				System.out.println("添加成功");
			} else {
				break;	//退出循环
			}
		}
		
		
		//输出arr看看效果
		System.out.println("====arr扩容后元素情况====");
		for(int i = 0; i< arr.length; i++){
			System.out.print(arr[i] + "\t");
		} 
	}
}
