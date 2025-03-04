import psutil   # 学习的库
from win32process import GetWindowThreadProcessId # 通过窗口句柄用来获取pid的
from datetime import datetime   # 用来计算时间（）
from time import sleep  # 必要的函数（用来等待）


# CPU
def get_cpu_times(per_cpu=False):
    """
    参数：per_cpu=False（如果为True则返回每个逻辑 CPU 的命名元组列表）
    返回值（如果per_cpu是True则会返回一个更大的列表）：
    user在用户模式下执行的正常进程所花费的时间
    system在内核模式下执行的进程所花费的时间
    idle无所事事所花费的时间
    interrupt处理硬件中断所花费的时间
    dpc为延迟过程调用 （DPC） 提供服务所花费的时间( DPC 是以低于标准中断的优先级运行的中断)
    """
    return psutil.cpu_times(per_cpu)

# noinspection PyTypeChecker
def get_cpu_utilization(interval=None,per_cpu=False):
    """获得cpu的利用率（包括虚拟cpu利用率，在多线程上可以见到）
    参数：
    如果interval为None则为非阻塞模式，立即返回自上次调用或模块导入后的 CPU 利用率。首次调用无效，需忽略。
    interval:  阻塞指定时间（秒），返回该时间段内的平均 CPU 利用率。首次调用即可获得有效结果。
    per_cpu ： 默认False，如果为True则返回每个cpu的利用率（适用于多核监控）
    返回值：
    一个浮点数，表示当前系统范围的 CPU 利用率
    如果per_cpu为True则返回所有cpu的利用率(列表)
    """
    return psutil.cpu_percent(interval, per_cpu)    # 爆警告不用管

def get_cpu_times_percent(interval=None,per_cpu=False):
    """获得CPU 时间分布的百分比统计（interval=None即为非阻塞，初次输出可能为全 0.0，必须先调用一次）
    参数：
    interval : 监控时间间隔（秒）。若为 None，非阻塞模式；若 >0，阻塞并计算分布。
    per_cpu : 是否按逻辑 CPU 核心分别返回时间分布。True 表示分核心返回列表。
    返回值：
    元组（scputimes）
    user：用户态时间（非特权进程）。
    system：内核态时间（系统调用、中断等）。
    idle：空闲时间。
    nice（Unix/Linux）：优先级调整后的用户态时间。
    iowait（Linux）：等待 I/O 完成的时间。
    irq（Linux）：处理硬件中断时间。
    softirq（Linux）：处理软件中断时间。
    steal（Linux）：虚拟化环境下被其他 VM 占用的时间。
    guest（Linux）：运行虚拟 CPU 的时间。
    guest_nice（Linux）：优先级调整后的虚拟 CPU 时间。
    """
    return psutil.cpu_times_percent(interval, per_cpu)

def get_cpu_count(logic_count=True):
    """获得逻辑核心数或物理核心数
    参数：
    logic_count : 逻辑核心数，默认为True，如果为False则获取物理核心数
    返回值:
    逻辑核心数或物理核心数
    """
    if logic_count:
        return psutil.cpu_count(True)
    elif not logic_count: # 获取物理核心数
        real_cpu_count = psutil.cpu_count(False)    # 获得真实的物理核心数
        if real_cpu_count:     # 返回值不是None
            return real_cpu_count   # 返回物理核心数
        else:
            return "该系统不支持物理核心的统计"

def get_cup_stats():
    """获取各种 CPU 统计信息
    返回值：
    ctx_switches： 自引导以来的上下文切换次数（自愿 + 非自愿）。
    中断： 自启动以来的中断数。
    soft_interrupts： 自启动以来的软件中断数。Linux、macOS（其他平台为 0）
    syscalls：自系统启动以来的系统调用次数。Linux（其他平台为 0）
    """
    return psutil.cpu_stats()

