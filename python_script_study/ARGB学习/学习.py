# pip3 install openrgb-python
# python调用文档链接
# https://openrgb-python.readthedocs.io/en/latest/

# 实例化对象
from openrgb import OpenRGBClient
cli = OpenRGBClient()
# 只要您控制本地 OpenRGB SDK，使用默认的 port 的 port 中，并且不想更改名称。如果不是这种情况，则有一个 更多选择。
# cli = OpenRGBClient('192.168.1.111', 8000, 'My client!')

from openrgb.utils import DeviceType

mobo = cli.get_devices_by_type(DeviceType.MOTHERBOARD)[0]


# 如果您有多个特定类型的设备，则可以尝试筛选 按设备的元数据、名称或任何其他属性。另一个选项是按名称选择设备。
corsair_thing = cli.get_devices_by_name('Corsair Lighting Node Pro')[0]
# 或者更确切地说
cooler = cli.get_devices_by_name('wraith prism', False)[0]
# 实际名称是 'AMD Wraith Prism'

# 颜色由 RGBColor 对象处理。它可以从 RGB、HSV 甚至十六进制颜色值。
from openrgb.utils import RGBColor
red = RGBColor(255, 0, 0)
blue = RGBColor.fromHSV(240, 100, 100)
green = RGBColor.fromHEX('#00ff00') # #符号不是必需的，它通常附加到十六进制颜色

# 要将 RGBObject 设置为 纯色，请使用  set_color 该函数。
mobo.set_color(RGBColor(0, 255, 0))
cli.devices[0].set_color(red)
cli.devices[1].zones[0].set_color(blue)
# 警告
# 多次与同一设备的 SDK 交互（设置颜色、更改模式、调整区域大小等），而两者之间没有某种延迟，可能会导致未定义的行为。

# 如果要将 RGBContainer 设置为多种颜色，请使用 set_colors 该函数。此示例假定 主板有 8 个 LED，并将它们设置为红色、蓝色、红色、蓝色......模式。
mobo.set_colors([red, blue]*4)

# 虽然这些方法可用于自定义效果等作，但它需要 多花点精力让它足够快地工作（参见 优化速度）。效果控制流程变得更加容易 用于需要快速更改的效果。
# 这两种方法都只能用于设置对象的一部分。例如 对于具有 8 个 LED 的主板，这会将中间的 4 个设置为红色。
mobo.set_color(red, 2, 6)

# 设备的模式可以在 ModeData 下以对象的形式找到。可以通过 Device.modes 该功能为设备设置模式。模式可以通过 index、name 或 您可以传入 actual mode 对象。
mobo.set_mode(3)
mobo.set_mode('direct')
mobo.set_mode(mobo.modes[2])

# 保存模式
# 某些设备支持保存其模式，以便在您关闭设备电源时， 当它再次开机时，它会记住自己的状态。
mobo.set_mode(3, save=True)
mobo.save_mode()
# 第一个选项会设置一个模式然后保存它，而专用功能只是 保存当前模式的任何内容。

# 调整区域大小
# 如果您的设备具有 ARGB 区域，则可能需要 在某个时候调整它的大小。
mobo.zones[0].resize(35) # 对于具有 35 个 LED 的区域

# 使用配置文件
# OpenRGB 的配置文件是一种在设置 一切都完全按照你的意愿进行，并且能够轻松加载该状态。 现有用户档案存储在profiles 的属性中。要保存配置文件，请先配置 按照您想要的方式进行 RGB 设置，然后运行
cli.save_profile('perfection') #保存到名为 “perfection” 的新配置文件或现有配置文件
cli.save_profile(0) # 覆盖列表中的第一个配置文件
# 加载配置文件同样简单。
cli.load_profile('perfection') # 查找并加载名为 perfection 的配置文件
cli.load_profile(0) # 加载列表中的第一个配置文件
# 如果需要，您还可以删除配置文件。
cli.delete_profile('perfection') # 删除名为 perfection 的配置文件
cli.delete_profile(0) # 删除列表中的第一个配置文件

# 如果您从 OpenRGB 创建了新的配置文件，并希望确保您的客户端可以 看到它，您可以使用cli.update_profiles该函数从服务器获取最新的配置文件列表

# 旧配置文件系统
# 有两种方法可以使用配置文件：本地和远程。 旧方法（本地）将配置文件保存到本地文件。较新的， 推荐的方法是远程。
# 远程保存配置文件只是告诉服务器 将其当前状态保存到配置文件中，方法与按 OpenRGB GUI 上的 “Save Profile” 按钮。
# 如果您仍想在本地存储 配置文件，您可以使用额外的参数来实现。
cli.save_profile('perfection', True) # 在本地保存配置文件

# 在本地保存配置文件会将名为 perfection.orp 的文件保存在 OpenRGB 的 config 目录，因此您可以直接从 OpenRGB 的 profile 列表。
#
# 在 OpenRGB-Python 中加载配置文件与保存它们一样简单。
# 这 功能会将您的灯光设置为与保存时相同。
# 它可以加载从 OpenRGB 本身或 OpenRGB-Python 保存的配置文件。
cli.load_profile('perfection', True) # 加载本地配置文件

# 警告
# 我只知道 OpenRGB 的配置目录在 linux 上的位置，我不知道 测试了在 Windows 上保存配置文件。
# 默认目录 OpenRGB-Python 保存配置文件是 。如果你知道 OpenRGB 的 config 目录在 Windows 上的位置以及如何可靠地找到它 从 python 中，
# 请提交 pr 或在 OpenRGB 的 discord 上与我交谈 服务器。同时，您可能必须手动指定 目录中，以便使用参数保存或加载配置文件。
# ~/.config/OpenRGBdirectory