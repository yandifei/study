# 练习22(自定义包的实战)
# 你的包文件名不能带有中文或者中文符号，且包储存路径在site-packages里，这两点做到包对

from my_utils.str_util import *  # 导入自定义的包
from my_utils.file_util import *  # 导入自定义的包
print(str_reverse("asdfas"))
print(substr("asdfas", 1, 3))
print_file_info("D:\\鸣潮脚本\\Free-my-WW\\bill.txt")
append_to_file("D:\\鸣潮脚本\\Free-my-WW\\bill.txt", "你好")