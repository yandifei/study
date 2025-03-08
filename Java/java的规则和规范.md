# 规则和规范的差别
# 规则：
规则必须遵守，规范可以不遵守
不能使用关键字和保留字
关键字：已经被java使用了，就是java自带的，如：（public、static、class）
保留字：现有Java版本尚未使用，但以后版本可能会作为关键字使用。如：goto
byValue、cast、future、 generic, inner、 operator、 outer、 rest、 var、goto 、const

虽然不能使用关键字和保留字，但是可以包含关键字和保留字，如：aclass
java严格区分大小写，无长度限制(200个字符就是有大病了)
标识符不能包含空格，如：int a b = 10;
命名和其它语言不同的就是java多了个`$ `这个符号是合法的以前都是只有_才合法，java有`_`、`$` 符号
# 规范：
为了更加专业
1. 包名:多单词组成时所有字母都小写:aaa.bbb.ccc //比如 com.hsp.crm
2. 类名、接口名:多单词组成时，所有单词的首字母大写:XxxYyyZ22。比如:TankShotGame【大驼峰】
3. 变量名、方法名:多单词组成时，第一个单词首字母小写，第二个单词开始每个单词首字母大写:xxxYyyZzz，比如:tankShotGame【小驼峰、驼峰】
4. 常量名:所有字母都大写。多单词时每个单词用下划线连接:XXXYYYZZZ。比如:定义一个所得税率 TAX RATE
5. 后面我们学习到 类，包，接口，等时，我们的命名规范要这样遵守,更加详细的看文档。
