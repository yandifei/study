"""官方代码
segments, _ = model.transcribe("../voice/output.wav", word_timestamps=True)
for segment in segments:
    for word in segment.words:
        print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
"""

from faster_whisper import WhisperModel

# 加载模型，选择模型大小、设备和计算类型
# large-v3 是目前最新和性能最好的模型
model_size = "large-v3"

# 在 GPU 上使用 FP16 精度运行
model = WhisperModel(model_size, device="cuda", compute_type="float16")

# 或者在 CPU 上使用 INT8 精度运行（推荐用于 CPU）
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

# 除了提供分段转录结果，你还可以轻松获取每个单词的精确开始和结束时间戳，这对于字幕制作或需要精细时间对齐的应用非常关键
segments, info = model.transcribe("../voice/output.wav", word_timestamps=True)
for segment in segments:
    for word in segment.words:
        print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))


# 打印检测到的语言和概率
print(f"检测到{info.language}语言的概率为{info.language_probability}")