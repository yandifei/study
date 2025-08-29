from ultralytics import YOLO


# windows用多进程时需要__main__
if __name__ == '__main__':
    # 加载模型
    # 从YAML建立新模型
    model = YOLO("yolo11n.yaml")
    # 加载预验证的模型（建议用于培训）
    model = YOLO("yolo11n.pt")
    # 从YAML和转移重量
    model = YOLO("yolo11n.yaml").load("yolo11n.pt")

    # 训练模型
    results = model.train(data="coco8.yaml", epochs=100, imgsz=640)

    """
    从预训练模型开始（推荐）
from ultralytics import YOLO
from ultralytics import YOLO
model = YOLO("yolo11n.pt")  # pass any model type
results = model.train(epochs=5)

从头开始
from ultralytics import YOLO
model = YOLO("yolo11n.yaml")
results = model.train(data="coco8.yaml", epochs=5)

恢复训练
model = YOLO("last.pt")
results = model.train(resume=True)
    """