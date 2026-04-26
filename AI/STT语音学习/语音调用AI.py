import warnings
# from ollama import chat   # 不再使用 Ollama
import numpy
import pyaudio
import pyttsx3
import whisper
# VAD语音活动检测，后面才用到，这里用不到
# from silero_vad import load_silero_vad
# 调用 DeepSeek API 需要
from openai import OpenAI

# ========== 1. 配置 DeepSeek API ==========
DEEPSEEK_API_KEY = ""  # 请替换为你自己的 API Key
DEEPSEEK_MODEL = "deepseek-chat"  # 使用的模型名称

# ========== 2. 读取人设 ==========
role: str
with open("爱丽丝人格.md", "r", encoding="utf-8") as f:
    role = f.read()
# role = """
# **回复长度**：通常1句话且不超过10个字(对方希望输出更多时1~3句，整体不超过50字)。特殊情况（如描述具体行为、讲述故事、表达复杂情绪）可稍长，但禁止输出大段文本或结构化内容。
# **输出格式**：默认输出纯文本，禁用任何标记语言。如果用户明确要求其他格式，仅在当次回复中遵循。
# **上下文适应**：无论前文内容多长（如文献、代码等），我的回复都必须切换到简短口语模式且回答内容符合我当前回答的问题，不延续前文的格式或长度。
# """
# ========== 3. 初始化对话历史（固定 system prompt）==========
conversation_history = [
    {"role": "system", "content": role}
]
MAX_HISTORY_ROUNDS = 10  # 最多保留的对话轮数


def chat_with_deepseek(user_input, history_messages):
    """
    调用 DeepSeek API，自动管理对话历史长度。
    user_input: 用户当前输入的文本
    history_messages: 当前的对话历史列表（会在此函数内被修改）
    返回: AI 回复的文本，以及更新后的历史列表
    """
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com"
    )

    # 将用户新输入加入历史
    history_messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=history_messages,
            stream=False
        )
        assistant_response = response.choices[0].message.content
        # 将 AI 回复加入历史
        history_messages.append({"role": "assistant", "content": assistant_response})

        # 裁剪历史：保留 system prompt + 最近 MAX_HISTORY_ROUNDS 轮对话
        # 每轮对话包含 user 和 assistant 两条消息，所以总消息数 = 1 + 2 * 轮数
        if len(history_messages) > 1 + MAX_HISTORY_ROUNDS * 2:
            # 保留 system prompt，然后只保留最后 MAX_HISTORY_ROUNDS*2 条消息
            history_messages = [history_messages[0]] + history_messages[-(MAX_HISTORY_ROUNDS * 2):]
            print(f"[对话历史] 已自动裁剪至最近 {MAX_HISTORY_ROUNDS} 轮。")

        return assistant_response, history_messages
    except Exception as e:
        print(f"调用 DeepSeek API 出错: {e}")
        return None, history_messages


# ========== 音频对象创建 ==========
audio = pyaudio.PyAudio()


def find_working_microphone():
    """
    自动检测并返回第一个可用的麦克风设备索引
    返回: (device_index, device_name) 或 (None, None)
    """
    print("正在扫描可用的麦克风设备...")
    
    # 获取所有输入设备信息
    device_count = audio.get_device_count()
    input_devices = []
    
    for i in range(device_count):
        try:
            device_info = audio.get_device_info_by_index(i)
            # 检查是否有输入通道
            if device_info['maxInputChannels'] > 0:
                input_devices.append({
                    'index': i,
                    'name': device_info['name'],
                    'channels': device_info['maxInputChannels']
                })
        except Exception as e:
            continue
    
    if not input_devices:
        print("错误: 未找到任何输入设备！")
        return None, None
    
    print(f"\n发现 {len(input_devices)} 个输入设备:")
    for idx, device in enumerate(input_devices):
        print(f"  [{idx}] {device['name']} (通道数: {device['channels']})")
    print()
    
    # 尝试每个设备，直到找到一个能正常打开的
    for device in input_devices:
        device_index = device['index']
        device_name = device['name']
        
        try:
            print(f"正在测试设备: {device_name} ...", end=' ')
            test_stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=1024
            )
            
            # 尝试读取一小段数据来验证设备是否真正可用
            test_data = test_stream.read(1024, exception_on_overflow=False)
            
            # 如果成功读取，关闭测试流并返回此设备
            test_stream.stop_stream()
            test_stream.close()
            
            print("✓ 可用")
            return device_index, device_name
            
        except Exception as e:
            print(f"✗ 失败 ({str(e)[:50]})")
            continue
    
    print("\n错误: 所有设备都无法使用！")
    return None, None


# 查找可用的麦克风
device_index, device_name = find_working_microphone()

if device_index is None:
    print("\n无法找到可用的麦克风，程序退出。")
    audio.terminate()
    exit(1)

print(f"\n使用设备: {device_name} (索引: {device_index})")
print("="*60)

# 使用找到的设备创建音频流
try:
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=1024)
    print("音频流已成功创建\n")
except Exception as e:
    print(f"\n创建音频流失败: {e}")
    audio.terminate()
    exit(1)

# ========== Whisper 初始化 ==========
warnings.filterwarnings("ignore", message="Performing inference on CPU when CUDA is available")
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
model = whisper.load_model("turbo", "cuda", download_root="models_files")
# model = whisper.load_model("tiny", download_root="models_files")

# ========== pyttsx3 初始化 ==========
engine = pyttsx3.init()
# 我来控制循环防止windows的bug
engine.startLoop(False)

def call_tts_api(text: str):
    """使用 pyttsx3 进行语音合成并直接播放"""
    # 检测输入是否有效
    if text == "":
        return False

    # 调用 pyttsx3
    engine.say(text)
    while engine.isBusy():
        engine.iterate()
    return True


# ========== 主循环 ==========
while True:

    frames = []
    print("正在监听...请开始说话。按 Ctrl+C 手动停止。")
    for i in range(round(15.625 * 5)):
        data = stream.read(1024)
        frames.append(data)
    print("录制完成")

    audio_data = numpy.frombuffer(b''.join(frames), dtype=numpy.int16).astype(numpy.float32) / 32768.0

    # Whisper 语音识别
    result = whisper.transcribe(model, audio_data, initial_prompt="我是爱丽丝，你也可以叫我Arisu")
    user_query = result["text"]
    print(f"\033[92m我的提问:{user_query}\033[0m")

    # 退出条件
    if user_query == "退出":
        break

    # ========== 调用 DeepSeek API 获取回复 ==========
    ai_response, conversation_history = chat_with_deepseek(user_query, conversation_history)
    if ai_response:
        print(f"\033[95mAI回答:{ai_response}\033[0m")
        call_tts_api(ai_response)
    else:
        print("AI 生成回答失败，跳过本次语音播放。")
        continue

# 清理资源
stream.stop_stream()
stream.close()
audio.terminate()