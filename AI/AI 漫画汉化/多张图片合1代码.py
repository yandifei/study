import os
import re
from PIL import Image

# 获取所有 jpg 文件，按文件名中的数字排序
files = [f for f in os.listdir('.') if f.lower().endswith('.jpg')]
files.sort(key=lambda f: int(re.search(r'(\d+)', f).group(1)))

if not files:
    print("没找到图片！")
    exit()

# 先读取所有图片信息和尺寸
images = []
max_width = 0
total_height = 0
for f in files:
    img = Image.open(f)
    img = img.convert('RGB')          # 统一模式，去掉透明通道干扰
    w, h = img.size
    images.append((f, img, w, h))
    max_width = max(max_width, w)
    total_height += h

print(f"共 {len(images)} 张，最大宽度 {max_width}，总高度 {total_height}")

# 创建长图（背景白色，可改成其他颜色）
long_img = Image.new('RGB', (max_width, total_height), (255, 255, 255))

# 竖向拼接（左对齐，宽度不足的部分自动填充白色）
y_offset = 0
for fname, img, w, h in images:
    long_img.paste(img, (0, y_offset))
    y_offset += h
    img.close()

# 保存为无损 PNG，如果想用 JPG 可改为 long_img.save('output.jpg', quality=100)
long_img.save('long_image.png', optimize=True)
print("拼接完成，已保存为 long_image.png")