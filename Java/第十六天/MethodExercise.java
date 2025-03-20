/*MethodExercise.java -- 方法学习*/
public class MethodExercise {
	public static void main(String[] args) {
		//编写类AA，有一个方法：判断一个数是奇数还是偶数，返回boolean(奇数返回true，偶数返回flase)
		AA a = new AA();
		if(a.isOdd(11)) {
			System.out.println("奇数");
		} else {
			 System.out.println("偶数");
		}
		a.print(10,10,'*');
		
	}
}

class AA {
	/**方法思路
	 * 1. 方法返回的类型
	 * 2. 方法的名字
	 * 3. 方法的实参
	 * 4. 方法体
	*/

	//判断是否为奇数
	public boolean isOdd(int num) {
		// if(num % 2 ！= 0) {
		// 	return false;
		// } else {
		// 	return true;
		// }

		// return num % 2 != 0 ? true; false;
		return num % 2 != 0;	//究极简化
	}

	//根据行、列、字符打印对应行数和列数的字符，
	//比如：行：4，列：4，字符#，则打印相应的效果/
	public void print(int index1, int index2, char word) {
		char[][] arr = new char[index1][index2];
		//赋值
		for(int i = 0; i < arr.length; i++) {
			for(int j = 0; j < arr[i].length; j++) {
				arr[i][j] = word;
			}
		}
		//打印
		for(int i = 0; i < arr.length; i++) {
			for(int j = 0; j < arr[i].length; j++) {
				System.out.print(arr[i][j]);
			}
			System.out.println();	//换行
		}


		System.out.println("======不跑数组打印======");	//换行

		//这里是可以不用跑数组的
		for(int i = 0; i < index1; i++) {
			for(int j = 0; j < index2; j++) {
				System.out.print(word);
			}
			System.out.println();	//换行
		}

	}
}