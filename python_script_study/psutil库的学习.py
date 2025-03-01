from datetime import datetime
from time import sleep
import psutil

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
def get_pid_list():
    """获得当前正在运行的 PID 的排序列表
    返回值 ：  正在运行的PID 排序的列表
    """
    return psutil.pids()

def get_pid_list_ex():
    """遍历系统中所有正在运行的进程。相较于手动遍历 PID 列表，此方法更高效且避免竞态条件（如进程中途退出导致的错误）
    

    """

    count_process_information = list()    # 设置一个列表用来统计放置不同进程的信息
    for process_information in psutil.process_iter():
        count_process_information.append(f"进程ID：{process_information.pid}，进程名：{process_information.name()}，进程状态：{process_information.status()}")
    return count_process_information

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
    print(get_pid_list())   # len(get_pid_list())：统计总共多少个进程
    for i in get_pid_list_ex():
        print(i)




