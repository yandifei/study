// 变量的存储和修改（stringnumberboolean)
// 1.变量存储
// 1.1字符串string类型
// 注意点1：字符串需要用引号引起来
// 注意点2：存储的时候，后面的存的内容，需要和前面的类型对应
let title : String = "我是字符串"
console.log("字符串title", title);

// 1.2数字 number 类型
let age : number = 18
console.log("年龄", age)

// 1.3布尔 boolean 类型(true为真，false为假)
let isLogin : boolean = true
console.log("是否登陆成功", isLogin)
isLogin = false
console.log("是否登陆成功", isLogin)

// 2.变量的修改
age = 80
console.log("年龄", age )

// 常量
const name: String = "yandifei"
console.log("常量名字：", name)
const PI: number = 3.14
console.log("PI", PI)

//命名规则:
// 1.只能包含数字、字母、_、$，不能以数字开头--重点(和java一样，python没有$)
// 2.不能使用内置关键字或保留字（比如飞et、const）
// 3.严格区分大小写


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