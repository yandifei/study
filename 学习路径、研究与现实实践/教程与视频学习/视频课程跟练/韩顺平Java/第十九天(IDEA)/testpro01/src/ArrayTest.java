public class ArrayTest {
    public static void main(String[] args) {
        MyTools mt = new MyTools();
        int[] arr = {10, -1, 8, 0, 34};
        mt.bubbleSorting(arr);
        //输出排序后的arr，引用传
        System.out.println("===排序后的arr===");
        for (int j : arr) {
            System.out.print(j + " ");
        }
    }
}
//创建一个类MyTools，编写一个方法，可以完成对int数组冒泡排序的功能
class MyTools {
    public void bubbleSorting(int[] arr) {
        //冒泡排序
        int temp = 0;
        for(int i = 0; i < arr.length - 1; i++) { //外层循环次数 arr.length - 1
            for(int j = 0; j < arr.length - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    temp = arr[j + 1];
                    arr[j + 1] = arr[j];    //交换
                    arr[j] = temp;
                }
            }
        }
    }
}