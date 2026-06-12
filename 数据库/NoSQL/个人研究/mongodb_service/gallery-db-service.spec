# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['gallery-db-service.py'],
    binaries=[],
    datas=[],
    hiddenimports=[
        # 日志库
        'colorlog',
        # 异步模块
        'asyncio',
        'aiofiles',
        'aiohttp',
        'starlette',
        'starlette.middleware',
        'starlette.middleware.cors',
        'charset_normalizer',
        'h11',
        'httpcore',
        'httpx',
        'websockets',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'uvicorn.protocols.http',
        'uvicorn.protocols.websockets',
        'uvicorn.loops',
        'uvicorn.loops.asyncio',
        # 添加其他可能需要的模块
        'charset_normalizer',
        'h11',
        'httpcore',
        'httpx',
        'websockets',
        'websockets.client',
        'websockets.server',
        'websockets.legacy',
        'websockets.legacy.client',
        'websockets.legacy.server',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ACG画廊数据库服务',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 图标
    icon="config/logo.ico"
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ACG画廊数据库服务',
)
