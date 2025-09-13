"""conda install ffmpeg -C conda-forge

"""

import whisper

model = whisper.load_model("medium")
result = model.transcribe(r"B:\study\python_script_study\STT语音学习\voice\1.ogg")
print(result["text"])