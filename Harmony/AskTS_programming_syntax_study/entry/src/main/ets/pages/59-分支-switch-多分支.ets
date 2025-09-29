/* switch 分支
switch分支一般用于精确匹配，不同的值执行不同的代码
注意：如果没有break语句，则会直接执行switch中的下一个代码块（无论是否匹配成功）
*/

//输入水果名称，查询价格(精确匹配)
let fruit: string = "西瓜1"
// fruit可以被表达式替代，比如5>3
switch (fruit) {
  case "苹果":
    console.log("苹果价格", "2.8元一斤")
    break
  case "香蕉":
    console.log("香蕉价格", "5.5一斤")
    break
  case "西瓜":
    console.log("西瓜价格", "1.5元一斤")
    break
  // 没有提到的选项
  default:
    console.log("提示", "尊敬的用户，该水果不存在")
}

@Entry
@Component
struct Index {
  build() {

  }
}