"""本地语音合成
pip install pyttsx3
文档：https://pyttsx3.readthedocs.io/en/latest/engine.html
"""

import pyttsx3

# 官方例子
# engine = pyttsx3.init()
# # engine.say('你好')
# engine.say('GPT-SoVITS崩溃，启动备用语音模型')
# engine.runAndWait()

# 官方例子改变语音声音（实际只有一种）
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# for voice in voices:
#    engine.setProperty('voice', voice.id)
#    engine.say('The quick brown fox jumped over the lazy dog.')
# engine.runAndWait()

# 个人研究
engine = pyttsx3.init()
engine.setProperty('volume', 0.5) # 设置音量，0.9 代表 90% 的音量
engine.say('GPT-SoVITS崩溃，启动备用语音模型')
engine.runAndWait()


# --- 1. 查看所有可用的语音 ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"Index: {index}, ID: {voice.id}")
    print(f"Name: {voice.name}")
    print(f"Languages: {voice.languages}\n")


# --- 2. 设置语音（变声的关键）---
# 通常，voices[0] 是系统默认语音，voices[1] 可能是另一个（例如在Windows上，0是David（男声），1是Zira（女声））
# 你可以通过索引号选择，也可以通过 voice.id 或 voice.name 来选择
selected_voice_index = 1 # 例如，尝试换成第二个声音
engine.setProperty('voice', voices[selected_voice_index].id)

# --- 3. 调整语速 ---
rate = engine.getProperty('rate') # 获取当前语速
print(f"Current Rate: {rate}")
engine.setProperty('rate', rate - 50) # 减慢语速

# --- 4. 调整音量 ---
volume = engine.getProperty('volume') # 获取当前音量（0.0-1.0）
print(f"当前音量: {volume}")
engine.setProperty('volume', 0.9) # 设置音量，0.9 代表 90% 的音量
