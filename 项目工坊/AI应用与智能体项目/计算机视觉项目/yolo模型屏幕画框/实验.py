import dxcam
import torch
from ultralytics import YOLO

# 加载模型
model = YOLO('models/v26 600(屏幕微信和qq).pt').to('cuda')

# 初始化DXCAM，指定设备为显卡，让 dxcam 直接输出在 GPU 显存上的数据，确保截图格式直接符合 YOLO 的输入要求
camera = dxcam.create(device_idx=0, output_idx=0, output_color="RGB")
# 开启一个后台专用线程，利用 DXGI 的“桌面复制 API”，持续把屏幕画面推送到一个 GPU 显存缓冲区
camera.start(target_fps=240, video_mode=True)

try:
    while True:
        # 直接获取显存中的帧 (需配合特定 backend)
        frame = camera.get_latest_frame()

        # 使用 GPU（设备 0）对屏幕帧进行半精度（FP16）流式推理，并关闭详细日志输出
        results = model.predict(frame, True, device=0, half=True, verbose=False)
finally:
    if camera:
        camera.stop()


