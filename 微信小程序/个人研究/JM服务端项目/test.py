import os
# task = 422866
# links = os.listdir(f"outputs/下载缓存/{task}")
# for link in links:
#     "outputs/下载缓存/{task}"
# print()
from pathlib import Path

dir_path = Path("outputs/下载缓存/422866")
files = [str(p) for p in dir_path.iterdir() if p.is_file()]
print(files)

files = [p.name for p in dir_path.iterdir() if p.is_file()]
print(files)