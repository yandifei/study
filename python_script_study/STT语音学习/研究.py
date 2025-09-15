import numpy
import pyaudio
import whisper
import torch
from silero_vad import load_silero_vad, read_audio

# 初始化Whisper模型
model = whisper.load_model("base")

# 初始化Silero VAD模型
vad_model = load_silero_vad()

# 设置音频参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisper和VAD通常使用16kHz
CHUNK = 512  # VAD的标准块大小(32ms @ 16kHz)

# 创建PyAudio对象
p = pyaudio.PyAudio()

# 打开音频流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# VAD参数
VAD_THRESHOLD = 0.8  # VAD检测阈值
SILENCE_DURATION = 1.5  # 静音持续时间(秒)，用于确定录音结束
PRE_SPEECH_BUFFER = 0.5  # 语音开始前的缓冲时间(秒)

print("正在监听...请开始说话。按 Ctrl+C 手动停止。")

try:
    frames = []  # 创建一个空列表来存储音频数据
    is_recording = False  # 录音状态标志
    silence_counter = 0  # 静音计数器
    pre_speech_frames = []  # 语音开始前的缓冲帧

    while True:
        # 读取音频数据
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_frame = numpy.frombuffer(data, dtype=numpy.int16)

        # 转换为浮点数并归一化(-1到1范围)
        audio_float = audio_frame.astype(numpy.float32) / 32768.0

        # 使用VAD检测语音
        with torch.no_grad():
            speech_prob = vad_model(torch.from_numpy(audio_float), RATE).item()

        # 检测到语音且当前不在录音状态
        if speech_prob > VAD_THRESHOLD and not is_recording:
            print("检测到语音，开始录音...")
            is_recording = True
            silence_counter = 0

            # 添加预缓冲帧（如果有）
            if pre_speech_frames:
                frames.extend(pre_speech_frames)
                pre_speech_frames = []

            # 添加当前帧
            frames.append(data)

        # 正在录音中
        elif is_recording:
            # 添加当前帧
            frames.append(data)

            # 检测静音
            if speech_prob <= VAD_THRESHOLD:
                silence_counter += 1
                silence_time = silence_counter * (CHUNK / RATE)  # 计算静音时间

                # 如果静音时间超过阈值，停止录音
                if silence_time >= SILENCE_DURATION:
                    print("检测到静音，停止录音")
                    break
            else:
                silence_counter = 0  # 重置静音计数器

        # 未检测到语音且不在录音状态，保存到预缓冲
        elif not is_recording:
            pre_speech_frames.append(data)
            # 保持预缓冲大小不超过预定义时间
            if len(pre_speech_frames) > int(PRE_SPEECH_BUFFER * RATE / CHUNK):
                pre_speech_frames.pop(0)  # 移除最旧的帧

except KeyboardInterrupt:
    print("\n手动停止录制")

finally:
    print("录制完成")
    # 关闭音频流
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 如果有录音数据，进行转录
    if frames:
        # 将字节数据转换为16位整数的NumPy数组
        audio_numpy = numpy.frombuffer(b''.join(frames), dtype=numpy.int16)

        # 转换为浮点数并归一化(-1到1范围)
        audio_data = audio_numpy.astype(numpy.float32) / 32768.0

        # 进行转录
        result = whisper.transcribe(model, audio_data, initial_prompt="我是爱丽丝，你也可以叫我Arisu")

        # 输出结果
        print(f"\033[92m我的提问:{result['text']}\033[0m")
    else:
        print("没有检测到语音")