/* 62-while语句&三个练习
while 语句
作用：重复执行指定的一段代码
while (条件) {
  需要循环执行的语句
}
*/

// 死循环：没有结束条件
// while (true) {
//   console.log("while", "重复执行代码")
// }

// Tips: 循环三要素 1.初始值（变量） 2.循环条件 3.变化量（变量计数，自增或自减）
// let i: number = 1
// while (i < 10) {
//   console.log("小于10成立", "执行代码", i)
//   i++
// }

// while语句一练习
// 需求1：打印1-100的数字
let i: number = 1
while (i <= 100) {
  console.log("打印1-100的数字", i)
  i++
}
//需求2：打印1-100中的偶数
let j: number = 1
while (j <= 100) {
  if (j % 2 == 0) {
    console.log("打印1-100中的偶数", i)
  }
  j++
}
// 需求3：计算1-10内数字的累加和
let k: number = 1
let result: number = 0
while (k <= 10) {
  console.log("需要累加的数字", k)
  // 每次执行下面这行代码，就会进行一次累加，并且更新累加的结果
  result += k
  k++
}
console.log("计算1-10内数字的累加和为", result)


@Entry
@Component
struct Index {
  build() {

  }
}