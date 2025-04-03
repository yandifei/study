package Homework08;

public class Homework8 {
    /*要求:
    （1）在上面类的基础上扩展新类CheckingAccount对每次存款和取款都收取1美元的手续费
    （2）扩展前一个练习的BankAccount类，新类SavingsAccount每个月都有利息产生
    （earnMonthlyInterest方法被调用），并且有每月三次免手续费的存款或取款。
    在earnMonthlylnterest方法中重置交易计数
    （3）体会重写的好处
    */
    public static void main(String[] args) {
        CheckingAccount checkingAccount = new CheckingAccount(1000);
        checkingAccount.deposit(10); //1010-1=1009
        System.out.println(checkingAccount.getBalance());
        checkingAccount.withdraw(9); //1009 - 9 = 1000 - 1


        //测试SavingAccount
        SavingAccount savingAccount = new SavingAccount(1000);
        savingAccount.deposit(100);
        savingAccount.deposit(100);
        savingAccount.deposit(100);
        System.out.println(savingAccount.getBalance()); //1300
        savingAccount.deposit(100);
        System.out.println(savingAccount.getBalance()); //1399
        //月初
        savingAccount.earnMonthlyInterest();
        System.out.println(savingAccount.getBalance());//1399 + 13.99（利息）
        savingAccount.withdraw(100); //免手续费
        System.out.println(savingAccount.getBalance()); //1412.99 - 100 = 1312.99
        savingAccount.withdraw(100); //免手续费
        savingAccount.withdraw(100); //免手续费
        System.out.println(savingAccount.getBalance()); //1312.99 - 200 = 1112.99
        savingAccount.deposit(100); //手续费1元
        System.out.println(savingAccount.getBalance()); //1112.99 + 100 - 1 = 1211.99


    }
}





