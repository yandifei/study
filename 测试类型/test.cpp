#include <iostream>
#include <typeinfo>

void test() {
    std::cout << "���ǲ��Ժ���" << std::endl;
}

int test2() {
    std::cout << "���ǲ��Ժ���2" << std::endl;
    return 1;
}
int main() {
    test(); //ִ��test����
    std::cout << "test() �ķ�������: " << typeid(test()).name() << std::endl;
    test2(); //ִ��test2����
    std::cout << "test() �ķ�������: " << typeid(test2()).name() << std::endl;
    //����ȥ�����ż�Ϊ��������
    std::cout << "test() �ķ�������: " << typeid(test).name() << std::endl;
    std::cout << "test() �ķ�������: " << typeid(test2).name() << std::endl;
    return 0;
}