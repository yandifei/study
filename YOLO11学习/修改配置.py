# 修改设置
# Ultralytics 可以通过以下方式轻松修改设置：
from ultralytics import settings

# 更新设置
settings.update({"runs_dir": "/path/to/runs"})
print(settings)
# 更新多个设置
settings.update({"runs_dir": "/path/to/runs", "tensorboard": False})
print(settings)
# 重置设置为默认值
settings.reset()
print(type(settings))
