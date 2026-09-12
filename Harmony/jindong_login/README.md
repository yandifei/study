# 简单介绍
jindong_login是对应黑马的`38-【阶段综合】-京东登录`这个内容
因为涉及到多个图片等资源所以这里单独拉出一个项目来写
目的是放置前面写的代码搞得很乱

## 布局容器+顶部+Logo
思路分析：
1. 布局容器：整体从上往下-Column
2. 布局背景：backgroundImage
3. 顶部：左右布局-Row、SpaceBetween
4. Logo：Image图片


## 输入框和登录区域
思路分析：
1. 国家地址：点按区域（Row→Text、Text、Image）
2. 手机号：输入框TextInput
3. 同意许可：复选框Checkbox，文本Text→Span
4. 登录按钮、用户注册

## 底部模块区域
思路分析：
1. 整体Column列
2. 标题：Text
3. 三方登录图标： Row→Image，SpaceAround
4. 底部居底：Blank()填充组件 

# 注意事项
我这里使用的图片等资源不是去黑马那边找的，仅仅是我自己从京东官网`https://www.jd.com/`爬的，所有有些图片等资源显示得和视频不同是正常的。

logo:
https://m.360buyimg.com/babel/jfs/t20280615/318148/22/9216/14627/684fdc85Fa154b4e0/0742847dfed41e81.png

默认头像(default_avatar)
https://img12.360buyimg.com/img/jfs/t1/293477/4/11778/9184/683ff418Fa597c987/651a589861eaae88.png


微信图标，微信4.0版本之后我没法直接找到他的资源图片，逆向exe去找找太麻烦了，所以这里直接搬app store中微信的图片了
https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/ea/eb/fa/eaebfa21-573f-1593-59d1-b5f781892e0c/AppIcon-0-0-1x_U007epad-0-6-0-sRGB-0-85-220.png/434x0w.webp

QQ图标本地有直接用

华为小图标
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAA6lBMVEVHcEzEICHfR0HfTEXph3bof2/VGBrbKyjeQzzgUUjrlYLsnYjWFxjhVUvWTEXvrZXnd2nrj33ph3a/GRy8GRzdPDbnfG27HB+xGx66Gh22Gh3ZHh7gUknne2uxGx60Gx7CGRvQFxneQjviXFLkZlrHGBrPGxzHGBrOGBnTHx/TJSTcNTGvGx66Gh2fHSHIGBu/Ghw0CAqrHB+ZHSKnHCCaHSKiHCGbHSKoHCC2Gh2jHCCqHCCXHiMEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAAEAAB3b9N9AAAATnRSTlMAIINRNI55///lsf///xf/YP+9/1H/vFvk/0f/m/8p/9v/vnP//2yOnsU75sO3/+TxDTb+/3aRuaeqz9PZxVd6py1FH5yD4WFs8or/l7N5GIk3AAABkUlEQVR4AaTNVYKDMBRA0VfFQiqBCVLDNdSd/a9rHuOu9ydyIvDDWu0OQLfX/cj6kqwAqJqmfnCPSLJOQRsMtOEbwYsNDukIcYwbL4wZDZp6uzvCboDK/Aktm4FDXFOeDKdYDxRTgodmc5stwMOrfhBidCJLbv8BOWIUJ8SV/Lau6wo1JZekTzcbbXnEzdqmaeYFmhfDQyUiE4lHsr4kZbFLiBc9UMVBNOpEXtYnJEfylpCvHLR1VVkbjrrkkYi9NPU8L6EZsw3AtlW1K2fCZsYi5VEripabhDF73mpwv612u91hY9k0MQzBOEey5yXcdWzu7uYOd/CTZLawkeYWPLQ5nDDB7+bijJ04PLY/HA6n48UAbFaK0wnXT7jZbvHlDdxFrztsD0+1jvWLlXO5OPDfbvsSawMGYCAG3kruzTLD/uOE6zwIjcMHH4gJl1PEKZXaWh/+XU4TVl+4pObY7HBy7GL1d7lvq+9SN0wVN1oj3vErJ/1oh21mOFcbd7mx5jUAMkpomBfi304k71MSf+cJdRhBl74wauYAAAAASUVORK5CYII=

微博的logo（给他转成png才能用）
https://h5.sinaimg.cn/m/weibo-lite/img/pwalogo.417d1674.svg

右边和关闭图标（鸿蒙官网自己的）
https://developer.huawei.com/consumer/cn/design/harmonyos-symbol/

# 鸿蒙图标原生网址
https://developer.huawei.com/consumer/cn/design/harmonyos-symbol/


