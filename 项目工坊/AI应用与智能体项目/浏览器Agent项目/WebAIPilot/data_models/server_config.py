from pydantic import BaseModel


class ServerConfig(BaseModel):
    """服务器配置模型"""
    # 请求协议（http或https）
    protocol: str = "http"
    # 监听的主机地址，"0.0.0.0"：允许所有网络接口访问（外网可访问，有风险）
    host: str = "127.0.0.1" # "127.0.0.1"：只允许本机访问（最安全），"localhost"：同 127.0.0.1
    # 端口号（2021.03.25是爱丽丝的生日）
    port: int = 21325