# yolo detect train data=yysls.yaml model=yolo26n.pt epochs=100 imgsz=1024 batch=16 device=0

from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")  # load a pretrained model (recommended for training)

# Train the model
model.train(data="yysls.yaml", epochs=100, imgsz=1024, batch=16, device=0)

"""训练指令
yolo detect train data=yysls.yaml model=yolo26n.pt epochs=100 imgsz=1024 batch=16 device=0


yolo detect train \
  data=yysls.yaml \
  model=yolo26n .pt \           # 使用更小的官方模型
  epochs=50 \                  # 轮次
  imgsz=640 \                  # 图像尺寸
  batch=32 \                   # 增大 batch
  device=0 \
  workers=16 \                 # 增加加载进程
  cache=True \                 # 缓存图片到内存
  amp=True \                   # 混合精度（默认已开）
  mosaic=0.0 \                 # 关闭马赛克增强（可选）
  save_period=-1 \             # 只保存最终权重
  plots=False \                # 不保存图表
  verbose=False                # 减少日志输出

yolo detect train data=yysls.yaml model=yolo26n.pt epochs=50 imgsz=1024 batch=32 cache='disk' amp=True save_period=-1 plots=False
yolo detect train data=yysls.yaml model=yolo26n.pt epochs=50 imgsz=1024 batch=32 cache=True amp=True save_period=-1 plots=True


yolo detect train data=yysls.yaml model=yolo26n.pt epochs=200 imgsz=640 batch=16 save_period=-1 plots=True
"""

"""推理
yolo predict model=runs/detect/train/weights/best.pt source="视频验证集/1.mp4" save=True device=0
yolo predict model=runs/detect/train2/weights/best.pt source="视频验证集/2.mp4" save=True device=0
"""