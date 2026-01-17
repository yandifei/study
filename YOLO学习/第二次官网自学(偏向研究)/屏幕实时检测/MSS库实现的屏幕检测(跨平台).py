import cv2 as cv
import numpy as np
from mss import mss
from ultralytics import YOLO

# 1. 初始化
model = YOLO("v26 600(屏幕微信和qq).pt")
sct = mss()

# 定义截图区域 (Left, Top, Width, Height)
# 如果想全屏，可以使用 sct.monitors[1]
# monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
monitor = sct.monitors[1]

print("正在运行... 按 'q' 键退出")

while True:
    # 2. 高速截图
    # sct.grab 比 pyautogui.screenshot() 快 10 倍以上
    screenshot = sct.grab(monitor)

    # 3. 转换为 OpenCV 格式 (BGRA -> BGR)
    # mss 抓取的是 BGRA 格式，YOLO 需要 BGR
    img = np.array(screenshot)
    frame = cv.cvtColor(img, cv.COLOR_BGRA2BGR)

    # 4. YOLO 跟踪推理
    # stream=True 可以更高效地处理连续帧
    results = model.track(frame, show=False, persist=True, verbose=False)

    # 5. 绘制结果与逻辑处理
    annotated_frame = results[0].plot()  # 获取带有检测框的图像

    # 打印检测到的坐标
    if results[0].boxes.id is not None:
        for box in results[0].boxes.xywh:
            x, y, w, h = box
            # print(f"目标中心: ({int(x)}, {int(y)})")

    # 6. 显示窗口
    cv.imshow("YOLO MSS Realtime", annotated_frame)

    # 7. 退出机制
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()