def get_cup_frequency(per_cpu=False):
    """获取cpu的频率（如果是windows用户不要填参数）
    参数：
    per_cpu ： 是否分核心返回频率，True表示按逻辑核心返回列表（仅支持 Linux 和 FreeBSD）
    返回值：
    current：当前频率（MHz）。
    min：最小频率（MHz）。若无法获取则返回 0.0。
    max：最大频率（MHz）。若无法获取则返回 0.0
    """
    return psutil.cpu_freq(per_cpu)

def get_average_system_load():
    """元组形式返回过去 1 分钟、5 分钟和 15 分钟的平均系统负载
    平均负载值反映了系统的整体负载压力，需结合 逻辑 CPU 核心数 来解读其实际意义。
    Windows后台线程模拟（每 5 秒更新）首次及 5 秒内无效（返回 0.0）,其它系统直接获取
    若负载值 ≤ 核心数：系统资源充足，无显著瓶颈。
    若负载值 > 核心数：系统过载，可能存在性能问题
    若Windows 始终返回 (0.0, 0.0, 0.0)管理员权限运行脚本。原因：后台线程未完成初始化或权限不足。
    问题 2：负载值与 CPU 利用率不匹配。问题 3：容器中负载值不准确
    """
    psutil.getloadavg()
    sleep(6)    #   等待6秒稳
    return psutil.getloadavg()

# 内存(Memory)
def get_virtual_memory():
    """以命名元组的形式返回有关系统内存使用情况的统计信息
    total：总物理内存（独占交换）。
    available：可以立即提供给进程的内存，而无需 系统进入 SWAP 状态。
    这是通过对不同的内存指标求和来计算的，这些指标因 在平台上。它应该用于监控实际的内存使用情况 以跨平台的方式。
    percent：使用百分比计算为 。(total - available) / total * 100
    其他指标：
    used：使用的内存
    free：完全未使用的 （清零） 现成可用的内存; 请注意，这并不反映实际的可用内存（请改用 available）。total - used 不一定匹配 free。
    active （UNIX）：当前正在使用或最近使用的内存，等等 它在 RAM 中。
    inactive （UNIX）：标记为未使用的内存。
    buffers （Linux， BSD）：缓存文件系统元数据等内容。
    cached （Linux， BSD）：各种事物的缓存。
    shared （Linux， BSD）：可同时由 多个进程。
    slab （Linux）：内核内数据结构缓存。
    wired （BSD， macOS）：标记为始终保留在 RAM 中的内存。是的 从未移动到磁盘。
    """
    return psutil.virtual_memory()

def get_swap_memory():
    """获得系统的交换内存（Swap Memory） 统计信息，包括总大小、已使用量、空闲量、使用百分比以及换入/换出的字节数
    交换内存是当物理内存（RAM）不足时，系统将部分内存数据临时存储到磁盘上的机制。
    返回值：
    total   : 总交换内存大小（字节）。
    used    : 已使用的交换内存大小（字节）。
    free    : 空闲的交换内存大小（字节）。
    percent : 交换内存使用百分比，计算公式为 (used / total) * 100。
    sin     :   系统从磁盘换入的字节数（累计值）。
    sout    :  系统从磁盘换出的字节数（累计值）。
    """
    return psutil.swap_memory()

# 磁盘(Disk)
def get_disk_information(filter_flag = False):
    """获得磁盘的信息
    参数：
    filter_flag ：默认为False即为开启过滤伪文件系统（如内存文件系统、重复挂载点），如果为Ture则关闭过滤
    返回值：
    device：设备路径
    mountpoint：挂载点路径
    fstype：分区文件系统
    opts：一个逗号分隔的字符串，表示 驱动器/分区
    """
    return psutil.disk_partitions(filter_flag)

def get_disk_usage(path):
    """获得磁盘的使用情况（总空间、已用空间、可用空间、使用百分比）
    参数：
    path ：
    返回值：
    total ： 总空间
    used ： 已用空间
    free ： 可用空间
    percent ： 使用百分比
    """
    return psutil.disk_usage(path)
