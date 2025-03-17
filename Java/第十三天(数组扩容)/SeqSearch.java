/*SeqSearch.java -- 顺序查找*/
import java.util.Scanner;
public class SeqSearch {
	public static void main(String[] args) {
		/*有一个数列:白眉鹰王、金毛狮王、紫衫龙王、青翼蝠王猜数游戏：
		从键盘中输入一个名称，判断数列中是否包含此名称，如果找到了
		就提示找到了，并给出下标值。*/
		//定义数组
		String[] names = {"白眉鹰王", "金毛狮王", "紫衫龙王", "青翼蝠王"};
		System.out.println("请输入猜测的名字");
		Scanner myScanner = new Scanner(System.in);
		String inputName = myScanner.next();
		//遍历数组
		for(int i = 0; i < names.length; i++) {
			if(names[i].equals(inputName)) {
				System.out.println("猜对" + names[i] + " 下标为" + i);
				break; //找到了就退出遍历
			} else if(i == names.length - 1) { //这里必须减1，因为无法遍历到这里
				System.out.println("没有猜对");
			}
		}

	}
}