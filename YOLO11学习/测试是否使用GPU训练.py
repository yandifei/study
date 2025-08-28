"""
需要注意的点是如果直接使用官网的 pip install ultralytics 指令下载的pytorch是cpu版本
去pytorch官网https://pytorch.org/get-started/locally/找下载指令
我的下载指令(5080)
我的显卡cuda版本是CUDA Version: 13.0，但是我pip的是12.6版本，显示我不兼容(我显卡版本太新了，pytorch的cuda太垃圾)
pytorch cuda 12.9下载指令: pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu129
这东西3.6GB，cpu版本的一秒下好
这个指令的报错能提示PyTorch版本是否兼容
"""
import torch

# 查看当前PyTorch版本
print(f"PyTorch版本:{torch.__version__}")

# 检查GPU是否可用
print("CUDA 是否可以使用:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("训练使用的GPU设备:", torch.cuda.get_device_name(0))
    print("训练使用的GPU数量:", torch.cuda.device_count())
else:
    print("训练使用CPU")

"""
# 卸载当前PyTorch
pip uninstall torch torchvision torchaudio

# 检查NVIDIA驱动
nvidia-smi

# 检查CUDA版本
nvcc --version
"""