import shutil   # shutil.copy2() - 保留元数据（修改时间等）
from pathlib import Path

# 删除整合目录
try:
    shutil.rmtree("ACG画廊数据库服务")
except FileNotFoundError:
    pass

# 需要整合的目录
(target := Path("ACG画廊数据库服务")).mkdir(parents=True, exist_ok=True)
# 日志和用户数据
(target / "outputs" / "logs").mkdir(parents=True, exist_ok=True)

# 程序和依赖包
shutil.copy2("dist/ACG画廊数据库服务/ACG画廊数据库服务.exe", target / "ACG画廊数据库服务.exe")
shutil.copytree("dist/ACG画廊数据库服务/packages", target / "packages", dirs_exist_ok=True, copy_function=shutil.copy2)

# 环境配置数据
shutil.copytree("config", target / "config", dirs_exist_ok=True, copy_function=shutil.copy2)
# 用户数据(目录存在就直接覆盖文件)
shutil.copytree("user_data", target / "user_data", dirs_exist_ok=True, copy_function=shutil.copy2)
# 界面模板
shutil.copytree("templates", target / "templates", dirs_exist_ok=True, copy_function=shutil.copy2)
