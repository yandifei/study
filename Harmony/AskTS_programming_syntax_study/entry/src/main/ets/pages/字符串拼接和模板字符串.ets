/* 字符串拼接
作用：把两个或多个字符串，拼成一个字符串。(通常拼接的是字符串)
加号的作用：拼接
'hello' + 'world' => 'helloworld'

let name: string = '小明'
console.log('简介信息'，‘名字是'+name)简介信息名字是小明
 */

//字符串拼接+拼串
let name: string='吕布'
let age: number =18
console.log("简介信息:", "姓名" + name)
console.log("简介信息:", "年纪" + age)

//注意点：+两边只要有字符串，就是拼串的作用（如果两边都是数字，就是计算求和的作用)
let num1:  number = 100
let num2: number = 200
console.log("总数", num1 + num2)


/*模板字符串
`hello`
作用：拼接字符串和变量
优势：更适合于多个变量的字符串拼接

let name: string ='小明'
let age: number =18
console.log('简介信息'，｀姓名是${name}，今年${age}岁了`)
 */
//模板字符串``（支持变量，更利于字符串拼接）  普通字符串'' ""
// let str: string = `hello world`
let name2: string = "成小龙"
let age3: number = 18
let hobby:string = "打拳"
console.log("简介信息", `姓名：${name},年纪：${age}岁，爱好：${hobby}`)



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