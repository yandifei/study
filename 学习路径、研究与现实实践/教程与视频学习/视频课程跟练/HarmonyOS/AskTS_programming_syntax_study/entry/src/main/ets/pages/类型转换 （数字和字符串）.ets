/*类型转换 （数字和字符串）
1.字符串转数字
Number()：字符串直接转数字，转换失败返回NaN（字符串中包含非数字）
parseInt()：去掉小数部分转数字，转换失败返回NaN
parseFloat()：保留小数部分转数字，转换失败返回NaN

需要注意的是取整数的的化他不会判断小数部分是否有效，也就是1.abcd都可以取整数啊！！！！！
仅仅填小数点不填小数位也是合规的，不填小数位也能转换
console.log("去掉小数展示", parseInt("1.abcdef"))
console.log("去掉小数展示", parseInt("1."))
console.log("去掉小数展示", parseInt("1"))
 */

let money: string = "10000"
let money2: number = 500
// +的两端，只要有字符串，就是拼接
// 需要是计算，必须都是数字=>将字符串类型，转成数字
// console.log('总工资'，Number(money)+money2)


let str1:string = "1.1"
let str2: string = "1.91"
let str3:string = "1.99a"
let str4: string = "a"
// 转数字类型
//1.Number(变量) 原样转数字
console.log('Number', Number(str1)) // 1.1
console.log('Number', Number(str2)) // 1.9
console.log('Number', Number(str3)) // NaN
console.log('Number', Number(str4)) // Nan
//2.parseInt(变量）去掉小数部分
console.log('parseInt', parseInt(str1))  // 1
console.log('parseInt', parseInt(str2))  // 1
console.log('parseInt', parseInt(str3))  // 1
console.log('parseInt', parseInt(str4))  //NaN
// 3.parseFloat(变量）保留小数部分
console.log('parseFloat', parseFloat(str1)) //1
console.log('parseFloat', parseFloat(str2)) //1
console.log('parseFloat', parseFloat(str3)) //1
console.log('parseFloat', parseFloat(str4)) // NaN

/* 类型转换（数字和字符串）
2.数字转字符串
toString()：数字直接转字符串
toFixed（)：四舍五入转字符串，可设置保留几位小数
 */

// 数字通常用于计算，字符串通常用于展示
let money1: number = 10000
// 将数字转字符串，toString toFixed()
//1.数据.toString()原样转字符串
console.log('toString:',money1.toString())
//2.数据.toFixed（保留几位小数）四舍五入
console.log('toFixed:',money1.toFixed())
console.log('toFixed:',money1.toFixed(2)) // 保留2位小数

@Entry
@Component
struct Index {
  @State message: string = 'Hello World';

  build() {
    RelativeContainer() {
      Text("工资发了：¥" + money1.toFixed(2))
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