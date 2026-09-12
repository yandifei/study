import sys
from time import sleep

print(f"{"开始下载":=^100}")
for i in range(101):
    sys.stdout.write(f"\r{i}%[{"*" * i}{"." * (100 - i)}]")  # 将输出写入到标准输出
    sys.stdout.flush()  # # 强制刷新输出，确保进度条立即显示
    sleep(0.05)  # 延迟
print(f"\n{"下载完成":=^100}")