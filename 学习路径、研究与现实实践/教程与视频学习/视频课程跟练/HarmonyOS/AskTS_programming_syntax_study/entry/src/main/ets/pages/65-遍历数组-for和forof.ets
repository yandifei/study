/*65-遍历数组-for和for of
遍历数组
遍历：将数组里面的每个数据，按顺序访问一遍
*/
// java和C在这个方舟语言中遍历数组做法都是通用的
// AskTS为什么方便数组遍历引入了另外1种语法for (let item of 数组名) {}

// 遍历数组：利用循环，依次按顺序访问数组的每一项
let names :string[] = ["大强", "老莫", "小龙", "大黑", "小黄"]
//数组的最后一项names[names.length - 1]
for (let i: number = 0; i < names.length; i++) {
  console.log("名字是", names[i])
}

/*第二种数组遍历方法
for (let item of 数组名) {}
for ...of：在...之中进行循环
item：声明的一个变量，用来在循环的时候接收每一个数组元素
 */

// 吐槽：java中的增强for，颇有python遗风
for (let i of names) {
  console.log("数组中的每一项", i)
}

// 案例(以下案例是自己写的吗，和视频有差别很正常)
// 需求1：求出下列数组元素的累加和
// [22, 3, 44, 55, 80]
let arr1: number[] = [22, 3, 44, 55, 80]
let result1: number = 0
for (let i of arr1) {
  result1 += i
}
console.log("需求1结果", result1)

// 需求2：筛选数组中大于等于10的元素，收集到一个新数组中
// [22, 3, 44, 55, 80, 10, 11, 5, -1]
let arr2: number[] = [22, 3, 44, 55, 80, 10, 11, 5, -1]
let result2: number[] = []
for (let i of arr2) {
  if (i >= 10) {
    result2.push(i)
  }
}
console.log("筛选数组中大于等于10的元素", result2)

// 需求3：数组去0，将数组中不是0的项收集到一个新数组中
// [22, 3, 0, 55, 0, 0, 11, 5, 0]
let arr3: number[] = [22, 3, 0, 55, 0, 0, 11, 5, 0]
let result3: number[] = []
for (let i of arr3) {
  if (i != 0) {
    result3.push(i)
  }
}
console.log("数组去0，将数组中不是0的项收集到一个新数组中", result3)

@Entry
@Component
struct Index {
  build() {

  }
}