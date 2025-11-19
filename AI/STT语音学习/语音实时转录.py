import warnings

import numpy
import pyaudio
import wave     # WAV文件操作库

import pyttsx3
import whisper

"""音频对象创建"""
# 创建音频对象
audio = pyaudio.PyAudio()
# 打开音频流
stream = audio.open(format=pyaudio.paInt16, # 16位整数格式
                channels=1,                 # 单声道
                rate=16000,                 # Silero-VAD 推荐的采样率（16kHz）
                input=True,
                frames_per_buffer=1024)     # 每次从麦克风读取的音频帧数为1024
frames = []  # 创建一个空列表来存储音频数据（frames_per_buffer的数据）

"""转义初始化"""
# faster-whisper实现
# # 在 GPU 上使用 FP16 精度运行
# model = WhisperModel("large-v3", device="cuda", compute_type="float16")
# # 或者在 CPU 上使用 INT8 精度运行（推荐用于 CPU）
# # model = WhisperModel(model_size, device="cpu", compute_type="int8")

# whisper实现
# 忽略gpu可以推理却用cpu推理的警告
warnings.filterwarnings("ignore", message="Performing inference on CPU when CUDA is available")
# 忽略CPU无法使用半浮点精度推理的警告
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
# 加载模型("cpu"默认是cpu，"cuda"是GPU)
model = whisper.load_model("turbo", "cuda")

"""TTS语音初始化"""
engine = pyttsx3.init()

"""开始实时转录"""
print("正在监听...请开始说话。按 Ctrl+C 手动停止。")


# 公式：总采样数 / 每次读取量 = 16000/1024 ≈ 15.6次 → 取整16次
# for i in range(0, round(16000 / 1024 * 16)):
for i in range(round(15.625 * 5)):
    data = stream.read(1024)    # 读取一块音频数据
    frames.append(data)         # 把数据添加到列表中

print("录制完成")

# 将字节数据转换为16位整数的NumPy数组(将列表中的字节数据连接起来)
# audio_numpy = numpy.frombuffer(b''.join(frames), dtype=numpy.int16)
# 将音频数据转换为numpy数组
audio_data = numpy.frombuffer(b''.join(frames), dtype=numpy.int16).astype(numpy.float32) / 32768.0

# 进行转录
result = whisper.transcribe(model,audio_data,initial_prompt="我是爱丽丝，你也可以叫我Arisu")
# 输出结果
print(result["text"])

# 录入文字
engine.say(result["text"])
# 播放声音
engine.runAndWait()


# 停止录音
stream.stop_stream()  # 停止音频流（停止录音）
stream.close()        # 关闭音频流（删除流式对象）
audio.terminate()     # 关闭音频系统（删除音频对象）

# 写入文件（标准文件=音频格式、采样率、通道数等信息+音频数据）
with wave.open("./voice/output.wav", 'wb') as wf:  # 'wb' = 写入二进制模式
    wf.setnchannels(1)                                          # 设置声道数
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))     # 设置采样宽度
    wf.setframerate(16000)                                      # 设置采样率
    wf.writeframes(b''.join(frames))                            # 将所有数据块合并并写入文件
    # print(b''.join(frames))
