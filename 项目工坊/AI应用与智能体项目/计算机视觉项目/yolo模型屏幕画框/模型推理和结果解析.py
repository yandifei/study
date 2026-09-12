from ultralytics import YOLO

# 加载你的模型
model = YOLO('models/v26 600(屏幕微信和qq).pt')

# 直接将 source 设置为 "screen"
# show=True 会弹出一个窗口显示检测结果
# save=True 会将检测过程保存为视频
# results = model.predict(source="screen", show=True, save=False, stream=True)

# 打印完整的类别映射字典（类别映射表）
name_map = model.names
print(name_map)

results = model.predict(source="img.png")


# # 获取总的检测结果(左上坐标和右下坐标)
# print(results[0].boxes.data.tolist())

# # 解析结果
for data in results[0].boxes.data.tolist():
    x1, y1, x2, y2, conf, cls = data
    # x1, y1, x2, y2 = map(int, data[:4])
    print(f"检测目标: {name_map[int(cls)]:<7} | 阈值: {conf:.2f} | 坐标: ({int(x1)}, {int(y1)}, {int(x2)}, {int(y2)})")
# 报废的
# for data in results[0].boxes.data.tolist():
#     x1, y1, x2, y2, conf, cls = data
#     # 添加解析结果到解析列表中
#     self.parse_list.append((self.model.names[int(cls)], int(conf, 2), int(x1), int(y1), int(x2), int(y2)))



# # 清空上一次结果
# parse_list.clear()
# # 抓取全屏截图
# frame = camera.grab()
# # 截图结果进行推理
# results = model.predict(source="img.png")
# # 解析推理结果
# for data in results[0].boxes.data.tolist():
#     x1, y1, x2, y2, conf, cls = data
#     # 添加解析结果到解析列表中
#     parse_list.append([name_map[int(cls)], int(conf,2), int(x1), int(y1), int(x2), int(y2)])
# # 更新绘制数据
# draw_window.detections = parse_list