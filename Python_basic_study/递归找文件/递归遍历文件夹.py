# 递归不能层级太多，不然会溢出
# 导包
import os
from math import degrees

# 函数
def test_os():
    print(os.listdir("D:\\Python_study\\软件安装器和其他程序（黑马）"))               # 遍历文件夹下的路径
    print(os.path.isdir("D:\\Python_study\\软件安装器和其他程序（黑马）\\第15章"))     # 判断路径是一个文件夹
    print(os.path.exists("D:\\Python_study\\软件安装器和其他程序（黑马）\\a"))        # 判断文件夹是否存在

def get_file_path(path):
    file_list = []
    if os.path.exists(path):
        for i in os.listdir(path):
            new_path = path +"/" + i
            if os.path.isdir(new_path):     # 判断是否是文件夹
                file_list += get_file_path(new_path) # 进入新的文件夹继续查找
            else:
                file_list.append(new_path)
        pass
    else:
        print(f"指定的目录{path},不存在")
        return []
    return file_list


if __name__ == '__main__':
    print(get_file_path("D:\\Python_study\\软件安装器和其他程序（黑马）"))
# test_os()