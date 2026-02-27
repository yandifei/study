import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QBrush

class DetectionOverlay(QWidget):
    """透明穿透窗口，用于绘制检测目标框"""
    def __init__(self):
        super().__init__()

        # 设置窗口标志：无边框、置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置鼠标穿透（点击操作会传递到下层窗口）
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # 获取屏幕尺寸并设置为全屏
        screen_geo = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geo)

        # 存储检测结果，每个元素为 (类别名, 置信度, x1, y1, x2, y2)
        self.detections = []

        # 可选：定时器模拟实时更新检测结果
        self.timer = QTimer()
        self.timer.timeout.connect(self.mock_update)
        self.timer.start(2000)  # 每2秒更新一次（仅演示）

    def mock_update(self):
        """模拟外部传入的检测数据（实际应从共享内存/队列等获取）"""
        # 构造几个示例检测框（坐标基于当前窗口大小）
        w, h = self.width(), self.height()
        self.detections = [
            ("person", 0.92, int(w*0.2), int(h*0.3), int(w*0.3), int(h*0.7)),
            ("car",    0.85, int(w*0.5), int(h*0.4), int(w*0.7), int(h*0.6)),
            ("dog",    0.78, int(w*0.6), int(h*0.2), int(w*0.8), int(h*0.4)),
        ]
        self.update()  # 触发重绘

    def update_detections(self, new_detections):
        """外部调用此方法更新检测结果"""
        self.detections = new_detections
        self.update()

    def paintEvent(self, event):
        """绘制事件：在透明窗口上画框和文字"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        # 可选：绘制一个极淡的半透明底色，便于观察窗口位置（实际可以省略）
        # painter.fillRect(self.rect(), QColor(0, 0, 0, 20))  # 黑色透明 20/255

        # 设置画笔：黄色边框，4像素宽
        pen = QPen(QColor(255, 255, 0), 4)
        painter.setPen(pen)
        # 设置画刷：不填充
        painter.setBrush(Qt.NoBrush)

        # 设置字体（Windows 下使用微软雅黑以显示中文）
        font = QFont("Microsoft YaHei", 16)
        painter.setFont(font)

        # 遍历所有检测结果绘制矩形和标签
        for cls_name, conf, x1, y1, x2, y2 in self.detections:
            # 绘制矩形框
            painter.drawRect(x1, y1, x2 - x1, y2 - y1)

            # 准备标签文本：类别 + 置信度
            label = f"{cls_name} {conf:.2f}"
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
            painter.setBrush(Qt.NoBrush)
            painter.drawText(x1 + 5, y1 - 10, label)

        # 绘制结束
        painter.end()

def main():
    app = QApplication(sys.argv)

    # 创建并显示覆盖窗口
    overlay = DetectionOverlay()
    overlay.show()

    # 如果不需要模拟更新，可以在这里调用 overlay.update_detections(...) 传入真实数据
    # 例如从YOLO线程通过信号槽传递数据（略）

    sys.exit(app.exec())

if __name__ == "__main__":
    main()