# noinspection PyTypeChecker
def get_disk_io_count(per_disk=False,nowrap=True):
    """将系统范围的磁盘 I/O 统计信息作为命名元组返回
    参数：
    per_disk ： 默认为False，返回总磁盘的I/O统计信息，如果为Ture则返回不同磁盘的I/O统计信息
    nowrap ： 是否自动处理计数器溢出（将溢出后的新值累加到旧值上，确保数值单调递增）。
    返回值：
    read_count：读取次数
    write_count：写入次数
    read_bytes：读取的字节数
    write_bytes：写入的字节数
    read_time：读取所花费的时间 磁盘（以毫秒为单位）
    write_time：写入磁盘所花费的时间 （以毫秒为单位）
    busy_time：（Linux、FreeBSD）执行实际 I/O 所花费的时间（在 毫秒）
    read_merged_count （Linux）：合并读取的数量
    write_merged_count （Linux）：合并写入次数
    """
    return psutil.disk_io_counters(per_disk,nowrap)

# 网络（net）
# noinspection PyTypeChecker
def get_net_io_count(per_nic=False,nowrap=True):
    """获得系统范围的网络 I/O 统计信息
    参数：
    per_nic ：是否按网络接口返回统计信息。若为 True，返回字典（键为接口名，值为统计元组）
    nowrap ：是否自动处理计数器溢出（将溢出后的新值累加到旧值上，确保数值单调递增）
    返回值：
    bytes_sent：发送的字节数
    bytes_recv：接收的字节数
    packets_sent：发送的数据包数
    packets_recv：收到的数据包数
    errin：接收时的错误总数
    errout：发送时的错误总数
    dropin：被丢弃的传入数据包总数
    dropout：被丢弃的传出数据包总数（始终为 0 在 macOS 和 BSD 上）
    """
    return psutil.net_io_counters(per_nic,nowrap)

def get_net_connections(kind="inet"):
    """系统范围的套接字连接
    参数：
    kind ： 过滤连接类型。（以下是可选参数）
    "inet"（IPv4 和 IPv6）     "inet4"（IPv4 协议）    "inet6"（IPv6 协议）
    "tcp"（TCP 协议）   "tcp4"（基于 IPv4 的 TCP）   "tcp6"（基于 IPv6 的 TCP）
    "udp"（UDP 协议）   "udp4"（基于 IPv4 的 UDP）   "udp6"（基于 IPv6 的 UDP）
    "unix"（UNIX 套接字（UDP 和 TCP 协议））  "all"（所有可能的族和协议的总和）
    返回值：
    fd：套接字文件描述符。如果连接引用当前的 process 这个可以传递给 socket.fromfd 来获取可用的 socket 对象。 在 Windows 和 SunOS 上，此参数始终设置为 。-1
    family：地址系列，可以是 AF_INET、AF_INET6 或 AF_UNIX。
    type：地址类型，可以是 SOCK_STREAM、SOCK_DGRAM 或 SOCK_SEQPACKET。
    laddr：本地地址，作为命名 Tuples 或 a （如果AF_UNIX套接字）。对于 UNIX 套接字，请参阅下面的注释。(ip, port)path
    raddr：远程地址，作为命名元组或 absolute 的 UNIX 套接字。 当远程端点未连接时，你将得到一个空元组 （AF_INET*） 或 （AF_UNIX）。对于 UNIX 套接字，请参阅下面的注释。(ip, port)path""
    status：表示 TCP 连接的状态。返回值 是 psutil 之一。CONN_* 常量 （字符串）。 对于 UDP 和 UNIX 套接字，这始终是 .
    pid：打开套接字的进程的 PID（如果可检索）， 还。在某些平台（例如 Linux）上，此 字段根据进程权限更改（需要 root）。None

    """
    return psutil.net_connections(kind)

def get_net_if_address():
    """获得每个 NIC（网络接口卡）关联的地址
    family：地址系列，AF_INET 或 AF_INET6 或 ，指的是 MAC 地址。
    address：主 NIC 地址（始终设置）。
    netmask：网络掩码地址（可能是None）。
    broadcast：广播地址（可能是None）。
    PTP：代表“点对点”;它是 点对点接口（通常为 VPN）。broadcast 和 ptp 是 互斥。可能为None
    """
    return psutil.net_if_addrs()

