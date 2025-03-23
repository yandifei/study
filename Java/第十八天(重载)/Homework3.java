/*Homework3.java -- 本章作业03*/
public class Homework3 {
	public static void main(String[] args) {
	// 编写类Book，定义方法updatePrice，实现更改某本书的价格
	// 具体：如果价格>150,则更改为150,如果价格>100,更改为100，否则不变
	Book book = new Book("小红帽", 900);
	book.updatePrice(book.price);
	System.out.println("书名：" + book.name + " 价格：" + book.price);
	}
}

class Book {
	String name;
	double price;
	public Book(String name, double price) {
		this.name = name;
		this.price = price;
	}
	public void updatePrice(double price) {
		if(price > 150) {
			this.price = 150;
		} else if(price > 100) {
			this.price = 100;
		}
	}
}
