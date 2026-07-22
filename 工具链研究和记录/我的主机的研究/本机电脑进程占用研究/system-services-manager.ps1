# ============================================================================
#  Windows 系统服务 & 进程管理器
#  用途: 一键启用/禁用非必要系统服务，释放内存，提速系统
#  用法 (在管理员 PowerShell 中运行):
#      .\system-services-manager.ps1 disable     # 禁用所有非必要服务
#      .\system-services-manager.ps1 enable      # 恢复所有服务
#      .\system-services-manager.ps1 status      # 查看当前状态
#      .\system-services-manager.ps1 interactive  # 逐项选择是否禁用
# ============================================================================

#Requires -RunAsAdministrator

param(
    [ValidateSet("disable","enable","status","interactive")]
    [string]$Action = "status"
)

# ======================== 服务注册表 ========================
# Name=服务名 Group=分类 Reason=为什么可以关

$ServiceRegistry = @(
    # ---- 系统优化 ----
    @{ Name="SysMain";               Group="系统优化";    Reason="Superfetch 预加载缓存，SSD 上意义不大，还吃内存" },
    @{ Name="WSearch";               Group="系统优化";    Reason="Windows Search 搜索索引，不用自带搜索可关闭" },
    @{ Name="TabletInputService";    Group="系统优化";    Reason="触摸键盘和手写面板，无触屏设备用不上" },

    # ---- 隐私/遥测 ----
    @{ Name="DiagTrack";             Group="隐私/遥测";   Reason="微软 Connected User Experiences 遥测数据收集服务" },

    # ---- 厂商 Bloatware ----
    @{ Name="AsusUpdateCheck";       Group="厂商Bloatware"; Reason="华硕主板自动更新检查程序" },
    @{ Name="ClickToRunSvc";         Group="厂商Bloatware"; Reason="Microsoft Office 后台即点即用更新" },
    @{ Name="Apple Mobile Device Service"; Group="厂商Bloatware"; Reason="iTunes/iPhone 连接服务，无 Apple 设备可关" },

    # ---- 游戏 (保留，默认不关) ----
    @{ Name="XboxNetApiSvc";         Group="游戏";        Reason="Xbox Live 网络服务 — 默认保留" },
    @{ Name="XblAuthManager";        Group="游戏";        Reason="Xbox Live 身份验证管理器 — 默认保留" },
    @{ Name="XblGameSave";           Group="游戏";        Reason="Xbox Live 游戏存档同步 — 默认保留" },
    @{ Name="BcastDVRUserService";   Group="游戏";        Reason="GameDVR 游戏录制和广播 — 默认保留" },

    # ---- 桌面体验 ----
    @{ Name="MapsBroker";            Group="桌面体验";    Reason="离线地图下载管理，桌面 PC 不需要" },
    @{ Name="lfsvc";                 Group="桌面体验";    Reason="地理定位服务，桌面 PC 不需要" },
    @{ Name="PhoneSvc";              Group="桌面体验";    Reason="Windows Phone 关联服务，已废弃" },
    @{ Name="WpcMonSvc";             Group="桌面体验";    Reason="家长控制/家庭安全监控" },
    @{ Name="PcaSvc";                Group="桌面体验";    Reason="程序兼容性助手，基本只弹无用警告" },
    @{ Name="DmEnrollmentSvc";       Group="桌面体验";    Reason="设备管理注册，个人 PC 不需要" },

    # ---- 远程工具 (保留，默认不关) ----
    @{ Name="GameViewerService";     Group="远程工具";    Reason="网易UU远程后台服务 — 默认保留" }
)

# Widgets 特殊处理：它是 Appx 包，不是服务
$WidgetsRegPath  = "HKLM:\SOFTWARE\Policies\Microsoft\Dsh"
$WidgetsRegName  = "AllowNewsAndInterests"
$WidgetsAppxName = "*WebExperience*"
$WidgetsProcs    = @("Widgets","WidgetService")

# ======================== 内部函数 ========================

function Write-Banner {
    param([string]$Text)
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host "  $Text" -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
}

function Stop-And-Disable {
    param($ServiceName)
    $svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if (-not $svc) { return "NOT_FOUND" }
    try {
        if ($svc.Status -eq 'Running') {
            Stop-Service -Name $ServiceName -Force -ErrorAction Stop
        }
        Set-Service -Name $ServiceName -StartupType Disabled -ErrorAction Stop
        return "OK"
    } catch {
        return "FAIL: $_"
    }
}

