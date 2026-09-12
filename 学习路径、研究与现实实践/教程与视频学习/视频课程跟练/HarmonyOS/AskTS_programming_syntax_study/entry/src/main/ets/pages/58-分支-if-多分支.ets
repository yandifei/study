/*if多分支
if多分支，可以解决多种分支的情况
 */
let score: number = 82
if (score >= 90) {
  console.log("评价", "优秀")
}
else if (score >= 80) {
  console.log("评价", "良好")
}
else if (score >= 60) {
  console.log("评价", "及格")
}
else {
  console.log("评价", "不及格")
}


/*if多分支-小作业
需求：根据不同年纪，给出不同的生活建议
年龄<18：“你还是个孩子，应该多学习。"
18<=年龄＜30：“你正年轻，可以多去旅行，拓展视野。"
30<=年龄<50："你处于事业的黄金期，应该专注于工作和家庭。"
50<=年龄<70：“你已经积累了丰富的人生经验，可以考虑分享给小朋友们。"
年龄>=70："你应该享受晚年生活，多和家人在一起。"
*/

//我就做一下这个小作业吧
let age: number = 100
if (age < 18) {
  console.log("", "你还是个孩子，应该多学习。")
}
else if (age < 30) {
  console.log("", "你正年轻，可以多去旅行，拓展视野。")
}
else if (age < 50) {
  console.log("", "你处于事业的黄金期，应该专注于工作和家庭。")
}
else if (age < 70) {
  console.log("", "你已经积累了丰富的人生经验，可以考虑分享给小朋友们。")
}
else {
  console.log("", "你应该享受晚年生活，多和家人在一起。")
}

@Entry
@Component
struct Index {
  build() {

  }
}

