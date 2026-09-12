"""
它能通过WMI模块获取设备的硬件ID来识别出纯物理设备
废了
"""
import pyaudio
import win32com.client


def get_physical_microphones():
    """获取系统真实的物理麦克风设备"""
    physical_mics = []

    # 1. 使用WMI查询所有声音设备，获取其硬件ID
    try:
        wmi = win32com.client.GetObject('winmgmts:')
        sound_devices = wmi.InstancesOf('Win32_SoundDevice')
        hardware_ids = {}
        for device in sound_devices:
            # 提取PNPDeviceID作为硬件唯一标识
            if device.PNPDeviceID:
                # 例如: HDAUDIO\FUNC_01&VEN_10EC...
                hardware_ids[device.Name] = device.PNPDeviceID
    except Exception as e:
        print(f"WMI查询失败: {e}")
        return []

    # 2. 遍历PyAudio输入设备，匹配其名称
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if dev_info['maxInputChannels'] > 0:
            dev_name = dev_info['name']
            # 如果名称在WMI设备列表中，则判定为物理设备
            for hw_name in hardware_ids:
                if hw_name in dev_name:
                    physical_mics.append({
                        'index': i,
                        'name': dev_name,
                        'hw_id': hardware_ids[hw_name]
                    })
                    break

    p.terminate()
    return physical_mics


if __name__ == "__main__":
    mics = get_physical_microphones()
    if mics:
        print("✅ 找到以下物理麦克风设备:")
        for mic in mics:
            print(f" - {mic['index']}: {mic['name']}")
            print(f"   硬件ID: {mic['hw_id']}")
    else:
        print("❌ 没有找到任何物理麦克风。")