# 使用mysql和python进行连接（第一次使用不同的软件和不同的语言对接）
# 导入需要的pymysql的包
from pymysql import connect
# 获取到MySQL数据库的链接对象(构建mysql的数据库链接)
conn = connect(
    host="localhost",   # 主机名（IP）
    port=3306,          # 端口
    user="root",        # 账户
    password="yandifei",# 密码
    autocommit=True     # 开启自动提交
)
print(conn.get_server_info()) #返回的是mysql服务器的版本
# 执行非查询性质SQL
cursor = conn.cursor()  # 获取游标对象
""" 数据查询
# 选择数据库
conn.select_db("db_p")
# 执行sql
cursor.execute("select * from emp")    # 这里可以不用写“;”的
# 获得查询的信息
result = cursor.fetchall() # 返回的类型是元组，一条元素是一个元组，全部加在一起是一个大的元组，简称嵌套
for r in result:
    print(r)
# print(result)
"""
#执行查询性质SQL
"""数据插入"""
# 选择数据库
conn.select_db("python_study")
# 执行sql
# insert into student(id, name, age) values(1, '周杰伦', 31),(4, '林俊杰', 33);
cursor.execute("insert into student values(1, '周杰伦', 31)")    # 这里可以不用写“;”的
# conn.commit()   # 确认更改，如果不确认就会无法真正修改（也可以在连接的时候选择自动提交为True）
# 获得查询的信息
# 关闭链接
conn.close()



