/*ReturnStudy.java -- 学习*/
public class ReturnStudy {
	public static void main(String[] agrs) {
		for(int i=1;i<=5;i++){
			if(i==3){
				System.out.println("教育"+i);
				return;//当retyrn用在方法时，表示跳出方法，如果使用在main中则代表退出程序
			}
			System.out.println("Hello World!");
		}
		System.out.println("go on..");
	}
}

