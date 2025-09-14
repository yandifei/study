import speech_recognition as sr

# 创建识别器对象
r = sr.Recognizer()

# 设置麦克风为源
with sr.Microphone() as source:
    print("请说话...")
    # 循环实现持续监听
    while True:
        try:
            # 调整环境噪音
            r.adjust_for_ambient_noise(source)
            # 监听音频输入，timeout 表示等待语音开始的最大时间，phrase_time_limit 表示允许说话的最长时间
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
            # 使用Google Web Speech API进行识别（需要网络连接）
            text = r.recognize_whisper(audio, language='zh-CN')
            # recognize_google(audio, language='zh-CN')
            print(f"识别结果: {text}")
        except sr.WaitTimeoutError:
            # 处理超时（一段时间内没有检测到语音）
            print("未检测到语音，继续监听...")
        except sr.UnknownValueError:
            # 处理识别不清
            print("无法识别音频")
        except sr.RequestError as e:
            # 处理API错误
            print(f"无法从Google Speech Recognition服务获取结果; {e}")
        except KeyboardInterrupt:
            # 用户中断（如按Ctrl+C）
            print("停止监听")
            break