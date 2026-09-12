/*数组的操作
主要针对数组中的数据进行查找、修改、增加或删除

操作              语法
查找              数组名[下标]、数组名.length
修改              数组名[下标]=新值
增加              数组名.push(数据1,数据2,...)、数组名.unshift(数据1,数据2,...)
删除              数组名.pop()、数组名.shift()
任意位置增加或删除   数组名.splice(操作的起始位置，删除的个数，新增1,新增2,·..)
 */


/*  查找&修改
查找：数组名[下标]
修改：数组名[下标]=新值
数组长度：数组名.length
*/
//1.定义一个数组
let names: string[] = ["刘小备", "吕小布", "张大飞"]
console.log("names数组", names)

//2.数组取值（通过下标）
console.log("数组取值", names[1])
console.log("数组长度", names.length)

// 3.数组修改（通过下标）
names[2]= "赵云"
console.log('修改数组', names)


/* 增加数组元素
往开头加：数组名.unshift(数据1,数据2,数据3,..)
结尾添加：数组名.push(数据1,数据2,数据3，.)
*/
//定义一个数组
let songs: string[] = ["告白气球","洋葱", "吻别"]

// 添加
// 1. 往开头新增 unshift(新增的值) 添加完成后还会返回操作后的数组长度
songs.unshift("彩虹")
console.log("返回数组的长度", songs.unshift("七里香"))
console.log("数组songs", songs)

// 2.往结尾新增push(新增的值）
songs.push("光辉岁月", "海阔天空")
console.log("数组", songs)



/*删除数组元素
从开头删：数组名.shift()
从结尾删：数组名.pop()
*/
// 删除
// 1.从开头删shift
// songs.shift()
console.log("返回删除的项", songs.shift())
console.log("数组", songs)
//2.从结尾删pop(这里和python一样都是pop后返回删除的值)
console.log("返回删除的项", songs.pop())
console.log("数组", songs)

//开头相关的都是shift
// 开头(S): unshift shift
// P在键盘上是后尾所以删都是后面，可以这么记
// 结尾(P): push    pop


/*任意位置添加/删除数组元素
语法：数组名.splice（起始位置，删除的个数，新增元素1，新增元素2，······）、
*/
//定义一个数组
let songs1: string[] = ["告白气球", "洋葱", "吻别", "双节棍", "曹操"]
//splice在任意位置进行删除或新增内容
//数组名.splice(操作的起始位置，删除几个，新增的项1，新增的项2，...)

//1.删除(任意位置)
songs1.splice(2, 2)
console.log("songs1数组", songs1)
//2.新增（任意位置）
songs.splice(1,0,"彩虹")
console.log("songs1数组", songs1)

/*个人研究
没有元素可以删仍然去删除后它返回的的是undefined，如：console.log("songs1数组", songs1.shift())
空数组打印也是空
songs1.splice(0)意味着删除0下标及后面的所有元素
 */

@Entry
@Component
struct Index {
  build() {

  }
}

