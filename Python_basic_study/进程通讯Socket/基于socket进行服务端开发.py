"""
2个进程之间通过Socket进行相互通讯,就必须有服务端和客户端
Socket服务端:等待其它进程的连接、可接受发来的消息、可以回复消息
Socket客户端:主动连接服务端、可以发送消息、可以接收回复
进阶版：多次收发信息
"""
# 演示Socket服务端开发
import socket
socket_server = socket.socket() # 创建Socket对象
socket_server.bind(("localhost", 8888))  # 传入的是元组# 绑定ip地址和端口
socket_server.listen(1)  # listen方法内接受一个整数传参数，表示接受连接的数量# 监听端口
conn, address = socket_server.accept()  # 高级写法# 等待客户端链接
print(f"接收到了客户端的信息，客户端的信息是：{address}")

while True:
    data = conn.recv(1024).decode("UTF-8") # 接收客户端的消息
    print(f"客户端发来的消息是：{data}")  # 打印消息
    if data == "结束聊天":
         break
    msg = input("请输入你要和客户端回复的消息：")
    conn.send(msg.encode("UTF-8"))# encode可以把字符串编码为字节数组对象
# 关闭链接
conn.close()    # 关闭当前客户端的链接
socket_server.close()   # 关闭整个链接（不会等待下一个客户端的链接）