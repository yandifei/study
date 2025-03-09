public class IfExercise2 {
	public static void main(String[] agrs) {
		boolean b = true;
		if(false = b) {		//b =false是不会报错的，因为这个一个赋值语句，所以要特别注意=的问题（c语言讲过交换来写来着）
			System.out.println("a");
		} else if(b) {
			System.out.println("c");
		} else if(!b) {
			System.out.println("d");
		}
	}
}