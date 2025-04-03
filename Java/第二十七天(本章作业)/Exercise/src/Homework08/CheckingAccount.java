package Homework08;

class CheckingAccount extends BankAccount { //新的账号
    //属性无

    public CheckingAccount(double initialBalance) {
        super(initialBalance);
    }

    @Override
    public void deposit(double amount) {//存款
        super.deposit(amount - 1); //巧妙的使用了父类的deposit
        //一块钱如银行的账号
    }

    @Override
    public void withdraw(double amount) {//取款
        super.withdraw(amount + 1);
        //一块钱转入银行的账号
    }


}
