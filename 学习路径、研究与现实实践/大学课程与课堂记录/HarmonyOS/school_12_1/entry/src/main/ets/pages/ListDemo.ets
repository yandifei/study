import { List } from '@kit.ArkTS';
let list: List<string | number | boolean | object> = new List();
let result1 = list.add("a");
console.log("after result1:", JSON.stringify(list));
let result2 = list.add(1);
console.log("after result2:", JSON.stringify(list));
let b = [1, 2, 3];
let result3 = list.add(b);
console.log("after result3:", JSON.stringify(list));
class C {
  name: string = ''
  age: string = ''
}
let c: C = {name : "Dylan", age : "13"};
let result4 = list.add(c);
console.log("after result4:", JSON.stringify(list));
let result5 = list.add(false);
console.log("after result5:", JSON.stringify(list));


// 类似地，尝试 insert:
list.insert("A", 0);
console.log("after insert:", JSON.stringify(list));
list.insert(0, 1);
console.log("after insert:", JSON.stringify(list));
list.insert(true, 2);
console.log("after insert:", JSON.stringify(list));


// 尝试 has:
let res1 = list.has(b);
console.log("Do we have [1,2,3]?", res1);

// 尝试 get，注意[下标会产生未定义结果]
let res2 = list.get(3);
console.log("the value got is: ", res2);
let res3 = list.get(6);
console.log("the value got is: ", JSON.stringify(res3));

@Entry
@Component
struct Index {

  build() {
  }
}