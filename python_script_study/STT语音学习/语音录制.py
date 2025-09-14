import pyaudio
import wave     # WAV文件操作库
# 创建音频对象
audio = pyaudio.PyAudio()
# 打开音频流
stream = audio.open(format=pyaudio.paInt16, # 16位整数格式
                channels=1,                 # 单声道
                rate=16000,                 # Silero-VAD 推荐的采样率（16kHz）
                input=True,
                frames_per_buffer=1024)     # 每次从麦克风读取的音频帧数为1024
frames = []  # 创建一个空列表来存储音频数据（frames_per_buffer的数据）
print("正在监听...请开始说话。按 Ctrl+C 手动停止。")

# 公式：总采样数 / 每次读取量 = 16000/1024 ≈ 15.6次 → 取整16次
# for i in range(0, round(16000 / 1024 * 16)):
for i in range(round(15.625 * 10)):
    data = stream.read(1024)    # 读取一块音频数据
    frames.append(data)         # 把数据添加到列表中

print("录制完成")

# 停止录音
stream.stop_stream()  # 停止音频流（停止录音）
stream.close()        # 关闭音频流（删除流式对象）
audio.terminate()     # 关闭音频系统（删除音频对象）

# 写入文件（标准文件=音频格式、采样率、通道数等信息+音频数据）
with wave.open("./voice/output.wav", 'wb') as wf:  # 'wb' = 写入二进制模式
    wf.setnchannels(1)                                          # 设置声道数
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))     # 设置采样宽度
    wf.setframerate(16000)                                      # 设置采样率
    wf.writeframes(b''.join(frames))                            # 将所有数据块合并并写入文件
    # print(b''.join(frames))

# # 非标准（直接写入原始数据，某些播放器可能无法识别）
# with open("./voice/output.wav", 'wb') as wf:
#     # 将列表中的所有字节数据连接起来并写入文件
#     wf.write(b''.join(frames))