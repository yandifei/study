import dxcam
import torch
from ultralytics import YOLO

# 加载模型
model = YOLO('models/v26 600(屏幕微信和qq).pt')

# 初始化DXCAM，指定设备为显卡，让 dxcam 直接输出在 GPU 显存上的数据，确保截图格式直接符合 YOLO 的输入要求
camera = dxcam.create(device_idx=0, output_idx=0, output_color="RGB")
# 开启一个后台专用线程，利用 DXGI 的“桌面复制 API”，持续把屏幕画面推送到一个 GPU 显存缓冲区
camera.start(target_fps=240, video_mode=True)

try:
    while True:
        # 直接获取显存中的帧 (需配合特定 backend)
        frame = camera.get_latest_frame()

        # 异步预测 (0 拷贝关键：数据已经在 GPU 上，开启异步流式推理)
        results = model.predict(source=frame, device=0, stream=True)
finally:
    if camera:
        camera.stop()


# 逻辑伪代码：独立的高速渲染线程
def render_thread():
    # 1. 创建 DX11 透明 Overlay
    overlay = create_dx11_overlay()

    while True:
        # 2. 从多线程队列中读取最新的 YOLO 预测坐标
        boxes = coordinate_queue.get()

        # 3. 开启 DX11 场景
        overlay.begin_scene()
        for box in boxes:
            # 预测平滑处理：根据当前时间戳补偿位置差
            smoothed_box = predict_position(box)
            # 调用底层指令直接画框
            overlay.draw_rect(smoothed_box)
        overlay.end_scene()

        # 4. 关键：不使用 VSync，通过精确的微秒级休眠控制频率
        high_precision_sleep(1 / 200)