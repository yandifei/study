"""

"""
import pyaudio

p = pyaudio.PyAudio()

# 获取默认输入设备信息（麦克风）
try:
    default_input = p.get_default_input_device_info()
    print(f"默认输入设备 (麦克风) - 索引: {default_input['index']}, 名称: {default_input['name']}")
except IOError:
    print("系统没有找到输入设备。")

# 获取默认输出设备信息（扬声器/耳机）
try:
    default_output = p.get_default_output_device_info()
    print(f"默认输出设备 (扬声器/耳机) - 索引: {default_output['index']}, 名称: {default_output['name']}")
except IOError:
    print("系统没有找到输出设备。")

p.terminate()


def refresh_devices():
    """刷新设备列表，返回所有设备的信息列表"""
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        devices.append(p.get_device_info_by_index(i))
    p.terminate()
    return devices

refresh_devices()