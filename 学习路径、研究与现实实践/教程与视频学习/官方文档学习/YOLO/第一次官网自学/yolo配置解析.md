配置查看
```python
from ultralytics import settings
print(settings)

"""
JSONDict("C:\Users\yandifei\AppData\Roaming\Ultralytics\settings.json"):
{
  "settings_version": "0.0.6",
  "datasets_dir": "B:\\study\\YOLO11学习\\datasets",
  "weights_dir": "weights",
  "runs_dir": "runs",
  "uuid": "a67e8626ae9bbf681c08126a5a60964371cb70d4677abe4b8eea127262c1604d",
  "sync": true,
  "api_key": "",
  "openai_api_key": "",
  "clearml": true,
  "comet": true,
  "dvc": true,
  "hub": true,
  "mlflow": true,
  "neptune": true,
  "raytune": true,
  "tensorboard": false,
  "wandb": false,
  "vscode_msg": true,
  "openvino_msg": true
}
"""
```
# Ultralytics 设置配置

| 名称 | 示例值 | 数据类型 | 描述 |
|------|--------|----------|------|
| settings_version | '0.0.4' | str | Ultralytics 设置版本（不同于 Ultralytics pip 版本） |
| datasets_dir | '/path/to/datasets' | str | 数据集存储目录 |
| weights_dir | '/path/to/weights' | str | 模型权重存储目录 |
| runs_dir | '/path/to/runs' | str | 实验运行存储目录 |
| uuid | 'a1b2c3d4' | str | 当前设置的唯一标识符 |
| sync | True | bool | 可选择将分析和崩溃同步到 Ultralytics HUB |
| api_key | '' | str | Ultralytics HUB API 密钥 |
| clearml | True | bool | 可选择使用 ClearML 日志记录 |
| comet | True | bool | 可选择使用 Comet ML 进行实验跟踪和可视化 |
| dvc | True | bool | 可选择使用 DVC 进行实验跟踪和版本控制 |
| hub | True | bool | 可选择使用 Ultralytics HUB 集成 |
| mlflow | True | bool | 可选择使用 MLFlow 进行实验跟踪 |
| neptune | True | bool | 可选择使用 Neptune 进行实验跟踪 |
| raytune | True | bool | 可选择使用 Ray Tune 进行超参数调优 |
| tensorboard | True | bool | 可选择使用 TensorBoard 进行可视化 |
| wandb | True | bool | 可选择使用 Weights & Biases 日志记录 |
| vscode_msg | True | bool | 当检测到 VS Code 终端时，会启用一个提示以下载 Ultralytics-Snippets 扩展 |
