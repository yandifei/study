import numpy
import pyaudio
import pyttsx3
import torch
import whisper

# 初始化 Whisper 模型
print("正在加载 Whisper 模型...")
# 检查推理设备是GPU还是CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"推理正在使用设备：{device}")
model = whisper.load_model(
    name="models_files/large-v3-turbo.pt",
    device="cpu",
    download_root=None, # 禁止下载路径
    in_memory=True # 直接把模型权重全部读进内存
)

# 音频流对象初始化
audio = pyaudio.PyAudio()
# 音频录制的时间
record_time: int = 5

# 初始化 pyttsx3 (TTS)
engine = pyttsx3.init()
# 我来控制循环防止windows的bug
engine.startLoop(False)

def speak(text: str):
    """语音输出"""
    # 检测输入是否有效
    if text == "":
        return False

    # 调用 pyttsx3
    engine.say(text)
    while engine.isBusy():
        engine.iterate()
    return True

# def find_working_microphone():
#     """检测麦克风"""
#     device_count = audio.get_device_count()
#     for i in range(device_count):
#         device_info = audio.get_device_info_by_index(i)
#         if device_info['maxInputChannels'] > 0:
#             return i, device_info['name']
#     return None, None
#
#
# device_index, device_name = find_working_microphone()
# if device_index is None:
#     print("未找到麦克风")
#     exit()

stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    input_device_index=0,
                    frames_per_buffer=1024)

try:
    while True:
        frames = []
        print("[状态] 正在录音 (5秒)... 请说话")

        # 录制约5秒的音频
        for i in range(0, int(16000 / 1024 * record_time)):
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

        print("[状态] 正在识别...")
        audio_data = numpy.frombuffer(b''.join(frames), dtype=numpy.int16).astype(numpy.float32) / 32768.0

        # Whisper 识别
        result = model.transcribe(audio_data, initial_prompt="我是爱丽丝，你也可以叫我Arisu或アリス")
        if result['text'] != "":
            print(f"我：{result['text']}")
            speak(result["text"])
        else:
            print("未检测到有效语音")

except KeyboardInterrupt:
    print("\n程序手动停止")

# 清理
stream.stop_stream()
stream.close()
audio.terminate()