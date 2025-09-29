// 数组
// 语法
// let 数组名: 类型[] = [数据1, 数据2, 数据3, ...]

// 数组中存储的每个数据都有自己的编号，编号从0开始(索引)
let names: string[] = ["yandifei", "ban", "tom", "jie"]
console.log("数组names：", names)

// 利用序号(索引)取数组的数据
// 取数据：数组名[索引]
console.log("数组names的第一个元素", names[0])

//注意：数组声明好的类型，后面的存的数据必须和他一致

/* let names: string[] = ["yandifei", "ban", "tom", 1000]
1000 是错误的
 */

// 函数学习
/*函数定义
function 关键字（函数声明）
printStar 函数名
{
  函数体
}

它的参数必须指定类型
 */
function printStar() {
  console.log("五角星", "*")
  console.log("五角星", "**")
  console.log("五角星", "***")
  console.log("五角星", "****")
  console.log("五角星", "*****")
}

// 调用函数
printStar()
printStar()

//函数返回值
function count(a: number, b: number) {
  // let result: number = a * b
  return a + b
}
//输出
console.log("计算结果", count(1, 2))

//默认返回值
function testReturn() {
  return
}
console.log("函数默认返回值", testReturn())  //undefined

/**箭头函数
 * 箭头函数是是比普通函数更简洁的一种函数写法
 *个人：我靠这就是匿名函数（python里面的lambda）
 * let 函数名 = (形参1: 类型, 形参2: 类型) => {
   //函数体
   return 返回结果
   }
 */

let star = () => {
  console.log("五角星", "*")
  console.log("五角星", "**")
  console.log("五角星", "***")
  console.log("五角星", "****")
  console.log("五角星", "*****")
}
star()

let buy = (price: number, weight: number) => {
  // 需求2:
  // 用箭头函数，完成计算
  // 传入价格和数量，返回计算的结果
  // 1，苹果2元/斤，买了3斤，多少钱?
  // 2，香蕉4元/斤，买了4斤，多少钱?
  let result: number = price * weight
  return result
}

let apple: number = buy(2, 3)
console.log("苹果",apple)

let banana: number = buy(4, 4)
console.log("香蕉", banana)

console.log("需求2计算结果", buy(1,2))

console.log("test", 1)


@Entry
@Component
struct Index {
  @State message: string = 'Hello World';

  build() {
    RelativeContainer() {
      Text(this.message)
        .id('HelloWorld')
        .fontSize($r('app.float.page_text_font_size'))
        .fontWeight(FontWeight.Bold)
        .alignRules({
          center: { anchor: '__container__', align: VerticalAlign.Center },
          middle: { anchor: '__container__', align: HorizontalAlign.Center }
        })
        .onClick(() => {
          this.message = 'Welcome';
        })
    }
    .height('100%')
    .width('100%')
  }
}