# 获得自身路径
import os       # 使用这个包好像不需要考虑“\”转义这个问题
from webbrowser import open_new

selfpath = os.path.abspath(__file__)    # 自身当前路径
print(selfpath) # 输出自己的路径（py文件）
current_directory = os.path.dirname(selfpath)   # 获得上级目录，也就是同级目录或者是同个文件夹里面
print(current_directory)    # 打印上级目录，也就是同一个文件夹的目录
# 读取同目录下的文件
with open(os.path.join(current_directory, "路径拼接"), "r", encoding="UTF-8") as filereader:    # 拼接路径
    data = filereader.read()
    print(data)