### 检测模型（Detection – COCO）
| 模型    | 尺寸<br>(像素) | mAPval<br>50-95 | mAPval<br>50-95(e2e) | CPU ONNX<br>速度(ms) | T4 TensorRT10<br>速度(ms) | 参数量<br>(M) | FLOPs<br>(B) | 下载链接                                                                                |
| :------ | :------------- | :-------------- | :------------------- | :------------------- | :------------------------ | :------------ | :----------- | :-------------------------------------------------------------------------------------- |
| YOLO26n | 640            | 40.9            | 40.1                 | 38.9 ± 0.7           | 1.7 ± 0.0                 | 2.4           | 5.4          | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26n.pt) |
| YOLO26s | 640            | 48.6            | 47.8                 | 87.2 ± 0.9           | 2.5 ± 0.0                 | 9.5           | 20.7         | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26s.pt) |
| YOLO26m | 640            | 53.1            | 52.5                 | 220.0 ± 1.4          | 4.7 ± 0.1                 | 20.4          | 68.2         | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26m.pt) |
| YOLO26l | 640            | 55.0            | 54.4                 | 286.2 ± 2.0          | 6.2 ± 0.2                 | 24.8          | 86.4         | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26l.pt) |
| YOLO26x | 640            | 57.5            | 56.9                 | 525.8 ± 4.0          | 11.8 ± 0.2                | 55.7          | 193.9        | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26x.pt) |

### 分割模型（Segmentation – COCO-Seg）
| 模型        | 尺寸<br>(像素) | mAPbox<br>50-95(e2e) | mAPmask<br>50-95(e2e) | CPU ONNX<br>速度(ms) | T4 TensorRT10<br>速度(ms) | 参数量<br>(M) | FLOPs<br>(B) | 下载链接                                                                                    |
| :---------- | :------------- | :------------------- | :-------------------- | :------------------- | :------------------------ | :------------ | :----------- | :------------------------------------------------------------------------------------------ |
| YOLO26n-seg | 640            | 39.6                 | 33.9                  | 53.3 ± 0.5           | 2.1 ± 0.0                 | 2.7           | 9.1          | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26n-seg.pt) |
| YOLO26s-seg | 640            | 47.3                 | 40.0                  | 118.4 ± 0.9          | 3.3 ± 0.0                 | 10.4          | 34.2         | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26s-seg.pt) |
| YOLO26m-seg | 640            | 52.5                 | 44.1                  | 328.2 ± 2.4          | 6.7 ± 0.1                 | 23.6          | 121.5        | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26m-seg.pt) |
| YOLO26l-seg | 640            | 54.4                 | 45.5                  | 387.0 ± 3.7          | 8.0 ± 0.1                 | 28.0          | 139.8        | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26l-seg.pt) |
| YOLO26x-seg | 640            | 56.5                 | 47.0                  | 787.0 ± 6.8          | 16.4 ± 0.1                | 62.8          | 313.5        | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26x-seg.pt) |

### 分类模型（Classification – ImageNet）
| 模型        | 尺寸<br>(像素) | 准确率<br>top1 | 准确率<br>top5 | CPU ONNX<br>速度(ms) | T4 TensorRT10<br>速度(ms) | 参数量<br>(M) | FLOPs<br>(B) at 224 | 下载链接                                                                                    |
| :---------- | :------------- | :------------- | :------------- | :------------------- | :------------------------ | :------------ | :------------------ | :------------------------------------------------------------------------------------------ |
| YOLO26n-cls | 224            | 71.4           | 90.1           | 5.0 ± 0.3            | 1.1 ± 0.0                 | 2.8           | 0.5                 | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26n-cls.pt) |
| YOLO26s-cls | 224            | 76.0           | 92.9           | 7.9 ± 0.2            | 1.3 ± 0.0                 | 6.7           | 1.6                 | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26s-cls.pt) |
| YOLO26m-cls | 224            | 78.1           | 94.2           | 17.2 ± 0.4           | 2.0 ± 0.0                 | 11.6          | 4.9                 | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26m-cls.pt) |
| YOLO26l-cls | 224            | 79.0           | 94.6           | 23.2 ± 0.3           | 2.8 ± 0.0                 | 14.1          | 6.2                 | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26l-cls.pt) |
| YOLO26x-cls | 224            | 79.9           | 95.0           | 41.4 ± 0.9           | 3.8 ± 0.0                 | 29.6          | 13.6                | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26x-cls.pt) |

