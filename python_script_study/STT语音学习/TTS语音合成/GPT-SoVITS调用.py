
# 启动服务
# python api.py -dr "GPT-SoVITS-File/参考文本.ogg" -dt "邦邦卡邦~！老师购买了道具！附赠的微笑，也请您收下吧~！" -dl "zh" -a 0.0.0.0 -p 9880
# # GET 请求：
# curl "http://127.0.0.1:9880/?text=要合成的文本&text_language=zh"


# python api.py -s "B:\study\python_script_study\STT语音学习\GPT-SoVITS-File\爱丽丝中文_e16_s1200_l32.pth" -g "B:\study\python_script_study\STT语音学习\GPT-SoVITS-File\爱丽丝中文-e50.ckpt" -dr "B:\study\python_script_study\STT语音学习\GPT-SoVITS-File\参考文本.ogg" -dt "邦邦卡邦~！老师购买了道具！附赠的微笑，也请您收下吧~！" -dl "zh" -d "cuda"
# python api.py -s GPT-SoVITS-File/爱丽丝中文_e16_s1200_l32.pth -g "GPT-SoVITS-File/爱丽丝中文-e50.ckpt" -dr "GPT-SoVITS-File/参考文本.ogg" -dt "邦邦卡邦~！老师购买了道具！附赠的微笑，也请您收下吧~！" -dl "zh" -d "cuda"
"""
# 基本启动命令
.\runtime\python api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml


python api.py -s GPT-SoVITS-File/爱丽丝中文_e16_s1200_l32.pth
-g "B:\study\python_script_study\STT语音学习\GPT-SoVITS-File\爱丽丝中文-e50.ckpt"
-dr "B:\study\python_script_study\STT语音学习\GPT-SoVITS-File\参考文本.ogg"
-dt "邦邦卡邦~！老师购买了道具！附赠的微笑，也请您收下吧~！"
-dl "zh"
-d "cuda"
"""
import os

import requests
import json


def call_tts_api(text):
    # API端点
    url = "http://127.0.0.1:9880/tts"

    # 准备请求参数
    payload = {
        "text": text, # 合成的文本内容
        "text_lang": "zh",                  # 合成文本的语言
        "ref_audio_path": "B:\study\python_script_study\STT语音学习\GPT-SoVITS-File\参考文本.ogg",    # 参考音频文件路径
        "aux_ref_audio_paths": [],  # 辅助参考音频路径列表。用于多说话人音色融合。提供多个参考音频路径，模型会尝试将它们的声音特征融合后生成新音频。
        "prompt_text": "邦邦卡邦~！老师购买了道具！附赠的微笑，也请您收下吧~！", # 参考音频对应文本
        "prompt_lang": "zh",    # 参考音频的语言
        "top_k": 5,             # 降低top_k值会增加生成音频的随机性和创造性，但也可能降低稳定性；提高它会使输出更稳定、更可预测。
        "top_p": 1,             # 降低top_p（如0.8）增加随机性，提高它（最大1.0）增加确定性。
        "temperature": 1,       # 提高温度（>1.0）会放大概率差异，使输出更随机、更有“创意”；降低温度（<1.0）会使分布更平缓，输出更保守、更确定。
        "text_split_method": "cut5",    # 指定如何将长文本切分成短句进行合成。常见选项：cut0（按标点分割），cut1（按句子长度），cut2（中英混合优化），cut5（另一种规则）。不同方法效果不同，需要尝试。
        "batch_size": 1,        # 批处理大小。一次处理多少句文本。增大batch_size（如4或8）通常可以显著提高长文本的整体合成速度，但会增加显存占用。
        "batch_threshold": 0.75,    # 批次拆分阈值。与batch_size和split_bucket配合使用，控制如何将句子分到不同的批次中。
        "split_bucket": True,   # 是否开启分桶处理。开启后，模型会将长度相近的句子分到同一个批次中一起处理，可以显著提高合成效率。
        "speed_factor": 1.0,    # 大于1.0（如1.5）会加快语速；小于1.0（如0.8）会减慢语速
        "streaming_mode": False,    # 是否使用流式传输模式。对于极长的文本，开启此模式可以边生成边返回音频数据，减少客户端等待时间。
        "seed": -1,                 # 设置为固定的正整数（如42）可以确保每次用相同输入和参数生成的音频完全一致，用于重现结果。设为-1表示使用随机种子
        "parallel_infer": True,     # 是否使用并行推理。通常保持开启以提升性能。
        "repetition_penalty": 1.35, # 用于防止模型生成重复的词汇或音素。值大于1.0（如1.2）可以有效减少重复，但设得过高可能导致语句不完整
        "sample_steps": 32,         # 采样步数（针对VITS模型V3版本）。增加步数（如50）可能会提高音频质量，但也会增加生成时间。
        "super_sampling": False     # 超级采样（针对VITS模型V3版本）。一种后处理技术，开启后可能会提升音频的清晰度和细节，但也会增加计算开销。
    }

    # 设置请求头
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # 发送POST请求
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        # 检查响应状态
        if response.status_code == 200:
            # 保存音频文件
            with open(r"B:/study/python_script_study/STT语音学习/TTS语音合成/合成音频.wav", "wb") as f:
                f.write(response.content)
            print("音频已成功生成并保存为合成音频.wav")
        else:
            # 处理错误
            error_data = response.json()
            print(f"错误: {error_data}")

    except Exception as e:
        print(f"请求异常: {str(e)}")


def set_gpt_weights(weights_path):
    """设置 GPT 模型权重"""
    params = {
        "weights_path": weights_path
    }
    try:
        response = requests.get("http://127.0.0.1:9880/set_gpt_weights", params=params)
        if response.status_code == 200:
            print("GPT 模型切换成功！")
        else:
            print(f"GPT 模型切换失败！错误信息：{response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"请求出错：{e}")

def set_sovits_weights(weights_path):
    """设置 SoVITS 模型权重"""
    params = {
        "weights_path": weights_path
    }
    try:
        response = requests.get("http://127.0.0.1:9880/set_sovits_weights", params=params)
        if response.status_code == 200:
            print("SoVITS 模型切换成功！")
        else:
            print(f"SoVITS 模型切换失败！错误信息：{response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"请求出错：{e}")

if __name__ == "__main__":
    set_sovits_weights(r"B:\study\python_script_study\STT语音学习\GPT-SoVITS-File\爱丽丝中文_e16_s1200_l32.pth")
    set_gpt_weights(r"B:\study\python_script_study\STT语音学习\GPT-SoVITS-File\爱丽丝中文-e50.ckpt")
    call_tts_api( "我是爱丽丝，老师，早上好")

