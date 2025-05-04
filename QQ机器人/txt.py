

from time import perf_counter

start = perf_counter()  # 最高精度计时器
# 要计时的代码
# print(sum(range(1000000)))    # 计算密集型操作示例
end = perf_counter()
print(f"耗时: {end - start:.6f} 秒")
# 输出示例：耗时: 0.034765 秒