# 导包
import socket
# 创建对象
socket_client = socket.socket()
# 连接服务端
socket_client.connect(("localhost", 8888))
# 发送消息
while True:
    send_msg =input("请输入要发送的信息:")
    if send_msg == "结束聊天":
        break
    socket_client.send(send_msg.encode("UTF-8"))    #发送消息
    # 接收返回的消息
    recv_data = socket_client.recv(1024)    # 1024是缓冲区大小，一般1024即可
    # recv方法是阻塞式的，即不接收到返回，就卡在这里等待
    print("服务端回复的消息是：", recv_data.decode("UTF-8"))  #接受的消息需要通过UTF-8解码为字符串



# 关闭连接
socket_client.close()   # 最后通过close关闭连接


