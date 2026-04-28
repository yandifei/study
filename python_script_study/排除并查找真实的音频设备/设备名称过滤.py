import pyaudio

pyaudio = pyaudio.PyAudio()
print("可用的麦克风设备：")
# 遍历所有设备
for device_index in range(pyaudio.get_device_count()):
    # 根据下标获得设备信息
    dev_info = pyaudio.get_device_info_by_index(device_index)
    # 筛选输入设备 & 按名称过滤
    if dev_info['maxInputChannels'] > 0 and ("麦克风" in dev_info['name'] or "Microphone" in dev_info['name']):
        print(f"{device_index}: {dev_info['name']}")