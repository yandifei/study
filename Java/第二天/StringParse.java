public class StringParse {
	public static void main(String[] args) {
		//String转换为不同的类型
		String s1 = "123";
		int num1 = Integer.parseInt(s1);
		double num2 = Double.parseDouble(s1);
		float num3 = Float.parseFloat(s1);
		long num4 = Long.parseLong(s1);
		byte num5 = Byte.parseByte(s1);
		boolean num6 = Boolean.parseBoolean("true");
		short num7 = Short.parseShort(s1);

		System.out.println(num1);
		System.out.println(num2);
		System.out.println(num3);
		System.out.println(num4);
		System.out.println(num5);
		System.out.println(num6);
		System.out.println(num7);
	}
}