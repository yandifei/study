"""【【中字】如何使用VAD模型Silero来做语音识别】
https://www.bilibili.com/video/BV1PyJqz2EUz?vd_source=298465310cd98e6ceddf1afe7d72e7ec
因为我不知道什么少了一个基础库audioop、还有pyaudioop这个库也没了

"""
import io
import warnings
import wave

import numpy
import whisper
import speech_recognition as sr # 语音识别模块（语音识别库）


"""基础配置"""
# whisper实现
# 忽略gpu可以推理却用cpu推理的警告
warnings.filterwarnings("ignore", message="Performing inference on CPU when CUDA is available")
# 忽略CPU无法使用半浮点精度推理的警告
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
# 加载模型("cpu"默认是cpu，"cuda"是GPU)
model = whisper.load_model("turbo", "cuda")

"""自动语音检测"""
r = sr.Recognizer()
# 设置麦克风的采样率为16000
with sr.Microphone(sample_rate=16000) as mic:
    # 环境噪音自动校准
    r.adjust_for_ambient_noise(mic)
    print("请说话......")
    while True:
        # 监听麦克风输入
        audio = r.listen(mic)
        # 将音频数据转换为numpy数组
        audio_data = numpy.frombuffer(audio.get_raw_data(), dtype=numpy.int16).astype(numpy.float32) / 32768.0
        # 进行转录
        result = whisper.transcribe(model, audio_data, initial_prompt="我是爱丽丝，你也可以叫我Arisu")
        print(f"我：{result['text']}")