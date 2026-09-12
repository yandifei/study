import time

# 测试append方法
start_time = time.time()
list_append = []
for i in range(1000000):
    list_append.append(i)
end_time = time.time()
print("append方法耗时:", end_time - start_time)

# 测试+运算符
start_time = time.time()
list_plus = []
for i in range(1000000):
    list_plus = list_plus + [i]
end_time = time.time()
print("+运算符耗时:", end_time - start_time)