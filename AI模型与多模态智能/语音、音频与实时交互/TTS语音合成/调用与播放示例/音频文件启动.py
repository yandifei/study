import pyaudio
from pydub import AudioSegment
"""
重新下载并安装当前环境中已有的 Python 包及其依赖。这个过程会覆盖任何损坏或不完整的本地文件。
conda install python --force-reinstall
conda 我这个aistudy缺少audioop标准库，无法通过pip安装(标准库无法安装)

"""


# # 创建PyAudio实例并打开音频流(接收声音)
# stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,  # 音频样本(16位整数格式)
#                                 channels=1,  # 声道(1单声道2立体声)
#                                 rate=16000,  # 采样率（每秒钟从音频信号中采集多少个样本，16kHz）
#                                 input=True,  # 打开输入流，从一个音频设备（通常是你的麦克风）读取数据(录入的话搞成False会更好)
#                                 frames_per_buffer=1024)  # 每次从麦克风读取的音频帧数为1024
# with wave.open(audio_file_path, 'rb') as wf:
#     # 创建音频流(接收声音)
#     output_stream = audio.open(
#         format=audio.get_format_from_width(wf.getsampwidth()),  # 合成音频为8
#         channels=wf.getnchannels(),  # 合成音频为1
#         rate=wf.getframerate(),  # 合成音频为32000（录音用的是16000）
#         input=False,  # 关闭音频输入流
#         output=True  # 开启音频输出流
#     )  # 从音频文件里面读取播放的配置数据
# if times != 0:
#     for _ in range(times):
#         # 流式处理(不会一次性将所有数据都读入内存再播放)
#         while data := wf.readframes(1024):  # 从文件中读取下一块数据
#             # 将当前这块数据写入音频流，PyAudio 会立即播放它
#             output_stream.write(data)
#         # 将文件指针重置到文件开头
#         wf.rewind()  # 给它重新读取
# else:
#     while True:
#         wf.rewind()  # 给它重新读取
#         while data := wf.readframes(1024):  # 从文件中读取下一块数据
#             # 将当前这块数据写入音频流，PyAudio 会立即播放它
#             output_stream.write(data)
#             # 将文件指针重置到文件开头

def play_audio_file(audio_file_path: str, times : int = 1):
    """播放音频文件
    audio_file_path:音频文件路径
    times: 播放次数（0为无限循环，默认为1）
    """
    audio = pyaudio.PyAudio()  # 创建PyAudio实例并保存引用(后面得释放掉)
    output_stream = None
    try:
        # 使用pydub加载音频文件
        audio_segment = AudioSegment.from_file(audio_file_path)
        # 创建音频流(接收声音)
        output_stream = audio.open(
            format=audio.get_format_from_width(audio_segment.sample_width),     # 合成音频为8
            channels=audio_segment.channels,                                    # 合成音频为1
            rate=audio_segment.frame_rate,                                      # 合成音频为32000（录音用的是16000）
            input=False,                                                        # 关闭音频输入流
            output=True                                                         # 开启音频输出流
        )   # 从音频文件里面读取播放的配置数据

        # 有次数播放
        if times != 0:
            # 循环给定的次数   
            for _ in range(times):
                # 将数据封装成一个内存文件流，以便分块读取
                for i in range(0, len(audio_segment.raw_data), 1024):
                    output_stream.write(audio_segment.raw_data[i:i + 1024])
        else:
            while True:
                # 将数据封装成一个内存文件流，以便分块读取
                for i in range(0, len(audio_segment.raw_data), 1024):
                    output_stream.write(audio_segment.raw_data[i:i + 1024])

    # 关闭音频流避免资源泄露
    finally:
        audio.terminate()  # 确保PyAudio实例被释放
        # 确保output_stream是一个有效的音频流
        if output_stream is not None:
            output_stream.stop_stream() # 停止播放
            output_stream.close()       # 关闭音频流

play_audio_file(r"B:\study\python_script_study\STT语音学习\TTS语音合成\合成音频.wav",0)