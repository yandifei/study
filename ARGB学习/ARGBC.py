"""RGBC = RGB_controller = RGB控制器
用来控制主机上风扇的灯光
"""
# 自带的包
import subprocess
import time
# 第三方包
from openrgb import OpenRGBClient

# 启动OpenRGB的客户端

OpenRGB_path = "./OpenRGB Windows 64-bit/OpenRGB.exe"  # OpenRGB的相对路径

# # 安装服务
# result = subprocess.run(
#     # 命令列表（避免注入风险）
#     [".\OpenRGB Windows 64-bit\OpenRGB.exe", "--install-service"],
#     capture_output=True,   # 捕获输出
#     text=True,             # 返回字符串（Python 3.5+）
#     check=True             # 检查错误（非零退出码抛异常）
# )
# print(result.stdout)

# 启动服务
# result = subprocess.run(
#     # 命令列表（避免注入风险）
#     [".\OpenRGB Windows 64-bit\OpenRGB.exe", "--start-service"],
#     capture_output=True,   # 捕获输出
#     text=True,             # 返回字符串（Python 3.5+）
#     check=True             # 检查错误（非零退出码抛异常）
# )
# print(result.stdout)

# 执行命令启动服务并获取输出(非流式)
result = subprocess.run(
    # 命令列表（避免注入风险）
    [OpenRGB_path, "--server","--server-port", "6742", "--profile", "default"],
    # capture_output=True,   # 捕获输出
    # text=True,             # 返回字符串（Python 3.5+）
    # check=True             # 检查错误（非零退出码抛异常）
)
print("OpenRGB 服务器已启动")
print(result.stdout)
time.sleep(2)  # 等待服务器初始化








# 安装为系统服务：
# "B:\study\ARGB学习\OpenRGB Windows 64-bit\OpenRGB.exe" --install-service

# 启动服务：
# "B:\study\ARGB学习\OpenRGB Windows 64-bit\OpenRGB.exe" --start-service

# 设置开机自启：
# sc config OpenRGBService start=auto

# 验证服务状态：
# sc query OpenRGBService

# "B:\study\ARGB学习\OpenRGB Windows 64-bit\OpenRGB.exe" --server --server-port 6742 --profile default


# 实例化对象
cli = OpenRGBClient()
cli.clear() # 关闭所有内容

# # # 找到设备
# from openrgb.utils import DeviceType
# motherboard = cli.get_devices_by_type(DeviceType.MOTHERBOARD)[0]
# print(len(cli.get_devices_by_type(DeviceType.MOTHERBOARD)))
#
# # 配置颜色（颜色由 RGBColor 对象处理。它可以从 RGB、HSV 甚至十六进制颜色值。）
# from openrgb.utils import RGBColor
# red = RGBColor(255, 0, 0)
# blue = RGBColor.fromHSV(240, 100, 100)
# green = RGBColor.fromHEX('#00ff00') # #符号不是必需的，它通常附加到十六进制颜色
# motherboard.set_color(RGBColor(0, 255, 0))
# motherboard.set_colors([red, blue]*3)










# 颜色由 RGBColor 对象处理。它可以从 RGB、HSV 甚至十六进制颜色值。
from openrgb.utils import RGBColor

# from openrgb import OpenRGBClient
# from openrgb.utils import RGBColor, DeviceType
#
# client = OpenRGBClient()
# client.clear() # 关闭所有内容
# motherboard = client.get_devices_by_type(DeviceType.MOTHERBOARD)[0]
# motherboard.set_color(RGBColor(0, 255, 0))
# motherboard.zones[0].set_color(RGBColor(255, 0, 0))
# motherboard.zones[1].leds[0].set_color(RGBColor.fromHSV(0, 100, 100))
# motherboard.set_mode("breathing")
# client.save_profile("profile1")