def get_net_if_stats():
    """获得系统中所有网络接口（NIC）的状态信息，包括是否启用、双工模式、速度、MTU（最大传输单元）及标志位等。
    适用于监控网络接口的健康状态、配置及性能。
    返回值 ：字典，键为网络接口名称（如 eth0、wlan0），值为 命名元组
    """
    return psutil.net_if_stats()

# 传感器（Sensors）|温度监控之类的
def get_hardware_temperature(fahrenheit=False):
    """Windows系统不能用。获得硬件的温度，包括 CPU、硬盘等设备的当前温度、高温阈值和临界温度。
    参数：
    fahrenheit 默认为True即返回摄氏度，如果为Ture则返回华摄氏度
    """
    return psutil.sensors_temperatures(fahrenheit)

def restore_fans():
    """恢复风扇的速度（Linux才能用）
    返回值：字典，label，风扇标签（如 cpu_fan、system_fan）|    current，当前风扇转速（单位：RPM）。
    """
    return psutil.sensors_fans()

def get_battery_information():
    """获得电池的信息（用于获取设备的电池状态信息，包括剩余电量百分比、剩余续航时间（秒）以及是否连接电源。）
    返回值：
    percent ： “剩余电池电量百分比” 或 “设备为台式机或无法获取电池信息”
    secsleft ： 电池剩余续航时间（秒），若已连接电源则为“电源连接续航无限”，若无法获取则返回"设备为台式机或无法计算电池剩余续航时间"
    power_plugged ： 如果交流电源线已连接则返回“电源已连接”，如果未连接或无法确定则返回"未连接电源或无法确定电源是否连接"
    """
    battery_information = list(psutil.sensors_battery())
    if battery_information[0] is None:
        battery_information[0] = "设备为台式机或无法获取电池信息"
    if battery_information[1] == psutil.POWER_TIME_UNLIMITED:
        battery_information[1] = "电源连接续航无限"
    elif battery_information[1] == psutil.POWER_TIME_UNKNOWN:
         battery_information[1] = "无法计算电池剩余续航时间"
    if battery_information[2] is None:
        battery_information[2] = "无法确定电源是否连接"
    elif battery_information[2]:    # 返回值为True
        battery_information[2] = "电源已连接"
    elif not battery_information[2]:
        battery_information[2] = "电源未连接"
    return battery_information

