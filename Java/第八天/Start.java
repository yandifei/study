/*Start.java --多重循环控制*/
public class Start {
	public static void main(String[] agrs){
		//打印金字塔
		//1行1个*
		//2行3个*
		//3行5个*
		//3行空2、1
		//  *		2 * 1 -1
		// ***		2 * 2 -1
		//*****		2 * 3 -1
		/*1. 打印矩阵
		2. 打印半个金字塔
		3. 打印空心金字塔
		4. 空心金字塔
		*/
		int level = 50;	//层级
		for(int i = 1; i <= level; i++) {  //i表示层数
			//输出空格
			for(int k = 1; k <= level - i; k++) {
				System.out.print(" ");
			}
			//控制每层的*个数
			for(int j = 1; j <=2 * i - 1; j++) {
				if(j == 1|| j == 2 * i - 1 || i == level) {
					System.out.print("*");
				} else {
					System.out.print(" ");
				}
			}
			System.out.println();
		}

	}
}