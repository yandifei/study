"""
2个进程之间通过Socket进行相互通讯,就必须有服务端和客户端
Socket服务端:等待其它进程的连接、可接受发来的消息、可以回复消息
Socket客户端:主动连接服务端、可以发送消息、可以接收回复
"""
# 演示Socket服务端开发
import socket
# 创建Socket对象
socket_server = socket.socket()
# 绑定ip地址和端口
socket_server.bind(("127.0.0.1", 8888))  # 传入的是元组
# 监听端口
socket_server.listen(1)  # listen方法内接受一个整数传参数，表示接受连接的数量
# 等待客户端链接
# result = socket_server.accept()   # 返回的是2元元组
# conn = result[0]    # 客户端和服务端的连接对象
# address = result[1] # 客户端的地址信息
conn, address = socket_server.accept()  # 高级写法
"""
accept 方法返回的是二元元组（链接对象，客户端地址信息）
可以通过 变量1，变量2=socket_server.accept()的形式，直接接受二元元组内的两个元素
accept()方法，是阻塞的方法，等特客户端的链接，如果没有链接，就卡在这一行不向下执行了
"""
print(f"接收到了客户端的信息，客户端的信息是：{address}")
# 接受客户端信息，要使用客户端和服务端的本次链接对象，而非socket_server对象
data = conn.recv(1024).decode("UTF-8")
"""
recv接受的参数是缓冲区大小，一般给1024即可
recv方法的返回值是一个字节数组也就是butes对象，不是字符串，可以通过decode方法通过UTF-8编码，将字节数组转换为字符串对象
"""
print(f"客户端发来的消息是：{data}")
# 发送回复消息
msg = input("请输入你要和客户端回复的消息：").encode("UTF-8")  #encode可以把字符串编码为字节数组对象
conn.send(msg)
# 关闭链接
conn.close()    # 关闭当前客户端的链接
socket_server.close()   # 关闭整个链接（不会等待下一个客户端的链接）