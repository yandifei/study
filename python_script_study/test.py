import psutil

# 'pid', 'name', 'username', 'status'
"""利用上下文管理器来高效获取进程的多个信息(比普通的直接调用性能提升约 4 倍)
通过单次系统调用批量获取进程的多个属性，避免多次单独调用造成的性能损耗，尤其适用于需要频繁获取进程信息的场景
"""



p = psutil.Process()  # 获取当前进程对象

# 普通调用（获取多个慢）
name = p.name()  # 进程名称（首次调用触发批量采集）
cpu_times = p.cpu_times()  # CPU 时间（直接读缓存）
cpu_percent = p.cpu_percent()  # CPU 使用率（直接读缓存）
create_time = p.create_time()  # 进程创建时间（直接读缓存）
ppid = p.ppid()  # 父进程 PID（直接读缓存）
status = p.status()  # 进程状态（直接读缓存）

# 高级调用（获取多个快）
try:
    with p.oneshot(): # 进入高效批处理模式
        name = p.name()  # 进程名称（首次调用触发批量采集）
        cpu_times = p.cpu_times()  # CPU 时间（直接读缓存）
        cpu_percent = p.cpu_percent()  # CPU 使用率（直接读缓存）
        create_time = p.create_time()  # 进程创建时间（直接读缓存）
        ppid = p.ppid()  # 父进程 PID（直接读缓存）
        status = p.status()  # 进程状态（直接读缓存）
except psutil.NoSuchProcess:
    print("进程已终止")

print(name)
# print(cpu_times)
print(cpu_percent)
print(create_time)
print(ppid)
print(status)