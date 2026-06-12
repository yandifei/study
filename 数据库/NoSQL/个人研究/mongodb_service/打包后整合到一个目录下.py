import shutil   # shutil.copy2() - 保留元数据（修改时间等）
from pathlib import Path

# 删除整合目录
try:
    shutil.rmtree("燕云十六声自动化")
except FileNotFoundError:
    pass

# 需要整合的目录
(target := Path("燕云十六声自动化")).mkdir(parents=True, exist_ok=True)
# 日志和用户数据
(target / "outputs" / "logs").mkdir(parents=True, exist_ok=True)
(target / "outputs" / "screenshots").mkdir(parents=True, exist_ok=True)

# 程序和依赖包
shutil.copy2("dist/燕云十六声自动化/燕云十六声自动化.exe", target / "燕云十六声自动化.exe")
shutil.copytree("dist/燕云十六声自动化/_internal", target / "_internal", dirs_exist_ok=True, copy_function=shutil.copy2)

# 协议和说明
shutil.copy2("LICENSE", target / "LICENSE")
shutil.copy2("README.md", target / "README.md")
shutil.copy2("README.en.md", target / "README.en.md")
# 界面模板
shutil.copytree("resources", target / "resources", dirs_exist_ok=True, copy_function=shutil.copy2)
