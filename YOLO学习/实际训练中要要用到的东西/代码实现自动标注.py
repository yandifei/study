# python detect.py --weights path/to/best.pt --source ./抽帧出来的地方 --save-txt --conf-thres 0.25 --project ./output --name auto_labels --exist-ok


import os
from pathlib import Path
from ultralytics import YOLO

"""需要改的地方"""
# 加载训练好的模型
model = YOLO("yolo26n.pt")  # 替换为您的模型路径
# 图片文件夹路径
img_folder = "output"
# 输出标签文件夹（与图片同名的 txt 文件）
label_folder = "自动标注的标签"
os.makedirs(label_folder, exist_ok=True)



# 获取所有图片文件
img_paths = list(Path(img_folder).glob("*.jpg")) + list(Path(img_folder).glob("*.png"))

# 遍历图片并推理
for img_path in img_paths:
    # 推理，可设置置信度阈值
    results = model(img_path)  # 返回 Results 对象列表

    # 获取检测结果（假设每张图只有一个结果）
    result = results[0]

    # 生成对应的 txt 标签文件名
    txt_name = img_path.stem + ".txt"
    txt_path = os.path.join(label_folder, txt_name)

    # 将检测结果写入 txt 文件（YOLO 格式：class_id x_center y_center width height）
    # 注意：坐标已归一化（0~1）
    with open(txt_path, "w") as f:
        if result.boxes is not None and len(result.boxes) > 0:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                # xywhn 是归一化的中心坐标和宽高
                xywhn = box.xywhn[0].tolist()
                line = f"{cls_id} {xywhn[0]:.6f} {xywhn[1]:.6f} {xywhn[2]:.6f} {xywhn[3]:.6f}\n"
                f.write(line)
        # 如果没有任何检测，可以保存空文件（可选），或者跳过不创建
        # 此处选择保存空文件（便于后续处理）
        # 如果不想生成空文件，可以用 else: pass，但要注意可能缺少文件

    print(f"已处理: {img_path.name} -> {txt_path}")

print("自动标注完成！")