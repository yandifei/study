import PIL.Image
from ultralytics import YOLO
import cvat_sdk.auto_annotation as cvataa

# 模型路径
model_path = "yolo.pt"
"""
cvat-cli --server-host app.cvat.ai --auth <你的用户名>:<你的密码> auto-annotate <TASK_ID> --function-file ./yolo.py --model-path ./your_model.pt --allow-unmatched-labels
"""

# 加载本地模型，脚本运行后，模型会自动加载到你的显卡上进行推理
model = YOLO(model_path)
# 自动定义标签规范，该代码会自动从模型中提取标签名称（如 "fight"）和对应 ID，并同步给 CVAT
spec = cvataa.DetectionFunctionSpec(
    labels=[cvataa.label_spec(name, id) for id, name in model.names.items()],
)

def _yolo_to_cvat(results):
    """将 YOLO 推理结果转换为 CVAT SDK 要求的格式"""
    for result in results:
        for box, label in zip(result.boxes.xyxy, result.boxes.cls):
            # 转换坐标为 [xtl, ytl, xbr, ybr] 格式
            yield cvataa.rectangle(int(label.item()), [p.item() for p in box])

def detect(context, image: PIL.Image.Image):
    """推理核心函数：CVAT 会逐帧调用此函数"""
    # 使用本地显卡执行推理
    results = model.predict(source=image, verbose=False)
    return list(_yolo_to_cvat(results))