/* 枚举类型（特殊）
 枚举类型是一种特殊的数据类型，约定变量只能在一组数据范围内选择值。
 enum 枚举名 {
  常量1 = 值,
  常量2 = 值,
  .....
 }
 */

// 1.定义枚举类型
enum ThemColor {
  Red = "#ff0f29",
  Orange = "#ff7100",
  Green = "#30b30e"
}

// 2.给变量设定枚举类型
let color: ThemColor = ThemColor.Red
console.log("color", color)