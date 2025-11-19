"""Faster Distil-Whisper
Distil-Whisper 检查点与 Faster-Whisper 软件包兼容。
特别是，最新的distil-large-v3 检查点本质上设计用于与 Faster-Whisper 转录算法配合使用。
以下代码片段演示了如何使用 distil-large-v3 对指定的音频文件进行推理：
"""
from faster_whisper import WhisperModel

model_size = "distil-large-v3"

model = WhisperModel(model_size, device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.mp3", beam_size=5, language="en", condition_on_previous_text=False)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))


"""字级时间戳"""
segments, _ = model.transcribe("audio.mp3", word_timestamps=True)

for segment in segments:
    for word in segment.words:
        print("[%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))

"""VAD 滤波器
该库集成了Silero VAD模型来滤除音频中不包含语音的部分：
"""
segments, _ = model.transcribe("audio.mp3", vad_filter=True)
"""
默认行为较为保守，仅移除超过 2 秒的静音。请参阅源代码中可用的 VAD 参数和默认值。
您可以使用字典参数自定义它们vad_parameters：
Vad 过滤器默认启用，用于批量转录。
"""
segments, _ = model.transcribe(
    "audio.mp3",
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500),
)

"""
日志记录
库日志记录级别可以这样配置：
"""
import logging

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)