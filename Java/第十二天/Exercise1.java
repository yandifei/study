/*Exercise1.java -- 数组练习1*/
public class Exercise1 {
	public static void main(String[] agrs) {
		/*创建一个char类型的26个元素的数组，分别放置'A'-'Z'。
		  使用for循环访问所有元素并打印出来。
		  提示：char类型数据运算'A'+2->'c'
		*/
		//我的
		// char[] letters = new char[26];
		// int j = 0;
		// for(char i = 'A'; i <= 'Z'; i++, j++) {
		// 	letters[j] = i;
		// }

		//视频的
		char[] letters = new char[26];
		for(int i = 0; i < letters.length; i++) {
			//letters 是 char[]类型
			//letters[i] 是 char类型
			letters[i] = (char)('A' + i);	//因为系统无法判定i是否会超过最大编码数(65535)所以不会自动转换
		}

		for(int i = 0; i < letters.length; i++) {
			System.out.print(letters[i] + " ");
		}
	}
}