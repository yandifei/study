"""fastest-whisper
fastest-whisper是使用CTranslate2对 OpenAI 的 Whisper 模型的重新实现，CTranslate2 是 Transformer 模型的快速推理引擎。
在相同准确率下，此实现比openai/whisper快 4 倍，同时占用更少的内存。通过在 CPU 和 GPU 上均采用 8 位量化，可以进一步提高效率。
https://github.com/SYSTRAN/faster-whisper

这个库集成了语音活动检测Silero VAD，可以过滤掉音频中不包含语音的部分，从而提高转录效率和准确性。
"""
from faster_whisper import WhisperModel

# 加载模型，选择模型大小、设备和计算类型
# large-v3 是目前最新和性能最好的模型
model_size = "large-v3"

# 在 GPU 上使用 FP16 精度运行
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# 或者在 CPU 上使用 INT8 精度运行（推荐用于 CPU）
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

# 转录音频文件
segments, info = model.transcribe("../voice/output.wav", beam_size=5)

# 打印检测到的语言和概率
print(f"检测到{info.language}语言的概率为{info.language_probability}")

# 遍历并打印转录结果
for segment in segments:
    print(f"[{segment.start:.2f} -> {segment.end:.2f}] {segment.text}")