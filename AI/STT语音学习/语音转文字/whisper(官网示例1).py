"""conda install ffmpeg -C conda-forge
所有模型：tiny、base、small、medium、large、turbo
"""
import warnings
import whisper

# 忽略警告
# 忽略gpu可以推理却用cpu推理的警告
warnings.filterwarnings("ignore", message="Performing inference on CPU when CUDA is available")
# 忽略CPU无法使用半浮点精度推理的警告
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# 加载模型("cpu"默认是cpu，"cuda"是GPU)
model = whisper.load_model("turbo", "cpu")
result = whisper.transcribe(
    model=model,                    # 加载模型
    audio=r"../voice/output.wav",    # 转录的音频（音频文件路径或音频波形数据（NumPy 数组或 PyTorch 张量））
    # verbose=None,                   # 控制台显示的信息(默认None不显示，True显示详细信息，False显示必要信息)
    # temperature=0.0,                # 采样时的随机性（默认0.0选择概率最高的词，1.0会随机）
    # compression_ratio_threshold=2.4,# 默认 2.4当转录文本的 gzip 压缩比过高时，表示文本可能存在大量重复或不通顺，即被认为是失败的。
    # logprob_threshold=-1.0,         # 当转录文本的平均对数概率低于此值时，表示模型对预测结果不自信，即被认为是失败的。
    # no_speech_threshold=0.6,        # 当模型识别为“没有语音”的概率高于此值，且平均对数概率低于 logprob_threshold 时该段会被认为是静音
    # condition_on_previous_text=True,#将前一个窗口的转录文本作为下一个窗口的提示（False可能会导致文本不连贯，但可以避免模型陷入重复循环或时间戳混乱的问题。如果你发现模型在重复某个词或短语，可以尝试将其设置为 False）
    # initial_prompt="我是爱丽丝，你也可以叫我Arisu",     # 第一次转录提供上下文或提示，帮助模型更好地识别相关词汇。
    # word_timestamps=False,          # 提取并返回词级别的精确时间戳，默认False只返回分段的时间戳，true返回每个词的开始和结束时间戳
    # prepend_punctuations= "\"'“¿([{-",                  # 将指定的标点（如引号、括号）与后面的词合并。
    # append_punctuations= "\"'.。,，!！?？:：”)]}、",     # 将指定的标点（如引号、括号）与后面的词合并。
    # clip_timestamps = "0",          # 用于指定只处理音频的特定片段[0, 30, 60, 90]，表示转录从 0 到 30 秒和 60 到 90 秒的片
)

print(result["text"])

