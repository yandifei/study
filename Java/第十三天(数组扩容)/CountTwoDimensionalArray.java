/*CountTwoDimensionalArray.java -- 遍历二维数组*/
public class CountTwoDimensionalArray {
	public static void main(String[] args) {
		//int arr[][]={{4,6},{1,4,5,7},{-2}};遍历该二维数组，并得到和
		int arr[][] = {{4, 6}, {1, 4, 5, 7}, {-2}};
		int count = 0;
		for(int i = 0; i < arr.length; i++) {
			for(int j = 0; j < arr[i].length; j++) {
				count += arr[i][j];
			}
		}
		System.out.println("该数组的和是：" + count);
	}
}