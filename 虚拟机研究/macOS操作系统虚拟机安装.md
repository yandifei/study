# <center>macOS操作系统虚拟机配置</center>
文档声明：使用的都是2025.3.15这个日期找到的最新的版本，电脑版本是win11（其他版本或系统都可以，这里侧重思路分析）
***其实就2个步骤：ios镜像文件和VM配置解锁***
这两个步骤没有先后关系
## 准备好IOS的镜像文件
macOS的博客文章：https://blog.csdn.net/molangmolang/article/details/136539553?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522dd964f3e3117b29c25f0468d4255da32%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=dd964f3e3117b29c25f0468d4255da32&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-2-136539553-null-null.142^v102^pc_search_result_base5&utm_term=macOS&spm=1018.2226.3001.4187
macOS下载网址，因为官方是没有提供镜像文件，所以都是别人收录的
https://pan.baidu.com/s/1_AHtQuyf8QxNz6Jq3CWy0w?（这里拿到的是pkg文件）
AMD和英伟达cpu都有详细讲解
【windows虚拟机一键安装苹果系统macos，轻松拥有xcode环境】https://www.bilibili.com/video/BV1hq4y1v73x?vd_source=298465310cd98e6ceddf1afe7d72e7ec

英伟达cpu详细
【在Windows下30分钟体验2024最新苹果系统，vmware虚拟机安装macOS Sequoia 15红杉树】https://www.bilibili.com/video/BV1PtynYHE13?vd_source=298465310cd98e6ceddf1afe7d72e7ec
macOS15(这里拿到的就直接是iso镜像文件):
夸克网盘:https://pan.quark.cn/s/a8c47dc4fea4
百度网盘:https://pan.baidu.com/share/init?surl=-Ix9lVnRiUrB75GyA5Te9A&pwd=85v1

镜像链接：
**黑苹果动力（这个看着好牛比，网址里面有教程）：https://www.mfpud.com/macos/raw/**
1.苹果官网镜像:https://support.apple.com/zh-cn/HT211683
2.苹果系统之家：https://macoshome.com/macos (仅有iso文件)
3.MAC下载吧:https://macxzb.com/macos （百度网盘iso要登录，有pkg和dmg）
4.HackTiny:https://www.hacktiny.com/macos （原版引导镜像）
5.pc6下载站:https://www.pc6.com/pc/osxtjx/ （打不开）
6.小黑豆:https://xiazai.winheidou.com/MacOsDownload/（360导航）


## 配置好VM虚拟机
如果是用VMware虚拟机的话打开任务管理器，查看cpu有没有打开虚拟化，如果cpu没有虚拟化就去B站，百度，AI（deepseek）找办法吧。其实我看到有一些视频讲到仅仅intel（英特尔）的CPU才能用macOS，其实AMD也是可以的（12AMD是可以的，13以后就太卡了，许多功能都无法实现），具体我没AMD卡去实践（不过我想很快就有机会实践了）macOS15是16GB，确保空间够大。

VMware 官方并不直接提供对macOS作为虚拟机客户操作系统的合法支持，苹果的最终用户许可协议（EULA）明确限制macOS仅能在苹果硬件上运行，因此在非苹果设备或虚拟机中运行macOS可能违反协议

我这里使用工具绕过限制（解锁虚拟机中macos的选项）：https://github.com/DrDonk/unlocker/releases
用的VM17版版本，其实其他VM版本都是一个套路，关掉虚拟机的服务后使用解锁工具，我这个版本就是直接解锁也没有关掉虚拟机的其他服务
1. 首先从https://github.com/DrDonk/unlocker/releases 下载好工具，为了方便，我就直接把他的发布版压缩包下载链接搬过来了：https://github.com/DrDonk/unlocker/releases/download/v4.2.7/unlocker427.tgz 下载慢或者打不开链接的话就直接在https://github.moeyy.xyz/ 这个网址里面输入https://github.com/DrDonk/unlocker/releases/download/v4.2.7/unlocker427.tgz 加速下载
2. 下载之后要解压出来，解压完之后直接去windows文件夹（如果自己是其他系统就对着来就ok了），解压之后确保你已经关闭了所有的虚拟机（为了不影响下一个步骤）
3. 我直接在windows文件夹下双击unlock.exe这个程序，出现一个黑框框（控制台）后等待出现`Press Enter key to continue...`后按下回车按键再打开虚拟机。
4. 点击新建虚拟机——>点击下一步——>点击稍后安装操作系统——>点击下一步，到了这一步就可以看到有Apple macOs(M)这个选项了
5. 选择下载好的镜像，我这里下载的镜像就是macOS15和macOS15版本，macOS14是pkg文件，macOS15是iso镜像文件，那我就选14版本的了（需要点击查看所有文件，还得去设置里面CD/DVD(STAT)选择ISO镜像文件，如果是pkg记得点所有文件才能看到pkg）
6. 再启动虚拟机安装之前必须打开虚拟机所在文件夹，修改vmx文件，将 ethernet0.virtualDev = "e1000e"改为 ethernet0.virtualDev = "vmxnet3"。这个操作时为了联网，从macOS14开始安装前就要求你必须联网，之前的版本（13、12、11）没有这个要求（安装完后再练网）
这一步修改超级麻烦（对应有AMD和因特尔的，看我给的B站链接，没有成功大多数都凉在这一步，挨个去试）
   1. 具体修改步骤：
   2. 选中macOS虚拟机，右键后选中点击`打开虚拟机目录`，找到以`.vmx`为后缀的目录
   3. 右击文本打开
   4. 往下找到`ethernet0.virtualDev`如果是`ethernet0.virtualDev = "vmxnet3"`就不用修改了，如果不是就把这一行改成这样,**我的VM17没改，默认改好了**

