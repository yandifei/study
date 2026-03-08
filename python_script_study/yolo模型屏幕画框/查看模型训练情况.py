from ultralytics import YOLO

model = YOLO(r'/models/yysls_x(23).pt')  # 例如 best.pt

# 查看模型内部保存的元数据
if hasattr(model, 'ckpt'):
    ckpt = model.ckpt  # 训练过程中保存的检查点
    if 'epoch' in ckpt:
        print(f"模型保存时的 epoch: {ckpt['epoch']}")
    else:
        print("元数据中没有 epoch 信息")
else:
    print("该模型没有 ckpt 属性，可能是纯权重文件")