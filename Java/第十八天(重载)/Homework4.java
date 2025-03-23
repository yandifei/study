/*Homework4.java -- 本章作业04*/
public class Homework4 {
	public static void main(String[] args) {
	// 编写类A03，实现数组的复制功能copyArr，输入旧数组，返回一个新数组，元素利旧数组一样
	int[] arr = {1, 2, 3, 4, 5, 6};
	A03 a03 = new A03();
	for(int i = 0; i < a03.copyArr(arr).length; i++) {
		System.out.print(a03.copyArr(arr)[i] + " ");
	}

	}
}

class A03 {
	public int[] copyArr(int[] arr) {
		int[] newArr = new int[arr.length];
		for(int i = 0; i < arr.length; i++) {
			newArr[i] = arr[i];
		}
		return newArr;
	}
}