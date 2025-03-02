# 路径替换为 NotMyFault.exe 的实际路径
import subprocess
"""因为协议问题我这里就不用官网的了"""
# path = r".\NotMyFault\notmyfault.exe"
# # 调用 NotMyFault 触发蓝屏
# subprocess.run([path, "/crash"])


import ctypes
# 加载 ntdll.dll
ntdll = ctypes.WinDLL('ntdll.dll')
# 提升权限
ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool(0)))
# 触发蓝屏
ntdll.NtRaiseHardError(0xC000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_ulong(0)))