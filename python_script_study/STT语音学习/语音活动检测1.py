"""给定音频文件，获得说话时间
./recording.wav
"""


from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
model = load_silero_vad()
wav = read_audio('./recording.wav')
speech_timestamps = get_speech_timestamps(
  wav,
  model,
  return_seconds=True,  # 返回语音时间戳（以秒为单位）（默认为示例）
)


import torch
torch.set_num_threads(1)

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
(get_speech_timestamps, _, read_audio, _, _) = utils

wav = read_audio('path_to_audio_file')
speech_timestamps = get_speech_timestamps(
  wav,
  model,
  return_seconds=True,  # 返回语音时间戳（以秒为单位）（默认为示例）
)