function Enable-And-Start {
    param($ServiceName, [string]$TargetStartType = "Manual")
    $svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
    if (-not $svc) { return "NOT_FOUND" }
    try {
        Set-Service -Name $ServiceName -StartupType $TargetStartType -ErrorAction Stop
        if ($TargetStartType -eq 'Automatic') {
            Start-Service -Name $ServiceName -ErrorAction SilentlyContinue
        }
        return "OK"
    } catch {
        return "FAIL: $_"
    }
}

# ======================== 动作分发 ========================

switch ($Action) {

    # ============================================================
    #  status — 查看所有服务的当前运行状态
    # ============================================================
    "status" {
        Write-Banner "当前服务运行状态"
        $groups = $ServiceRegistry | Group-Object Group
        foreach ($g in $groups) {
            Write-Host ""
            Write-Host "  [$($g.Name)]" -ForegroundColor Yellow
            foreach ($item in $g.Group) {
                $svc = Get-Service -Name $item.Name -ErrorAction SilentlyContinue
                if ($svc) {
                    $color = if ($svc.Status -eq 'Running') { 'Red' }
                        elseif ($svc.StartType -eq 'Disabled') { 'Green' }
                        else { 'Gray' }
                    Write-Host ("    {0,-30} Status={1,-8} StartType={2,-10} | {3}" -f $item.Name, $svc.Status, $svc.StartType, $item.Reason) -ForegroundColor $color
                } else {
                    Write-Host ("    {0,-30} [服务不存在]" -f $item.Name) -ForegroundColor DarkGray
                }
            }
        }
        # Widgets
        Write-Host ""
        Write-Host "  [Widgets 小组件]" -ForegroundColor Yellow
        $reg = Get-ItemProperty -Path $WidgetsRegPath -Name $WidgetsRegName -ErrorAction SilentlyContinue
        $running = Get-Process -Name $WidgetsProcs -ErrorAction SilentlyContinue
        if ($reg -and $reg.$WidgetsRegName -eq 0) {
            Write-Host "    注册表策略: 已禁用" -ForegroundColor Green
        } else {
            Write-Host "    注册表策略: 未禁用" -ForegroundColor Red
        }
        if ($running) {
            Write-Host "    进程状态: 正在运行 ($($running.Count) 个实例)" -ForegroundColor Red
        } else {
            Write-Host "    进程状态: 未运行" -ForegroundColor Green
        }
        Write-Host ""
    }

    # ============================================================
    #  disable — 禁用所有非必要服务和组件
    # ============================================================
    "disable" {
        Write-Banner "正在禁用非必要服务..."

        # --- Widgets ---
        Write-Host ""
        Write-Host "  [Widgets 小组件]" -ForegroundColor Yellow
        $widgetProcs = Get-Process -Name $WidgetsProcs -ErrorAction SilentlyContinue
        if ($widgetProcs) {
            $widgetProcs | Stop-Process -Force -ErrorAction SilentlyContinue
            Write-Host "    ✓ 已终止 Widgets 进程" -ForegroundColor Green
        } else {
            Write-Host "    - Widgets 进程未运行" -ForegroundColor DarkGray
        }
        try {
            New-ItemProperty -Path $WidgetsRegPath -Name $WidgetsRegName -Value 0 -PropertyType DWORD -Force -ErrorAction Stop | Out-Null
            Write-Host "    ✓ 注册表策略已设置: 禁用小组件" -ForegroundColor Green
        } catch {
            Write-Host "    ✗ 注册表写入失败: $_" -ForegroundColor Red
        }
        try {
            $pkg = Get-AppxPackage $WidgetsAppxName -ErrorAction SilentlyContinue
            if ($pkg) {
                $pkg | Remove-AppxPackage -ErrorAction Stop
                Write-Host "    ✓ Appx 包已卸载" -ForegroundColor Green
            } else {
                Write-Host "    - Appx 包不存在，跳过" -ForegroundColor DarkGray
            }
        } catch {
            Write-Host "    ✗ Appx 卸载失败: $_" -ForegroundColor Red
        }

        # --- 服务 ---
        $groups = $ServiceRegistry | Group-Object Group
        foreach ($g in $groups) {
            Write-Host ""
            Write-Host "  [$($g.Name)]" -ForegroundColor Yellow
            foreach ($item in $g.Group) {
                $result = Stop-And-Disable $item.Name
                switch -Wildcard ($result) {
                    "OK"        { Write-Host "    ✓ $($item.Name) -> 已停止并禁用" -ForegroundColor Green }
                    "NOT_FOUND" { Write-Host "    - $($item.Name) -> 服务不存在，跳过" -ForegroundColor DarkGray }
                    "FAIL*"     { Write-Host "    ✗ $($item.Name) -> $result" -ForegroundColor Red }
                }
            }
        }

        # 同样杀掉 Touch Keyboard 相关进程
        Write-Host ""
        Write-Host "  [额外进程清理]" -ForegroundColor Yellow
        $extraProcs = @("TabTip","OfficeClickToRun","AsusUpdateCheck","AppleMobileDeviceService")
        foreach ($pname in $extraProcs) {
            $p = Get-Process -Name $pname -ErrorAction SilentlyContinue
            if ($p) {
                $p | Stop-Process -Force -ErrorAction SilentlyContinue
                Write-Host "    ✓ $pname 进程已终止" -ForegroundColor Green
            }
        }

        Write-Host ""
        Write-Banner "全部完成！建议重启使更改彻底生效"
        Write-Host "  恢复命令: .\system-services-manager.ps1 enable" -ForegroundColor Gray
        Write-Host "  查看状态: .\system-services-manager.ps1 status" -ForegroundColor Gray
    }

    # ============================================================
    #  enable — 恢复所有服务到默认启动类型
    # ============================================================
    "enable" {
        Write-Banner "正在恢复服务到默认状态..."

        # --- Widgets ---
        Write-Host ""
        Write-Host "  [Widgets 小组件]" -ForegroundColor Yellow
        Remove-ItemProperty -Path $WidgetsRegPath -Name $WidgetsRegName -Force -ErrorAction SilentlyContinue
        Write-Host "    ✓ 注册表限制已移除"
        Write-Host "    ! Appx 包需从 Microsoft Store 重新安装（若已卸载）" -ForegroundColor DarkYellow

        # 恢复为 Automatic 的服务
        $asAuto = @("SysMain","WSearch","DiagTrack","XboxNetApiSvc","XblAuthManager","BcastDVRUserService","MapsBroker","PcaSvc")
        # 恢复为 Manual 的服务
        $asManual = @("TabletInputService","AsusUpdateCheck","ClickToRunSvc",
                      "Apple Mobile Device Service","XblGameSave","lfsvc","PhoneSvc",
                      "WpcMonSvc","DmEnrollmentSvc","GameViewerService")

        $groups = $ServiceRegistry | Group-Object Group
        foreach ($g in $groups) {
            Write-Host ""
            Write-Host "  [$($g.Name)]" -ForegroundColor Yellow
            foreach ($item in $g.Group) {
                $target = if ($item.Name -in $asAuto) { "Automatic" } else { "Manual" }
                $result = Enable-And-Start $item.Name $target
                switch -Wildcard ($result) {
                    "OK"        { Write-Host "    ✓ $($item.Name) -> 已恢复为 $target" -ForegroundColor Green }
                    "NOT_FOUND" { Write-Host "    - $($item.Name) -> 服务不存在，跳过" -ForegroundColor DarkGray }
                    "FAIL*"     { Write-Host "    ✗ $($item.Name) -> $result" -ForegroundColor Red }
                }
            }
        }

        Write-Host ""
        Write-Banner "恢复完成"
        Write-Host "  部分服务可能需要重启才能生效" -ForegroundColor DarkYellow
    }

    # ============================================================
    #  interactive — 逐项选择
    # ============================================================
    "interactive" {
        Write-Banner "逐项选择模式"
        Write-Host "  输入: y=禁用  n=保留  q=退出"
        Write-Host ""
        foreach ($item in $ServiceRegistry) {
            $svc = Get-Service -Name $item.Name -ErrorAction SilentlyContinue
            if (-not $svc) { continue }
            $choice = Read-Host "  [$($item.Group)] $($item.Name) — $($item.Reason)`n    当前: Status=$($svc.Status) StartType=$($svc.StartType) -> [y/n/q]"
            if ($choice -eq 'q') { break }
            if ($choice -eq 'y') {
                $result = Stop-And-Disable $item.Name
                $fg = if ($result -eq 'OK') { 'Green' } else { 'Red' }
                Write-Host "    -> $result" -ForegroundColor $fg
            }
        }
        Write-Host ""
        Write-Host "交互模式结束。" -ForegroundColor Cyan
    }
}