### 姿态估计模型（Pose – COCO-Pose）
| 模型         | 尺寸<br>(像素) | mAPpose<br>50-95(e2e) | mAPpose<br>50(e2e) | CPU ONNX<br>速度(ms) | T4 TensorRT10<br>速度(ms) | 参数量<br>(M) | FLOPs<br>(B) | 下载链接                                                                                     |
| :----------- | :------------- | :-------------------- | :----------------- | :------------------- | :------------------------ | :------------ | :----------- | :------------------------------------------------------------------------------------------- |
| YOLO26n-pose | 640            | 57.2                  | 83.3               | 40.3 ± 0.5           | 1.8 ± 0.0                 | 2.9           | 7.5          | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26n-pose.pt) |
| YOLO26s-pose | 640            | 63.0                  | 86.6               | 85.3 ± 0.9           | 2.7 ± 0.0                 | 10.4          | 23.9         | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26s-pose.pt) |
| YOLO26m-pose | 640            | 68.8                  | 89.6               | 218.0 ± 1.5          | 5.0 ± 0.1                 | 21.5          | 73.1         | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26m-pose.pt) |
| YOLO26l-pose | 640            | 70.4                  | 90.5               | 275.4 ± 2.4          | 6.5 ± 0.1                 | 25.9          | 91.3         | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26l-pose.pt) |
| YOLO26x-pose | 640            | 71.6                  | 91.6               | 565.4 ± 3.0          | 12.2 ± 0.2                | 57.6          | 201.7        | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26x-pose.pt) |

### 旋转框检测模型（OBB – DOTAv1）
| 模型        | 尺寸<br>(像素) | mAPtest<br>50-95(e2e) | mAPtest<br>50(e2e) | CPU ONNX<br>速度(ms) | T4 TensorRT10<br>速度(ms) | 参数量<br>(M) | FLOPs<br>(B) | 下载链接                                                                                    |
| :---------- | :------------- | :-------------------- | :----------------- | :------------------- | :------------------------ | :------------ | :----------- | :------------------------------------------------------------------------------------------ |
| YOLO26n-obb | 1024           | 52.4                  | 78.9               | 97.7 ± 0.9           | 2.8 ± 0.0                 | 2.5           | 14.0         | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26n-obb.pt) |
| YOLO26s-obb | 1024           | 54.8                  | 80.9               | 218.0 ± 1.4          | 4.9 ± 0.1                 | 9.8           | 55.1         | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26s-obb.pt) |
| YOLO26m-obb | 1024           | 55.3                  | 81.0               | 579.2 ± 3.8          | 10.2 ± 0.3                | 21.2          | 183.3        | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26m-obb.pt) |
| YOLO26l-obb | 1024           | 56.2                  | 81.6               | 735.6 ± 3.1          | 13.0 ± 0.2                | 25.6          | 230.0        | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26l-obb.pt) |
| YOLO26x-obb | 1024           | 56.7                  | 81.7               | 1485.7 ± 11.5        | 30.5 ± 0.9                | 57.6          | 516.5        | [下载](https://github.com/ultralytics/ultralytics/releases/download/v8.4.30/yolo26x-obb.pt) |

### 使用建议
- **精度优先**：在同类任务中，模型从 **n → s → m → l → x** 精度（mAP/准确率）逐步提升，但参数量和计算量（FLOPs）也显著增加。
- **速度优先**：CPU 或 GPU 上推理速度最快的通常是 **n** 型号，适合实时应用或资源受限设备。
- **任务选择**：根据具体需求选择带对应后缀的模型（`-seg` 分割、`-pose` 姿态估计、`-obb` 旋转框检测、`-cls` 分类）。