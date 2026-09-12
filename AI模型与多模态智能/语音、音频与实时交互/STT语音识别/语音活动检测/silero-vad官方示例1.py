"""语音活动检测器
检测语音文件出现人声的时间和人声结束的时间
load_silero_vad: 加载预训练的 Silero VAD 模型。
read_audio: 一个读取音频文件的辅助函数，它会处理文件并为模型做好数据准备。
get_speech_timestamps: 这是核心函数，它将音频数据和 VAD 模型作为输入，来识别并返回语音片段的时间戳。
"""
from silero_vad import load_silero_vad, read_audio, get_speech_timestamps

# 加载 VAD 模型
model = load_silero_vad()
# 从指定的路径读取一个音频文件
wav = read_audio("../voice/output.wav")
# 用 VAD 模型来分析音频
speech_timestamps = get_speech_timestamps(
  wav,      # 你读取的音频数据。
  model,    # 用于分析音频的 VAD 模型。
  return_seconds=True,  # 返回语音时间戳（以秒为单位）（默认为示例）
)
print(speech_timestamps)