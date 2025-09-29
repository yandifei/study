/*面向对象学习
对象：用来描述一个物体的特征和行为
对象：存储多个数据的容器
1. 定义接口
2. 基于接口，定义对象
*/


//1. 通过interface接口约定对象结构类型
/*深入研究
 这是模仿C语言的结构体？
 和java和python里的对象概念不同
 结构中不同属性没有都逗号
 interface  Person {
    属性1: 类型1
    属性2: 类型2
    属性3: 类型3
 }
 */
interface  Person {
  name: string
  age: number
  weight: number
}

//2. 基于接口，定义对象
let ydf: Person = {
  name: "雁低飞",
  age: 18,
  weight: 90
}

//3. 获取对象的属性值 对象名.属性
console.log("名字", ydf.name)
console.log("体重", ydf.weight)
console.log("年龄", ydf.age)


//基于接口，可以定义多个对象、这些对象有着相同的结构类型
let lss: Person = {
  name: "Arisu",
  age: 19,
  weight: 3
}

console.log("姓名", lss.name)
console.log("年龄", lss.age)
console.log("体重",lss.weight)

/*方法定义
interface 接口名称 {
  方法名:(参数:类型) => 返回类型
}
*/
//定义对象(属性加方法)
interface Person2 {
  name: string
  age: number
  weight: number

  //定义方法的类型
  sing: (song: string) => void
  dance: () => void
}

//实例化对象
let ym2: Person2 = {
  name: "大幂幂",
  age: 18,
  weight: 80,

  //定义方法
  sing: (song: string) => {
    console.log("杨幂说", "我来唱首歌", song)
  },
  dance: () => {
    console.log("杨幂说", "我来挑个舞")
  }
}

//调用对象里面的方法（重要！！！）
ym2.sing("爱的供养")
ym2.dance()