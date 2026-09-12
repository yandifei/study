# 导入 whisper 库，这样我们才能使用它的功能
import whisper

# 加载一个预先训练好的 Whisper 模型。
# 注意：'turbo' 不是标准的开源模型名称，这里我将其换成 'base' 模型举例。
# 'base' 模型在速度和准确度上取得了很好的平衡，非常适合入门。
model = whisper.load_model("base")

# --- 音频预处理 ---

# 从硬盘加载名为 "audio.mp3" 的音频文件。
# Whisper 会自动将音频转换为模型所需的格式（16kHz采样率的浮点数数组）。
audio = whisper.load_audio("audio.mp3")

# Whisper 模型按 30 秒的片段处理音频。
# 这行代码会把音频填充（如果不足30秒）或裁剪（如果超过30秒）到正好30秒。
audio = whisper.pad_or_trim(audio)

# 将原始的音频波形数据，转换成一种叫做“对数梅尔频谱图”的格式。
# 你可以把它想象成是声音的“图像”或“指纹”，这是神经网络真正用来分析和识别的输入数据。
# .to(model.device) 会把这个频谱图数据移动到模型所在的计算设备上（CPU或GPU），以保证计算能够顺利进行。
mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

# --- 识别与输出 ---

# 调用模型的语言检测功能，分析刚刚生成的频谱图。
# 它会返回一个概率字典 `probs`，包含了它认为音频中可能是什么语言以及对应的置信度。
_, probs = model.detect_language(mel)

# 从概率字典 `probs` 中找到概率最高的那个语言，并把它打印出来。
# 例如，它可能会打印出 "Detected language: zh" (zh 代表中文)。
print(f"Detected language: {max(probs, key=probs.get)}")

# 创建一个解码配置对象。这里使用默认配置，不做任何特殊设置。
options = whisper.DecodingOptions()

# 这是最关键的一步：进行解码（也就是语音识别）。
# 函数将模型、频谱图和配置选项作为输入，运行神经网络，最终输出识别结果。
result = whisper.decode(model, mel, options)

# `result` 是一个包含很多信息的对象，我们只取其中的 `.text` 属性，也就是识别出的文字内容。
# 最后，将识别出来的文字打印到屏幕上。
print(result.text)