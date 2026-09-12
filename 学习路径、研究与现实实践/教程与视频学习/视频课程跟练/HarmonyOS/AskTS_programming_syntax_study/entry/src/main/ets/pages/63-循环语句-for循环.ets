/*63-循环语句-for循环.ets
for 语句
作用：重复执行指定的一段代码
for (初始值；条件变化量) {
  重复执行的代码
}

Tips：循环三要素
1.初始值（变量）
2.循环条件
3.变化量（变量计数，自增或自减）
*/
// 需求：打印1-10从1开始，循环到10结束
for (let i: number = 1; i <= 10; i++) {
  console.log("for循环", i)
}

// 我靠，真的就是学java和和学C的狂喜啊
// C语言switch语句的case表达式只能是整数类型，这里有点不同，还是java7之后的版本都支持字符串了

// 练习：计算1-10内数字的累加和
let result: number = 0
for (let i: number = 0; i <= 10; i++) {
  result += i
}
console.log("1-10内数字的累加和为", result)

//个人研究
// let result: number = 0
// for (let i: number = 10; i >= 0; i--) {
//   result += i
// }
// console.log("1-10内数字的累加和为", result)

@Entry
@Component
struct Index {
  build() {

  }
}