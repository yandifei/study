"""【【中字】如何使用VAD模型Silero来做语音识别】
https://www.bilibili.com/video/BV1PyJqz2EUz?vd_source=298465310cd98e6ceddf1afe7d72e7ec
"""
import io

import torch
from pydub import AudioSegment
import speech_recognition as sr # 语音识别模块（语音识别库）


"""基础配置"""
# 用cpu运行，因为cpu更加完善
device = torch.device("cpu")
# 模型、解码器、工具集（这些对象由加载模型函数返回）
model, decoder, utils = torch.hub.load(repo_or_dir="snakers4/silero_models",
                                       model="silero_stt", # VAD的模型
                                       languages="zh",  # 语言是中文
                                       device=device,)    # 使用的设备

"""自动语音检测"""
r = sr.Recognizer()
# 设置麦克风的采样率为16000
with sr.Microphone(sample_rate=16000) as mic:
    # 环境噪音自动校准
    r.adjust_for_ambient_noise(mic)
    print("请说话......")
    while True:
        audio = r.listen(mic)
        audio = io.BytesIO(audio.get_wav_data())
        audio = AudioSegment.from_file(audio)
        x = torch.FloatTensor(audio.get_array_of_samples()).view(1, -1)# 重塑波形的基本形状
        x = x.to(device)
        z = model(x)
        print(f"我的提问：{decoder(z[0])}")

        # 无需特换成bytes.u对象，直接使用audio三io