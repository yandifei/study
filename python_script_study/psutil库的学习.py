import psutil


def get_cpu_times(per_cpu=False):
    return_value = psutil.cpu_times(per_cpu)   # 原生默认也是False的
    return_value_explain = set()   # 创建字典来解释返回值的参数
    if per_cpu: # 默认总的逻辑 CPU
        for s_cpu_times in psutil.cpu_times():
            s_cpu_times
        # replace_name = return_value[0]
        # replace_name

# 在用户模式下执行的正常进程所花费的时间
# 在内核模式下执行的进程所花费的时间
# 无所事事所花费的时间
# 处理硬件中断所花费的时间
# 为延迟过程调用 （DPC） 提供服务所花费的时间( DPC 是以低于标准中断的优先级运行的中断)
print(psutil.cpu_times())
for i in psutil.cpu_times():
    print(i)

