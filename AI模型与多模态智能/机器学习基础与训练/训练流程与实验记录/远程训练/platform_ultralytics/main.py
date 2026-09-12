from ultralytics import HUB, YOLO

# 1. 身份验证：连接你的 Ultralytics 账户
# 这相当于 export ULTRALYTICS_API_KEY="..."
HUB.login("密钥")

# 2. 加载模型：这里会从云端拉取 yolo26n 的配置
model = YOLO("yolo26n.pt")

# 3. 开始训练
# 所有的参数（data, epochs, imgsz 等）都作为 train 方法的参数传入
model.train(
    data="ul:",
    epochs=100,
    batch=16,
    imgsz=640,
    project="yandifei/table-ico"
)