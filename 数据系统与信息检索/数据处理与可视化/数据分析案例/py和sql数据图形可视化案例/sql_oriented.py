# 这里是用来构建数据库和python相关操作的函数方法
# 导入需要的pymysql的包
from pymysql import connect

# 数据库连接
def databases_insert(all_data):
    # 获取到MySQL数据库的链接对象(构建mysql的数据库链接)
    databases = connect(
        host="localhost",   # 主机名（IP）
        port=3306,          # 端口
        user="root",        # 账户
        password="yandifei",# 密码
        autocommit=True     # 开启自动提交
    )
    print(databases.get_server_info()) #返回的是mysql服务器的版本(判断数据库是否链接成功)
    databases_cursor = databases.cursor()  # 获得游标对象用来执行之后的sql语句操作
    # 创建数据库，字符集为utf8(如果数据库存在则不创建)# 执行sql
    databases_cursor.execute("create database if not exists py_sql charset utf8;")    # 这里可以不用写“;”的
    databases.select_db("py_sql")  # 选择对应的数据库
    # 创建需要的表格(如果表格不存在才创建)
    databases_cursor.execute(
        "create table if not exists orders("
        "order_data date,"
        "order_id varchar(255),"
        "money varchar(10),"
        "province varchar(255)"
        ")"
    )
    # 数据输入语句
    for put_data in all_data:
        sql = f"insert into orders(order_data, order_id, money, province) " \
              f"values('{put_data.date}','{put_data.order_id}','{put_data.money}','{put_data.province}')"
        #执行插入语句
        databases_cursor.execute(sql)
    # 关闭数据库连接
    databases.close()











