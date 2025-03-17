/*YanHui.java -- 杨辉三角打印*/
public class YanHui {
	public static void main(String[] args) {
		/*使用二维数组打印一个10行杨辉三角
		1
		1  1
		1  2  1
		1  3  3  1
		1  4  6  4  1
		1  5  10 10 5  1
		*/
		int[][] yanHui = new int[10][];
		for(int i = 0; i < yanHui.length; i++) { //遍历二维数组的每个元素 
			//给每个一维数组开辟空间
			yanHui[i] = new int[i + 1];
			//给每个一维数组(行)赋值
			for(int j = 0; j < yanHui[i].length; j++) {
				if(j == 0 || j == yanHui[i].length - 1) {
					yanHui[i][j] = 1;
				} else {	//中间的元素
					yanHui[i][j] = yanHui[i - 1][j] + yanHui[i - 1][j - 1]; 
				}

			}
		}
		//输出杨辉三角
		for(int i = 0; i < yanHui.length; i++) {
			for(int j = 0; j < yanHui[i].length; j++) {
				System.out.print(yanHui[i][j] + "\t");
			}
		System.out.println(); //换行
		}
	}
}
