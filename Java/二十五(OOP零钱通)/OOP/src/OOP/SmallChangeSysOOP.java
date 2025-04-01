package OOP;




import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;

/**
 *该类是完成零钱通的各个功能的类
 *使用OOP（面向对象编程）
 * 将各个功能对应一个方法
 */
public class SmallChangeSysOOP {
    //属性
    boolean loop = true;
    Scanner scanner = new Scanner(System.in);
    String key;

    String details = "---------------零钱通明细---------------";

    double money = 0;
    double balance = 0;
    Date date = null;
    SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");

    String note = "";

    public void mainMenu() {
        do {
            System.out.println("\n================零钱通菜单(OOP)===============");
            System.out.println("\t\t\t1零钱通明细");
            System.out.println("\t\t\t2 收益入账");
            System.out.println("\t\t\t3 消费");
            System.out.println("\t\t\t4 退出");

            System.out.print("请选择(1-4):");
            key = scanner.next();

            //使用switch分支控制
            switch (key) {
                case "1" :
                    this.details();
                    break;
                case "2" :
                    this.income();
                    break;
                case "3" :
                    this.pay();
                    break;
                case "4" :
                    this.exit();
                    break;
                default:
                    System.out.println("选择有误，请重新选择");
            }
        } while (loop);
    }

    //完成零钱通明细
    public void details() {
        System.out.println(details);
    }

    //完成收益入账
    public void income() {
        System.out.print("收益入账金额：");
        money = scanner.nextDouble();
        if (money <= 0) {
            System.out.println("收益入账金额需要大于0");
            return; //退出方法，不再执行
        }
        balance += money;
        date = new Date();
        details += "\n收益入账\t+" + money + "\t" + sdf.format(date)+ "\t" + balance;
    }

    //消费
    public void pay() {
        System.out.print("消费金额:");
        money = scanner.nextDouble();
        if(money <= 0 || money > balance) {
            System.out.println("你的消费金额 应该在 0-" + balance);
            return;
        }
        System.out.print("消费说明:");
        note = scanner.next();
        balance -= money;
        //拼接消费信息到details
        date = new Date();//获取当前日期
        details += "\n" + note + "\t\t-" + money + "\t" + sdf.format(date) + "\t" + balance;
    }

    public void exit() {
        String choice = "";
        while (true) {
            System.out.println("你确定要退出吗?y/n");
            choice = scanner.next();
            if ("y".equals(choice) || "n".equals(choice)) {
                return;
            }
            if(choice.equals("y")) {
                loop = false;
            }
            return;
        }
    }
}
