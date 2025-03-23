/*Homework2.java -- 本章作业02*/
public class Homework2 {
	public static void main(String[] args) {
		// 2.编写类A02，定义方法find，实现查找某字符串数组中的元素查找，并返回索引，
		// 如果找不到，返回-1.Homework02.java
		A02 a = new A02();
		// System.out.println(a.find("a","aa", "sdf", "nihao1", "a"));
		String[] myArr = {"a","aa", "sdf", "nihao1", "b"};
		Integer res = a.find("b",myArr);
		if(res != null) {
			System.out.println(res);
		} else {
			System.out.println("输入错误");
		}
		

	}
}

//自己补充代码健壮性
class A02 {
	public Integer find(String string,String... arr) {
		if(string != null && arr != null && arr.length > 0) {
			for(int i = 0; i < arr.length; i++) {
				if(string.equals(arr[i])) {
					return i;//后面的语句都不执行
				}
			}
			//如果没有就返回-1
			return -1;
		} else {
			return null;//输入错误
		}

		
	}
}

