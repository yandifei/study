/*一元运算符
常见一元运算符：++和--
后置写法：先赋值后自增/自减
前置写法：先自增/自减再赋值

++作用：让变量，在原本基础之上加1
let num: number = 10
num++   //先赋值，后自增
++num   //先自增，后赋值
console.log('num',num)
 */

let num2_1: number =10
let res2: number = --num2_1
console.log("res2", res2)
console.log("num2", num2_1)

/*比较运算符
作用：用来判断比较两个数据大小，返回一个布尔值(true/false)
比较运算符    作用
>           判断大于
>=          判断大于等于
<           判断小于
<=          判断小于等于
==          判断相等
!=          判断不相等
 */

// 比较运算符 > >= < <= == !=
let num1: number = 11
let num2: number = 11
console.log("判断结果", num1>num2) // false
console.log("判断结果", num1<num2) // false
console.log("判断结果", num1>=num2)  // true
//==！=判断是否相等（判断数据，也会用来判断字符串）
let password: string ='123456'
let password2: string ='123456'
console.log('判断结果',password==password2)

/*逻辑运算符
作用：扩充判断条件
逻辑运算符     作用
&&        与，都真才真
||        或，一真则真
!           非，取反
 */

//逻辑运算符
//1.&&(全真则真）都得满足
console.log('结果1', 3 > 5 && 5 < 9)// false
console.log("结果2", 5 > 2 && 5 < 9)// true
//2.1|（一真则真）只要有一个满足即可
console.log("结果1", 3 > 5 || 5 < 9) // true
console.log('结果2',5 > 2 || 5 < 9)// true
console.log("结果3", 5 > 20 || 5 < 1) // false
//3.取反
console.log("结果", !true) //false

@Entry
@Component
struct Index {
  build() {

  }
}

