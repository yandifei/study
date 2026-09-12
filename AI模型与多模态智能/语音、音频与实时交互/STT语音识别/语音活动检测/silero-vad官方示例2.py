import torch
torch.set_num_threads(1)

# 加上trust_repo可以去掉警告，警告存在是因为PyTorch和TorchAudio提示你运行了来自不受信任仓库的代码
# model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', trust_repo=True)

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')

(get_speech_timestamps, _, read_audio, _, _) = utils

wav = read_audio('../voice/output.wav')
speech_timestamps = get_speech_timestamps(
  wav,
  model,
  return_seconds=True,  # 返回语音时间戳（以秒为单位）（默认为示例）
)
print(speech_timestamps)