<center>
    <h1>
        鸿蒙数据爬虫
    </h1>
</center>

# 原则(每次开DevEco Studio看一遍)
- 原型开发
  - 基于自己python的P站排行榜爬虫转到鸿蒙里面去
  - 基于老师的代码、文档进行二次改进或开发（核心）
- 优先追求核心功能，功能开发完成前没有必要上`奇技淫巧`
- 优化先滚一边去（赶时间2025.12.22 17:09）
- 文档别写太好，记录要点就行，没必要把软件工程或其他开发的全套流程搬过来，**Real developers ship.**

# 需求建模
- 应用图标和应用名字要改
-  2个界面
   1. 插画主界面
   2. 登陆界面
- 能滚动看插画内容，能按照排行来看
- 能进行登陆后看屏蔽内容
- 数据本地存储(仅存cookies，用sqlite)
- 命名遵守编程规范

## 插画主界面
图片
排名
作者
图片名称
# 优化
P站要VPN，所以除非我是使用代理网址否则正常是不能跑这个应用的。
程序启动做一个检测是否能连通P站（启动的生命周期使用）

# 数据
https://www.pixiv.net/
https://www.pixiv.net/favicon20250122.ico

# 开发随笔
改兔图标和名称
B:\study\Harmony\personal_research\entry\src\main\module.json5（这个文件才有效）
B:\study\Harmony\personal_research\AppScope\app.json5（这个文件改无效）
反正都改了就行，鬼记触发条件

构建数据模型->反序列化和序列化,数据模型仅构建需要用到的就行，用不到的放一边

我靠构建完基础的http请求了，但是我忘了加权限，笑了

哈哈哈，python用BeautifulSoup实现，鸿蒙我得搞正则了，早知道就给自己挖坑了
```python
soup = BeautifulSoup(responds.text, "lxml") # 解析整个DOM
json = json.loads(soup.find("script", id="__NEXT_DATA__").text)
print(f"目前排行榜共有{len(json["props"]["pageProps"]["assign"]["contents"])}张图片")
```

涉及到联合请求我这里必须对request进行封装，反正都是get(仅适用pixiv)
```
function request(url: string, callback_function: Function) {
  httpRequest.request(
    url, // 请求URL
    {
      method: http.RequestMethod.GET, // 请求方法：GET
      header: { // 请求头（模拟浏览器请求，我这里就极致参数，其他默认）
        // 用户代理（身份用我windows的chrome模拟）
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        // 伪装请求来自合法来源（这个关键）
        "referer": "https://www.pixiv.net"
      }
    },
    // 请求回调函数
    (err, response) => {
      // 调用回调函数处理结果
      callback_function(err, response)
      // 在请求完成后销毁实例
      httpRequest.destroy();
    }
  );
}
```

当数据太大时，控制台输出其实是不完整的，处理方式：当数据超过1000字符时，只显示开头500字符和结尾500字符。

对于返回的json直接不做校验，解析为对象也不做异常捕获，没有必要，对于vue框架来说头部一般不改。
但是在ts中必须对正则匹配返回的数据做校验是否存在不然报错

网络请求读写资源耗尽问题
![alt text](image.png)
https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V14/js-apis-http-V14?utm_source=chatgpt.com
![alt text](image-1.png)

换个流式吧