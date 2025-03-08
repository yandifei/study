public class Selfadd {
	public static void main(String[] agrs) {
		int i = 1;
		i = i++;	//temp=i;i=i+i;i=temp;
		i = ++i;	//i=i+i;temp=i;i=temp;
		System.out.println(i);
	}
}