"""语音活动检测
监听你的声音，当检测到你开始说话时，开始录音。
持续录音，直到 Silero-VAD 检测到一段持续的静默，就自动结束录音，并将音频数据保存为 .wav 文件。
需要安装pyaudio这个库
"""
import torch
import pyaudio
from silero_vad import VADIterator      # 一个VAD迭代器，用于实时流式处理

SILENCE_THRESHOLD = 30  # 静默帧数阈值，当连续检测到这么多静默帧时，停止录音


# ==============================================================================
# 开启录音工具
# ==============================================================================
# 1创建 PyAudio 实例
audio = pyaudio.PyAudio()
# 2. 打开音频流
stream = audio.open(format=pyaudio.paInt16, # 16位整数格式
                channels=1,                 # 单声道
                rate=16000,                 # Silero-VAD 推荐的采样率（16kHz）
                input=True,
                frames_per_buffer=1024)     # 每次从麦克风读取的音频帧数为1024
print("正在监听...请开始说话。按 Ctrl+C 手动停止。")
# ==============================================================================
# 加载Silero-VAD模型和工具
# ==============================================================================
# 从本地加载模型，或者如果本地没有，则从torch.hub下载
model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False
)
(get_speech_timestamps, _, read_audio, _, _) = utils

# 创建一个VAD迭代器，用于实时流式处理
vad_iterator = VADIterator(model)
# ==============================================================================
# 主循环：实时监听和录音逻辑
# ==============================================================================
frames = []  # 用于存储录音数据的列表
is_recording = False  # 录音状态标志
silent_frames = 0  # 连续静默帧计数器

try:
    while True:
        # 从音频流中读取一小块数据
        audio_chunk = stream.read(1024, exception_on_overflow=False)

        # 将读取的音频数据传递给VAD迭代器进行处理
        speech_dict = vad_iterator(audio_chunk, return_seconds=True)

        # 如果VAD迭代器返回一个非空字典，说明检测到了语音
        if speech_dict:
            # 如果目前没有在录音，则开始录音
            if not is_recording:
                print("检测到人声，开始录音...")
                is_recording = True
            # 重置静默帧计数器
            silent_frames = 0
        else:
            # 如果目前正在录音，且没有检测到语音，则增加静默帧计数器
            if is_recording:
                silent_frames += 1
                # 如果静默帧数达到阈值，则认为语音已停止，结束录音
                if silent_frames > SILENCE_THRESHOLD:
                    print("检测到持续静默，录音结束。")
                    break

        # 如果正在录音，将当前音频块添加到帧列表中
        if is_recording:
            frames.append(audio_chunk)

except KeyboardInterrupt:
    # 允许用户使用 Ctrl+C 手动停止程序
    print("\n手动停止录音。")

# ==============================================================================
# 录音结束后的处理
# ==============================================================================
print("录音完成，正在保存文件。")

# 停止和关闭音频流
stream.stop_stream()
stream.close()
audio.terminate()

# 将收集到的音频数据保存为.wav文件
if frames:
    output_filename = "recorded_voice.wav"
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"音频已保存为 {output_filename}")
else:
    print("没有录到任何音频。")