/*66-对象数组
对象数组=>数组中包裹存储了很多的对象
*/
import { JSON } from '@kit.ArkTS'

// 1.约定接口（对象的类型）
interface Student {
  stuID: number
  name: string
  gender: string
  age: number
}

//2.基于接口，构建对象数组
let stuArr: Student[] = [
  { stuID: 1, name: "小丽", gender: "女", age: 12 },
  { stuID: 1, name: "小红", gender: "女", age: 11 },
  { stuID: 1, name: "大强", gender: "男", age: 12 },
  { stuID: 1, name: "阿明", gender: "男", age: 13 },
]
// 包括对象的复杂数据，如果想要在日志中打印，需要调用一个方法，转成字符串格式
//JSoN.stringify(复杂类型) 对象/数组
// console.log("学生数组", stuArr)
console.log("学生数组", JSON.stringify(stuArr))

// //3.具体使用（访问通过下标）
console.log('小红',stuArr[1].name)
console.log('小红',JSON.stringify(stuArr[1]))

// 4.也支持遍历 for...of，普通for
for (let item of stuArr) {
  /*在我这个环境中我这里是没有成功打印的
   The json.stringify interface in the Previewer is a mocked implementation and may behave differently than on a real device.
   预览器中的JSON.STRINGIFY接口是模拟的实现，并且可能与真实设备上的行为不同。
   */
  console.log("每一项", JSON.stringify(item))
}

/*个人研究
弹幕:对象（结构体）  对象数组（结构体数组）
java佬简直狂喜啊！我python玩对象数组的时候都没有打过这么富裕的仗
这里的缺点就是我在java中要打印一个对象的所有属性都是toSting方法，这个方法是object内置的，但是
在ArkTS没有内置这个方法，这也和它用接口来创建对象有关。
还有一点就是黑马的这个视频中`4.也支持遍历 for...of，普通for`他是成功输出，但是我没没有成功输出
AI:
总结
你的 for...of 循环语法是完全正确的。
你遇到的问题不是代码语法错误，而是 DevEco Studio 预览器的局限性。
在实际开发中，如果预览器出现奇怪的行为，你应该优先在 设备（真机或模拟器） 上进行验证和调试。
 */

@Entry
@Component
struct Index {
  build() {

  }
}