#include <iostream>
#include <typeinfo>

void test() {
    std::cout << "我是测试函数" << std::endl;
}

int test2() {
    std::cout << "我是测试函数2" << std::endl;
    return 1;
}
int main() {
    test(); //执行test函数
    std::cout << "test() 的返回类型: " << typeid(test()).name() << std::endl;
    test2(); //执行test2函数
    std::cout << "test() 的返回类型: " << typeid(test2()).name() << std::endl;
    //尝试去掉括号即为函数本体
    std::cout << "test() 的返回类型: " << typeid(test).name() << std::endl;
    std::cout << "test() 的返回类型: " << typeid(test2).name() << std::endl;
    return 0;
}