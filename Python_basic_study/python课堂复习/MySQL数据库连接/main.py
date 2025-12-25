import mysql.connector

# 建立连接
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="yandifei",
  database="test"
)

# 创建游标
cursor = db.cursor()

# 创建表
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")
# 插入数据
sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
# 数据
val = ("test", "test@qq.com")
# 执行
cursor.execute(sql, val)
# 提交事务
db.commit()

# 关闭游标
cursor.close()
# 关闭连接
db.close()

print(f"插入成功，记录ID: {cursor.lastrowid}")