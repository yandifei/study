import multiprocessing
import time
import math
import os


# 1. 定义一个计算密集型函数
def heavy_computation(number):
    """
    一个计算量大的函数：计算平方根并返回
    """
    # 为了确保计算量足够大，我们在内部也进行一些迭代
    result = 0
    for _ in range(5):  # 增加内部循环以提高单个任务的计算时间
        result = math.sqrt(number)
    return result


# 2. 定义主函数进行并行计算
def parallel_heavy_task(data_size=10_000_000):
    """
    创建大量数据并使用多进程池进行并行处理
    """
    print(f"--- 准备进行并行计算 ---")

    # 获取可用的CPU核心数
    # 将要使用的进程数设置为 CPU 核心数 - 1，保留一个核心给操作系统/其他进程
    num_processes = os.cpu_count()
    if num_processes is None or num_processes == 1:
        # 兜底，如果获取不到或只有1个核心，就用1
        num_processes = 1
    else:
        num_processes -= 1

    print(f"数据量 (列表大小): {data_size:,}")
    print(f"将使用的进程数: {num_processes}")

    # 创建一个包含大量数据的列表
    # 这里创建了一个从1到 data_size 的列表作为输入数据
    input_data = list(range(1, data_size + 1))

    start_time = time.time()

    # 创建一个进程池
    # 'with' 语句确保进程池在使用完毕后被正确关闭
    with multiprocessing.Pool(processes=num_processes) as pool:
        # 使用 map 方法将 heavy_computation 函数应用到 input_data 中的每一个元素上
        # 这是一个同步调用，它会阻塞直到所有结果都计算完毕
        results = pool.map(heavy_computation, input_data)

    end_time = time.time()

    # 打印结果（只打印前5个和最后一个以避免屏幕被刷爆）
    # print(f"\n前5个计算结果: {results[:5]}")
    # print(f"最后一个计算结果: {results[-1]}")

    # 打印耗时
    print(f"\n--- 并行计算完成 ---")
    print(f"总耗时: {end_time - start_time:.2f} 秒")
    print(f"计算结果总数: {len(results):,}")


if __name__ == '__main__':
    # 确保代码只在主程序执行时运行，这是多进程的规范要求
    # 传入更大的数值可以增加计算量，例如 20_000_000 (两千万)
    parallel_heavy_task(data_size=10_000_000)