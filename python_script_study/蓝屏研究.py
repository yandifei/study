# 路径替换为 NotMyFault.exe 的实际路径
import subprocess
"""因为协议（法律）问题我这里就不用微软官方的方法了"""
# path = r".\NotMyFault\notmyfault.exe"
# # 调用 NotMyFault 触发蓝屏
# subprocess.run([path, "/crash"])

import ctypes
ntdll = ctypes.WinDLL('ntdll.dll')  # 加载 ntdll.dll
ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref (ctypes.c_bool(0)))  # 提升权限
ntdll.NtRaiseHardError(0xC000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_ulong(0))) # 触发蓝屏
# 怎么让蓝屏改为用户手动重启呢？以后思考
pass