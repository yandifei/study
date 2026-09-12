frames = []  # 创建一个空列表来存储音频数据（frames_per_buffer的数据）
    # 读取音频数据
    data = stream.read(1024, exception_on_overflow=False)
    audio_frame = numpy.frombuffer(data, dtype=numpy.int16)
    # 转换为浮点数并归一化(-1到1范围)
    audio_float = audio_frame.astype(numpy.float32) / 32768.0

    # 使用VAD检测语音
    with torch.no_grad():
        speech_prob = model(torch.from_numpy(audio_float), 16000).item()

    print("检测到语音，开始录音...")

    # 大于设定的阈值
    if speech_prob > 0.5 and not is_recording_flag:
        # 正在录音标志
        is_recording_flag = True
        # 添加当前帧
        frames.append(data)
    else:
        pass
    """进行转录"""
    # 将字节数据转换为16位整数的NumPy数组(将列表中的字节数据连接起来)
    audio_numpy = numpy.frombuffer(b''.join(frames), dtype=numpy.int16).astype(numpy.float32) / 32768.0
    # 进行转录
    result = whisper.transcribe(model, audio_numpy, initial_prompt="我是爱丽丝，你也可以叫我Arisu")
    # 输出结果
    print(f"\033[92m我的提问:{result["text"]}\033[0m")