/*Homework5.java -- 本章作业3*/
public class Homework5 {
	public static void main(String[] args) {
		/*随机生成10个整数（1-100的范围）保存到数组，并倒序打印以及求平均值、求最大
		值和最大值的下标、并查找里面是否有8*/
		int[] arr = new int[10];
		//生成1-100的整数
		for(int i = 0; i < arr.length; i++) {
			arr[i] = (int)(Math.random() * 100) + 1;	//生成1-100的整数
		}
		System.out.println("打印数组:");	//换行
		//打印数组
		for(int i = 0; i < arr.length; i++) {
			System.out.print(arr[i] + " ");
		}
		
		//倒序
		for(int i = 0, temp = 0; i < arr.length / 2; i++) {
			temp = arr[i];
			arr[i] = arr[arr.length - i - 1];
			arr[arr.length - i -1] = temp;
		}
		System.out.println("倒序打印:");
		//打印数组
		for(int i = 0; i < arr.length; i++) {
			System.out.print(arr[i] + " ");
		}
		System.out.println();	//换行


		//求平均值
		int count = 0;//统计总数值
		for(int i = 0; i < arr.length; i++) {
			count  += arr[i];
		}
		System.out.println("数组的总值:" + count + " 数组的平均值：" + count / arr.length);	//换行

		//求最大值和最大值的下表
		int tempMax = arr[0]; //记录最大值
		int tempMin = arr[0]; //记录最小值
		int indexMax = -1; //记录最大值的下标
		int indexMin = -1; //记录最小值的下标
		for(int i = 0; i < arr.length - 1; i++) {	//这里减1是为了下面的arr[i+1]
			if(tempMax < arr[i + 1]) {
				tempMax  = arr[i + 1];
				indexMax = i + 1;
			}
			if(tempMin > arr[i + 1]){
				tempMin  = arr[i + 1];
				indexMin = i + 1;
			}
		}
		System.out.println("数组的最大值:" + tempMax + " 数组的最大值：" + tempMin);	//换行

		//查找数组中是否有8
		for(int i = 0; i < arr.length; i++) {
			if(arr[i] == 8) {
				System.out.println("存在8");
				break;
			} else if(i == arr.length -1) {	//必须放在if的第二个入口
				System.out.println("不存在8");
			}
		}

	}
}