# 其他（系统启动时间、用户）
def get_sys_boot_timestamp(calculate=False):
    """获得系统启动时的时间戳（自1970年1月1日UTC以来的秒数）
    参数：
    mod ： 默认为False返回秒的时间戳，如果为True则会进行计算并返回本时区的日期
    """
    boot_timestamp = psutil.boot_time() # 获得系统启动时的时间戳
    if not calculate:
        return  boot_timestamp
    else:   # 获取系统启动时间的时间戳（秒），转换为可读的日期时间格式（本地时区）
        return datetime.fromtimestamp(boot_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def get_user_information():
    """获得计算机用户相关的信息
    name: 登录用户名。
    terminal: 用户登录的终端（如 tty1, pts/0，Windows 可能为 None）。
    host: 用户登录的主机（如远程 IP 或本地终端）。
    started: 用户登录时间的时间戳（秒级，Unix 时间戳）。
    pid: 用户登录会话的进程 ID（如 Linux 的登录进程 PID，Windows 可能为 None）
    """
    return psutil.users()

# 进程（Processes）
def hwnd_get_current_process_pid(return_class=False):
    """获得当前程序的PID
    参数：
    return_class ： 默认False即返回值是数值，如果为True则返回对象可以执行更多操作，如果关闭进程等等
    返回值：
    默认返回子进程的PID，如何return_class=Ture则返回子进程的对象
    """
    if return_class:
        return psutil.Process().pid
    else:
        current_process_pid = psutil.Process().pid
        return current_process_pid

def hwnd_get_pid(hwnd):
    """通过句柄获得进程的PID（windows专属，这调用的win32的库）
    注意：主进程创建的窗口则获得主进程的pid，子进程创建的窗口则获得子进程的pid
    参数:
    hwnd ： 窗口的句柄
    返回值：
    pid
    """
    tid,pid = GetWindowThreadProcessId(hwnd)    # 调用win32的api获取进程的PID，通过窗口句柄
    try:
        if psutil.pid_exists(pid):  # 判断进程是否有效
            return pid
        else:
            return None # 未找到该进程号
    except(psutil.NoSuchProcess, psutil.AccessDenied):
        return "进程可能已退出或无权限访问"

def hwnd_get_tid(hwnd):
    """通过句柄获得窗口的线程
    这个函数本来不应该在这里的
    注意：获得的线程ID和窗口的创建有关（如果是主进程的子线程创建的窗口，输入该窗口句柄后获得的是创建者子线程ID）
    """
    tid, pid = GetWindowThreadProcessId(hwnd)  # 调用win32的api获取进程的TID，通过窗口句柄
    return tid

def get_pid_name(pid):
    """获得进程的名字
    参数：
    pid ： 进程ID
    """
    return psutil.Process(pid).name()

def get_parent_pid(pid, recursive=True,return_class=False):
    """获得父进程的pid
    参数：
    pid ： 进程ID
    recursive ：默认为Ture递归获取所有父进程（包括父进程的父进程），如果为False则仅获取直接父进程
    return_class ： 默认False即返回值是数值，如果为True则返回对象可以执行更多操作，如果关闭进程等等
    返回值：
    默认返回父进程的PID，如何return_class=Ture则返回父进程的对象，当然也会报错
    """

    parent_process = list()   # 用来放父进程的等级和父进程的父进程
    try:
        father_process = psutil.Process(pid).parents()  # 把进程ID变为多个父进程的对象
        if father_process:  # 检测父进程是否存在
            for level, parent in enumerate(father_process, 1):
                parent_process.append(f"P{level}级父进程,PID:{parent.pid},名称：{parent.name()}")
        return parent_process

        father_process = psutil.Process(pid).ppid()  # 获得父进程PID
        if return_class:
            father_process = psutil.Process(father_process).parent() # 把进程ID变为对象
        return father_process
    except psutil.NoSuchProcess:
        print(f"进程 {pid} 不存在")
    except psutil.AccessDenied:
        print(f"无权限访问进程 {pid}")

def get_child_pid(pid, return_name=False):
    """获得当前进程下的所有子进程的pid（不包括子进程的子进程）
    参数：
    pid ： 进程ID
    return_name ： 默认False即仅仅返回pid，如果为True则返回pid和子进程的名字
    返回值：
    默认返回子进程的PID，如何return_class=Ture则返回子进程的对象
    """
    child_process_infos = list()    # 设置一个列表来放子进程的信息
    child_process = psutil.Process(pid).children(False) # 获得子进程PID，False不包括子进程的子进程
    if return_name:
        for child_process_infos in child_process:
            child_process_infos.append(f"子进程ID:{child_process_infos.pid},子进程名:{child_process_infos.name()}")   # 存放子进程的pid和名
    else:
        for child_process_infos in child_process:
            child_process_infos.append(child_process_infos.pid) # 存放子进程的pid
    return child_process_infos

def get_all_child_pid(pid):
    """获得所有子进程，包括子进程的子进程
    参数：
    pid ： 进程ID
    返回值：
    一个列表，无法显示层级，只能显示所有的子进程
    """
    all_child_process = list()  # 创建列表用来存放子进程的信息
    for child_process in psutil.Process(pid).children(True):  # 获得子进程PID,True是包括子进程的子进程
        all_child_process.append(child_process)
    return all_child_process

def pid_get_path(pid):
    """获得该进程的路径
    参数：
    pid ： 进程ID
    返回值是路径
    """
    return psutil.Process(pid).exe()

def is_running(pid):
    """检查当前进程列表中是否存在给定的 PID（如果PID被接替了依旧可以检测出来，即确保这个应用是真的消失了）
    直接使用 is_running() 更安全，因为它不仅检查 PID 是否存在，还确保该 PID 对应的是原始进程。
    参数：
    pid ： 进程ID
    返回值：
    存在则为True，不存在则为False
    """
    psutil.Process(pid).is_running()

def is_pid_exists(pid):
    """检查当前进程列表中是否存在给定的 PID（最快的）
    参数：
    pid ： 进程ID
    返回值：
    存在则为True（如果这个进程号被接替了还是显示True），不存在则为False
    """
    return psutil.pid_exists(pid)

def kill_pid(pid,check=True):
    """终止指定进程
    参数：
    pid ： 进程ID
    check ： True检查 PID有效性，防止误杀新进程，False则直接干掉这个进程
    返回值：
    终止成功返回True，失败为False
    """
    try:
        if check:   # 开启内置PID重用检查机制，确保操作的是原始目标进程
            psutil.Process(pid).terminate()
        elif not check:     # 无论是新的还是旧的都干掉
            psutil.Process(pid).kill()
    except():
        return False
    else:
        return True

def pause_process(pid):
    """暂停进程
    内置了 PID 重用检查 机制，确保操作的是原始目标进程（Windows 系统：暂停进程的所有线程）
    参数：
    pid ： 进程ID
    返回值：
    暂停成功返回True，失败为False(False是权限不够的问题)
    """
    try:
        psutil.Process(pid).suspend()  # 暂停进程
    except psutil.AccessDenied:
        return False

def restore_process(pid):
    """恢复被暂停的进程
    内置了 PID 重用检查 机制，确保操作的是原始目标进程（Windows 系统：暂停进程的所有线程）
    参数：
    pid ： 进程ID
    返回值：
    暂停恢复返回True，失败为False(False是权限不够的问题)
    """
    try:
        psutil.Process(pid).resume()  # 恢复被暂停的进程
    except psutil.AccessDenied:
        return False

def wait_process_die(pid,timeout=None):
    """等待进程结束
    内置了 PID 重用检查 机制，确保操作的是原始目标进程（Windows 系统：暂停进程的所有线程）
    参数：
    pid ： 进程ID
    timeout ： 默认None无限等待、可以自定义时间超时抛出异常
    timeout=0：非阻塞模式立即返回进程状态（若进程未终止则抛出异常）
    """
    psutil.Process(pid).wait(timeout)  # 等待进程结束

def get_pid_create_time(pid):
    """获得进程的创建时间
    参数：
    pid ： 进程ID
    """
    return datetime.fromtimestamp(psutil.Process(pid).create_time()).strftime("%Y-%m-%d %H:%M:%S")

def process_callback(process):
    """进程回调函数（为了下面的函数服务的）
    每当下面函数中有一个给定的进程结束时就会的调用此函数。
    当然，这个回调函数在这里只是为了测试而已
    """
    # print(f"进程：{process.name()}已经终止，进程ID：{process.pid}，进程状态：{process.status()}")
    print(f"进程：{process.pid}已经终止,状态：{process}，退出代码：{process.returncode}")

def monitor_process(procs,timeout=None,callback=process_callback):
    """用于等待一组进程终止，并返回已终止和仍在运行的进程列表。
    它特别适用于批量管理进程（如等待多个子进程退出），支持超时机制和回调函数，能有效监控进程生命周期。
    参数：
    procs   ：   要等待的 psutil.Process 对象列表
    timeout	：	最大等待时间（秒）。默认为 None（无限等待）
    callback：	回调函数，每当有进程终止时触发，参数为已终止的 Process 对象
    返回值（一下都是列表）：
    gone	已终止的进程列表（包含新属性 returncode 表示退出状态）
    alive	仍存活的进程列表（超时或未终止）。
    """
    # 把procs列表通过for给每个pid创建进程的实例对象再放回procs列表里面去
    procs = [psutil.Process(pid) for pid in procs]
    gone, alive = psutil.wait_procs(procs, timeout, callback)
    for process in gone:
        # print(f"进程：{process.name()}已经终止，进程ID：{process.pid}，进程状态：{process.status()}，退出码: {process.returncode}")
        print(f"进程：{process.pid}已经终止,状态：{process}，退出代码：{process.returncode}")
    if alive:
        print("以下进程超时后仍存活:")
        for process in alive:
            print(f"PID: {process.status()}")
        # 可选：强制终止存活进程
        for process in alive:
            process.kill()
        # 再次等待确保终止
        # gone, alive = psutil.wait_procs(alive, timeout=1)
    # return
    # 核心使用场景
    # 批量等待进程退出
    # 等待一组进程正常终止，或超时后强制终止剩余进程。
    # 实时监控进程状态
    # 通过回调函数实时处理进程退出事件（如日志记录）。
    # 资源回收
    # 确保子进程退出后释放资源（如临时文件、网络连接）。

# get_all_pid_attribute_super 这个是最全的，遍历所有进程的属性（属性自定义）
def get_all_pid_attribute_super(attrs=None,ad_value=None):
    """遍历系统中所有正在运行的进程。相较于手动遍历 PID 列表，此方法更高效且避免竞态条件（如进程中途退出导致的错误）
    这个可以包括所有的进程相关的操作，可以说是进程里面最强最有效的操作，不过得去官网看类
    参数：
    attrs ： 通过 attrs 参数指定需要预加载的属性，减少多次系统调用
    如果attrs为None，则默认attrs=["pid", "name", "status"]
    ad_value : 设置当进程某个属性无法获取时的值（如权限不足），默认为None，
    返回值：
    默认pid（进程ID），name（进程名），status（进程当前状态），started（进程开始时间）
    """
    psutil.process_iter.cache_clear()  # 手动清除进程列表缓存以确保获取最新数据(爆黄不用管的，能用的啊)
    count_process_information = list()    # 设置一个列表用来统计放置不同进程的信息
    for process_information in psutil.process_iter(attrs, ad_value):
        try:
            count_process_information.append(process_information)
        except(psutil.NoSuchProcess, psutil.AccessDenied):
            count_process_information.append("进程可能已退出或无权限访问")
    return count_process_information

def get_all_active_pid():
    """获得所有当前正在运行的 PID 的排序列表
    返回值 ：  正在运行的PID 排序的列表
    """
    return psutil.pids()

def get_all_active_pid_name(return_value="set"):
    """获得当前所有进程的名字
    参数：
    return_value ： 默认"set"即如果有多个进程同个名字则自动去重
    如果为"list"则返回所有的进程名包括重名（子进程可能重名）
    返回值：
    return_value为"set"时如果其中有一个进程退出或无权限访问，则集合中就有“进程可能已退出或无权限访问”
    return_value为"list"为所有进程都返回，可以看到多个无权访问的进程
    """
    if return_value == "set":    # 返回值以集合形式返回
        all_active_pid_name = set()  # 创建一个集合来放置所有进程的名字
    elif return_value == "list":  # 返回值以列表形式返回
        all_active_pid_name = list()  # 创建一个集合来放置所有进程的名字
    else: raise TypeError("参数类型错误，只能填 'list'、'set'(字符串)")
    # 开始遍历所有正在活动进程
    for pid in psutil.process_iter():
        try:
            all_active_pid_name.add(pid.name())
        except(psutil.NoSuchProcess, psutil.AccessDenied):
            all_active_pid_name.add("进程可能已退出或无权限访问")
    return all_active_pid_name

def get_pid_cmdline(pid):
    """获得此进程作为字符串列表调用的命令行。
    参数：
    pid ： 进程ID
    返回值：    字典
    """
    return  psutil.Process(pid).cmdline()

def get_pid_environment(pid):
    """获得进程的环境变量
    参数：
    pid ： 进程ID
    返回值：    字典
    """
    return  psutil.Process(pid).environ()

def get_pid_status(pid):
    """获得进程的状态
        参数：
        pid ： 进程ID
        """
    return psutil.Process(pid).status()

def get_pid_cwd(pid):
    """获得进程将当前工作目录作为绝对路径进行处理
        参数：
        pid ： 进程ID
        """
    return psutil.Process(pid).cwd()

def get_or_set_pid_priority(pid, value=None):
    """设置或获取进程的优先级
    参数:
    pid ： 进程ID
    value : 默认None即获取进程优先级，如果value=1则设置进程优先级为1级
    """
    return psutil.Process(pid).nice(value)

def get_or_set_pid_io_priority(pid, value=None):
    """获取或设置进程 I/O 友好度 （优先级）如果未提供任何参数，则它为获得模式
    参数:
    pid ： 进程ID
    value : 默认None即获取进程 I/O优先级，如果value=1则设置进程 I/O优先级为1级
    """
    return psutil.Process(pid).ionice(None, value)

def get_pid_cpu_percent(pid):
    """获得该进程对cup的占比
    参数:
    pid ： 进程ID
    """
    return psutil.Process(pid).cpu_percent()

def get_pid_memory_percent(pid):
    """获得该进程对内存的占比
    参数:
    pid ： 进程ID
    """
    # RSS (Resident Set Size)表示进程实际使用的物理内存（不包括交换分区）
    return psutil.Process(pid).memory_percent(memtype='rss')

def get_cpu_num(pid):
    """获得该进程当前正在哪个CPU上运行(Linux、FreeBSD、SunOS可用，windows不支持)
    参数:
    pid ： 进程ID
    """
    return psutil.Process(pid).cpu_num()
"""
uids()
此进程的真实、有效和保存的用户 ID 作为命名元组。 这与 os.getresuid 相同，但可用于任何进程 PID。
gids()
此进程的真实、有效和保存的组 ID 作为命名元组。 这与 os.getresgid 相同，但可用于任何进程 PID。
terminal()
与此进程关联的终端（如果有），否则 。这是 类似于 “tty” 命令，但可用于任何进程 PID
"""
if __name__ == '__main__':
    print(get_cpu_times())
    # psutil.cpu_percent(1)  # 首次调用非阻塞模式，把无效数值使用掉
    # while True:
    #     print(f"CPU利用率：{get_cpu_utilization()}%")
    #     sleep(1)
    # psutil.cpu_times_percent() # 如果不填初次输出可能为全 0.0，先调用一次
    # while True:
    #     print(get_cpu_times_percent())
        # sleep(1)
    print(get_cpu_count())
    print(get_cup_stats())
    print(get_cup_frequency())
    # print(get_average_system_load())
    print(get_virtual_memory())
    print(get_swap_memory())
    print(get_disk_information())
    print(get_disk_usage("/"))  # /为所有磁盘的使用率
    # print(get_disk_io_count())
    print(get_net_io_count())
    # print(get_net_connections())
    # print(get_net_if_address())
    # print(get_net_if_stats())
    # print(get_hardware_temperature()) windows系统不能用这个函数。Linux等可以用
    # print(restore_fans())   # 只有Linux可以用
    print(get_battery_information())
    print(get_sys_boot_timestamp(True))
    print(get_user_information())
    """进程"""
    print(f"当前窗口的进程是{hwnd_get_current_process_pid()}")  # 进程会不断改变
    # print(f"窗口PID：{hwnd_get_pid(6555674)}")
    # print(f"窗口TID：{hwnd_get_tid(6555674)}")
    # print(get_pid_name(5008))
    # print(pid_get_path(5008))
    # print(get_parent_pid(0))
    # print(get_child_pid(5008))
    # print(is_pid_exists(4))
    # print(get_pid_create_time(5008))

    # for process in get_all_pid_attribute_super():
    #     print(process)
    # print(get_pid_list())   # len(get_pid_list())：统计总共多少个进程
    # print(get_all_active_pid_name())

    # print(monitor_process(procs=[6428]))    # notepad，记事本方便

    # print(get_pid_cmdline(5008))
    # print(get_pid_environment(5008))

    print(get_cpu_num(14128))



