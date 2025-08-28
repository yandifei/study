"""
加载模型、训练模型、评估其在验证集上的性能，将其导出为 ONNX 格式。
"""
from ultralytics import YOLO

# 从头开始创建新的Yolo模型
model = YOLO("yolo11n.yaml")

# 加载预验证的Yolo型号（建议用于训练）
model = YOLO("yolo11n.pt")

# 使用3个时代的“ Coco8.yaml”数据集训练模型
results = model.train(data="coco8.yaml", epochs=3)

# 评估模型在验证集上的性能
results = model.val()

# 使用模型在图像上执行对象检测
results = model("https://ultralytics.com/images/bus.jpg")

# 将模型导出到ONNX格式
success = model.export(format="onnx")