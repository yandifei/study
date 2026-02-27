"""FastAPI应用程序主入口"""

from fastapi import FastAPI
from core.config import settings
from api import api_router

def create_app() -> FastAPI:
    """创建并配置FastAPI应用"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    # 注册路由
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

# 创建应用实例
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)