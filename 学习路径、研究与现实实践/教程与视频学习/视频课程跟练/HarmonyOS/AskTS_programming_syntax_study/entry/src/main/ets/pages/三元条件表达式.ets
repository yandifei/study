/* 三元条件表达式
语法：条件？条件成立执行的表达式：条件不成立执行的表达式
*/
//这里和java、C、C++、vbs都是一样的，会的都能直接条，黑马视频没细节
let num1: number = 40
let num2: number = 30
//
// let max: number = num1 > num2 ? num1 : num2
// console.log("三元条件表达式", max)

let res: number = num1 > num2 ? 3 * 5 : 2 + 6
console.log("三元条件表达式", res)

@Entry
@Component
struct Index {
  build() {

  }
}