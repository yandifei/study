"""高速截图
库名	特点与性能	安装方法	主要优势
RapidShot	支持 240Hz+，可集成 NVIDIA GPU (CuPy) 加速，有详细的性能对比 。	pip install rapidshot[all]	性能最强，功能全面（含光标捕获），适合追求极致速度的用户。
DXcam / DXcamPIL	原版DXcam实测可达 238 FPS，社区版DXcamPIL简化依赖，专注于PIL输出 。	pip install dxcam[cv2] 或 dxcampil	成熟稳定，社区活跃，文档和示例丰富。
BetterCam	同样是DXcam衍生版，强调240Hz+捕获能力和易用性 。	pip install bettercam	API设计简洁，上手非常快。
"""

import dxcam

# 创建主显示器的摄像头实例
camera = dxcam.create()

# 抓取全屏截图
frame = camera.grab()

# 如果要显示图片，可以用PIL
if frame is not None:
    from PIL import Image
    Image.fromarray(frame).show()