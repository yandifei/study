# <center>Hyper-v虚拟机研究</center>

- 虚拟机目前主流是VM和Hyper-V，学习和大多企业一般都是VM
- 两者架构不同，Hyper-V仅能在windows11或10的企业版和专业版使用（家庭版需要脚本破解限制）
## 选择原因
我的VM配置了乌班图、kali、CentOS6、macOS15、Windows11Pro系统，但是某些系统使用效果确实不好
1. VM的macOS15直接给我卡死了，没有显卡直通，VM使用CPU的虚拟化技术模拟GPU，使用CPU渲染，这也导致了他的卡顿爆了。（仅仅在macOS系统）
2. 神奇的是我创建win11的虚拟机直接给我卡死了，和我宿主机一样的系统一样的版本，但是效果确实不同，超级卡顿（我已经分配了80%的资源给虚拟机了）
3. Hyper-V和VM在性能上最大差别就是硬件资源调度方式
   1. Hyper-V是直接调度电脑硬件的资源。在资源调度上，毋庸置疑Hyper-V比VM强太多了。
   2. VM使用的是完全虚拟化技术，在新建虚拟机后用户是不能直接在虚拟机里面调用硬件资源，需要VM中间过度(优点就是节约资源，但是相对与Hyper-V资源调度的速度就慢了)
   3. macOS的法律规定不能逆向也不能在非苹果产品使用这个系统，这也导致了VM没有合适的GPU驱动去供VM使用。(没人敢开发给大家使用)
4. Hyper-V确实可以很好的兼容windows
## 缺点
1. 但是因为环境必须是windows10或11版本。
2. 如果不是专业版或企业版必须要使用脚本开启
3. VM有桥接联网方便，但是Hyper-V还要自己配置网络适配器
4. 后台会有一个Hyper-V的服务占用后台资源，如果不开虚拟机的话得手动关闭，我觉得超级麻烦(笔记本比之前耗电更快是真的)

## 开启使用
- 不同于其他软件，这个软件已经安装好了，只是需要激活。所以他不是在网站上下载下来
首先确保系统是Windows11或10
确保开启了CPU虚拟化技术
1. ctrl + shift + esc 打开资源管理器
2. 点到CPU查看右下角是否开启虚拟化
3. 如果没有开启进入BIOS开启
### 家庭版（专业版或企业版跳过）
win + R 输入cmd，在终端输入以下指令。共有5条指令，一条一条输入执行
```shell
pushd "%~dp0"
dir /b %SystemRoot%\servicing\Packages\*Hyper-V*.mum >hyper-v.txt
for /f %%i in ('findstr /i . hyper-v.txt 2^>nul') do dism /online /norestart /add-package:"%SystemRoot%\servicing\Packages\%%i"
del hyper-v.txt
Dism /online /enable-feature /featurename:Microsoft-Hyper-V-All /LimitAccess /ALL
```
### 激活Hyper-V
在控制面板里找到软件->服务->Hyper-v虚拟->等待运行库安装完成
桌面直接点开就行了
虚拟机创建完后记得开证书认证（不然没法开虚拟机）
