from time import sleep

import pyttsx3

engine = pyttsx3.init()
# windows有bug，我必须手动控制循环
engine.startLoop(False)


voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"索引: {index} | 名称: {voice.name} | 语言: {voice.languages}")


def speak(text: str):
    engine.say(text)
    while engine.isBusy():
        engine.iterate()

speak("1111")
speak("你好")