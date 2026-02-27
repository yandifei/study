# 内置库
import sys
from pathlib import Path
# 三方库
import dxcam
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QBrush, QShortcut, QKeySequence
from ultralytics import YOLO

class YOLOThread(QThread):
    # 定义一个信号，用于传输检测结果列表
    result_ready = Signal(list)

    def __init__(self, model_path):
        super().__init__()
        self.model = YOLO(model_path)
        # 创建主显示器的摄像头实例
        self.camera = dxcam.create()
        # 创建线程运行标志位
        self.running = True

    def run(self):
        """线程执行主体"""
        """截图、推理结果、解析结果、更新绘制数据、屏幕重新绘制"""
        # 循环获取屏幕截图并推理
        while self.running:
            # 不休眠子线程把 CPU 核心占得死死的，CPU 太忙而变得不
            self.msleep(100)
            # 获取截图
            frame = self.camera.grab()
            if frame is not None:
                # 解析列表（不用self.parse_list是因为解析的绘制的时候又要创新创建，本质是线程的问题）
                parse_list = []

                # 推理图像 (直接传入numpy数组frame)verbose停止输出没有的信息
                results = self.model.predict(source=frame,verbose=False)

                # 解析推理结果(访问raw tensor数据提升速度)
                for det in results[0].boxes.data.cpu().numpy():
                    x1, y1, x2, y2, conf, cls = det
                    # 添加解析结果到解析列表中
                    parse_list.append([self.model.names[int(cls)], f"{conf:.2f}", int(x1), int(y1), int(x2), int(y2)])

                # 发射信号，通知 UI 线程更新
                self.result_ready.emit(parse_list)

class DrawWindow(QWidget):
    """透明穿透窗口，用于绘制检测目标框"""
    def __init__(self, model_path: str|Path):
        super().__init__()

        # 设置窗口标志：无边框、置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 获取缩放比例
        self.scale = QApplication.primaryScreen().devicePixelRatio()
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置鼠标穿透（点击操作会传递到下层窗口）
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # 允许接收焦点（不然热键无效）
        self.setFocusPolicy(Qt.StrongFocus)

        # 热键创建和绑定
        self.shortcut = QShortcut(QKeySequence("Ctrl+F4"), self)
        self.shortcut.activated.connect(QApplication.quit)  # 退出

        # 获取屏幕尺寸并设置为全屏
        self.setGeometry(QApplication.primaryScreen().geometry())

        # 存储检测结果，每个元素为 (类别名, 置信度, x1, y1, x2, y2)
        self.detections = []

        """yolo线程启动"""
        # 启动子线程
        self.yolo_thread = YOLOThread(model_path)
        # 连接信号：线程有了结果 -> 调用自己的 update_detections
        self.yolo_thread.result_ready.connect(self.update_detections)
        self.yolo_thread.start()

    def update_detections(self, new_detections):
        """外部调用此方法更新检测结果并刷新界面"""
        # 如果传递的是self的列表必须是深度拷贝，不然还没解析完就把结果干掉了
        self.detections = new_detections
        if self.detections: print(self.detections)
        # 刷新界面重新绘制
        self.update()

    def paintEvent(self, event):
        """绘制事件：在透明窗口上画框和文字"""
        # 绘制实例
        painter = QPainter(self)
        # self.painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        # 可选：绘制一个极淡的半透明底色，便于观察窗口位置（实际可以省略）
        # painter.fillRect(self.rect(), QColor(0, 0, 0, 20))  # 黑色透明 20/255

        # 设置画笔：蓝色边框，2素宽
        painter.setPen(QPen(QColor(0, 0, 255), 2))
        painter.setBrush(Qt.NoBrush) # 设置画刷：不填充
        # 设置字体（Windows 下使用微软雅黑以显示中文）
        painter.setFont(QFont("Microsoft YaHei", 16))

        # 遍历所有检测结果绘制矩形和标签
        for cls, conf, x1, y1, x2, y2 in self.detections:
            # 缩放还原
            x1, y1, x2, y2 = x1/self.scale, y1/self.scale, x2/self.scale, y2/self.scale
            # 绘制矩形框
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)

            # 准备标签文本：类别 + 置信度
            label = f"{cls} {conf}"
            # 获取文本尺寸以绘制背景
            metrics = painter.fontMetrics()
            text_w = metrics.horizontalAdvance(label)
            text_h = metrics.height()

            # 在矩形上方绘制半透明背景（便于阅读）
            painter.setBrush(QColor(0, 0, 0, 150))  # 黑色半透明
            painter.setPen(Qt.NoPen)
            painter.drawRect(x1, y1 - text_h - 5, text_w + 10, text_h + 5)

            # 绘制白色文字
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(x1 + 5, y1 - 10, label)



"""真正干活的地方"""
# 创建QApplication实例
app = QApplication(sys.argv)
# 创建窗口
draw_window = DrawWindow('models/v26 600(屏幕微信和qq).pt')
# 时间监听循环显示
draw_window.show()
# 例如从YOLO线程通过信号槽传递数据（略）
sys.exit(app.exec())