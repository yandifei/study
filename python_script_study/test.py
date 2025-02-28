import psutil
import time

def monitor_cpu(interval=1, percpu=False):
    print("开始监控 CPU 使用率（按 Ctrl+C 停止）...")
    try:
        while True:
            usage = psutil.cpu_percent(interval=interval, percpu=percpu)
            if percpu:
                core_str = " | ".join([f"Core {i}: {u}%" for i, u in enumerate(usage)])
                print(f"CPU 核心利用率: {core_str}")
            else:
                print(f"当前系统 CPU 利用率: {usage}%")
    except KeyboardInterrupt:
        print("监控已停止。")
# 监控整体 CPU 使用率
monitor_cpu(interval=1)

# 监控每个核心（取消注释运行）
# monitor_cpu(interval=1, percpu=True)