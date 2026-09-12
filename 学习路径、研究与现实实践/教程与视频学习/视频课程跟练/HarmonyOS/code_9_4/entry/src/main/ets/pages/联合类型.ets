/*联合类型
 联合类型是一种灵活的数据类型，它修饰的变量可以存储不同类型的数据。
 let jude: number = 100
 jude = 'A' 字符串不能分配给数字
 语法：
 let 变量: 类型1 | 类型2 | 类型3 = 值
 */

// 需求：定义一个变量，存放【年终考试评价】
// 考试评价：可能是具体的分数，也可能是A、B、C、D等级
let judge: number | string = 100
judge = 'A+'
judge = "优秀"
judge = "不错，继续努力"

console.log("年终考试评价", judge)

//联合类型还可以将变量值，约定在一组数据范围内进行选择
//性别:男 女 保密
let gender: "man" | "woman" | "secret" = "man"