1. 接下来就是正常安装系统就行，不会的可以B站搜索，这就跟你买到mac电脑后第一次使用的情况一样了（自己安装系统）
   1. 虚拟机启动macOS系统后会有4个图标选项（从时间机器恢复、安装macOS （英文，每个人都可能不同）、Safari浏览器、磁盘工具）
   2. 点击`磁盘工具`选中`VMware Virtual SATA Head Drive MEdia`我的这个选项在最左上角，然后点击抹掉，这时会有个重命名，磁盘名称自定义（我这里改为macOS，强烈建议英文，中文不知道有什么bug），格式和方案都不动。改完之后点击完成，点击左上角红色按键返回到4个选项的界面
   3. 选`安装macOS`-->点击继续-->点击同意（同意条款）-->选中上一个步骤分配好的磁盘-->点击继续-->等待macOS在这个系统上的安装（中间有多次重启是正常的情况）
2. 分好盘和创建好账户之后就得安装VM tool了，系统启动后界面没有加载出来很正常（macOS在虚拟机里面很卡），看到白色一片的桌面不用慌
3.  虚拟机里面安装VM tool可以解决卡顿、分辨路缩放的问题，自己去B找安装教程，如果是缩放分辨率没问题那就是已经安装成功了，没有安装就直接进入macOS系统后点击VMware Workstation的`虚拟机`选项就可以看到`安装VM tool`这个选项了，我看其他up都好麻烦，如果是其他VM版本或许还真的是麻烦
4.  可以自己去调整内核大小和内存大小来调高体验
**如果打不开虚拟机，在自定义硬件那里调整cpu和内存的参数（我给了8GB的内存，1核4处理器），直接走iso通道，没有自定义后选iso**

## 卡顿方法解决
根本原因：这个苹果系统是无法直接通显卡，所以全是cpu模拟的，CPU压力大就卡顿了
### 方法一：
 虚拟机里面安装VM tool，直接进入macOS系统后点击VMware Workstation的`虚拟机`选项就可以看到`安装VM tool`这个选项了，我看其他up都好麻烦，如果是其他VM版本或许还真的是麻烦

### 方法二：
1.ios虚拟机关机
2.选择虚拟机右键设置
3.点击显示器
4.勾选3d图形加速
5.勾选指定监视器设置
6.分辨率调低
7.缩放比例调节自由拉伸
### 方法三：
虚拟机换成了keal oS，这个系统镜像支持AMD和Intel平台
kealos 10.15 Catalina：https://cloud.mfpud.com/mfpud/macOS/cdr/Catalina/macOS%20Catalina%2010.15.4%20VMimg%20KealOS.iso
其实也可以切换低级版本的macOS，因为我这个15版本都16GB了，macOS 10.15（Catalina）这个是10GB之内的
### 方法四：
把虚拟机和镜像放到固态硬盘里面去，因为是cpu模拟，IO流数据量大，所以如果虚拟机和镜像在机器硬盘里面的话就放到固态硬盘更好
### 方法五：
增加内存和处理器内核数量
macOS虚拟机-->设置-->硬件-->内存-->根据情况自己调大（我的是8192MB=8GB）-->处理器-->每个处理器的内核数量（我调成了4，其实我可以调为6或8）
减小消耗（减轻负担）
macOS虚拟机-->设置-->选项-->高级-->收集调试信息（选择无）-->打开禁用内存页面修整-->关闭定期记录虚拟机进度
### 方法六：
新建虚拟机的时候选择`将虚拟磁盘存储为单个文件`，如果是U盘经常移动就放弃这个方法选择`将虚拟磁盘拆分成多个文件`
### mcaOS里面的设置：
#### 方法一：

