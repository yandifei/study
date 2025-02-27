# 将已经构建好的数据库里面的数据写出，还要以json格式保存到文本里面去
""" 存放数据库数据路径
D:/Python_study/Python_basic_study/数据库数据提出.txt
"""
# 导入必要的宏包
from pymysql import connect # 导入数据库包连接方法
from data_change import * # 导入自定义字符串修改对象
# 数据库数据读取（连接数据库、选择数据库、查询列表所有数据、获得查询数据）

databases = connect(        # 数据库连接
    host="localhost",       # 主机名（IP）
    port=3306,              # 端口
    user="root",            # 账户
    password="yandifei",    # 密码
    autocommit=True         # 开启自动提交
)
print(databases.get_server_info())  # 返回数据库的版本号，用来确定数据库是否连接成功
databases.select_db("py_sql")   #选择导出数据的数据库
databases_cursor = databases.cursor()   # 获得游标用来执行sql语句
databases_cursor.execute("select * from orders")    # 执行查询语句
result_data = databases_cursor.fetchall() # 获得查询的信息(返回的类型是元组)
# 创建导出数据的对象
export_data = DataModification(result_data)
write_data = export_data.data_modification() #对字符串进行处理修改以列表形式返回
# 将处理后的数据写入到文本里去
with open("D:/Python_study/Python_basic_study/数据库数据提出.txt", "w", encoding="UTF-8") as writefile:
    for data_line in write_data:
        print(data_line)
        writefile.writelines(data_line + "\n")   # 加上\n是为了换行