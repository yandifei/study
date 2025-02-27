
# 接收传入文件的路径，打印文件的全部内容，如文件不存在则捕获异常，输出提示信息，通过finally关闭文件对象
def print_file_info(file_name):
    try:
        openfile = open(file_name, "r", encoding="UTF-8")
    except Exception as warning:
        print(f"出现异常，异常原因为{warning}")
    else:
            print(openfile.read())  # 打印文件的所有内容
    finally:
        if openfile:
            openfile.close  # 关闭文件

# 接收文件路径以及传入数据,将数据追加写入到文件中
def append_to_file(file_name,data):
    appendfile = open(file_name, "a", encoding="UTF-8")
    appendfile.write("\n" + data)   # 自动换行加的

# 测试地点
if __name__ == '__main__':
    print_file_info("D:\\鸣潮脚本\\Free-my-WW\\bill.txt")
    append_to_file("D:\\鸣潮脚本\\Free-my-WW\\bill.txt", "你好")