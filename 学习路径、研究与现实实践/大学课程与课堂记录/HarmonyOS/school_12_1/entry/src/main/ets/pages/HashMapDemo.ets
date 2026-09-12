import { HashMap } from '@kit.ArkTS';
const hashMap: HashMap<string, number> = new HashMap();
let result = hashMap.isEmpty();
console.log("is it empty: ", result);
hashMap.set("squirrel", 123);
let result1 = hashMap.hasValue(123);
let result2 = hashMap.hasKey("squirrel");
console.log("do we have the value: ", result1);
console.log("do we have the key: ", result2);
// - set: 添加 key-value 键值对
// - hasKey: 判断是否有键 key
// - hasValue: 判断是否有值 value
// - isEmpty: 判断这个 HashMap 是否为空
// 再添加代码看 get 函数：
hashMap.set("sparrow", 356);
let result3 = hashMap.get("sparrow");
console.log("sparrow's value is: ", result3);

// 再添加代码看 forEach 和 setAll（将一个 HashMap 中的所有元素组添加到另一个hashMap 中）
console.log("before setAll:")
hashMap.forEach((value?: number, key?: string) => {
  console.log("value:" + value, "key:" + key);
});
let newHashMap: HashMap<string, number> = new HashMap();
newHashMap.set("newMap", 99);
hashMap.setAll(newHashMap);
console.log("after setAll:")
hashMap.forEach((value?: number, key?: string) => {
  console.log("value:" + value, "key:" + key);
});

// 再添加代码看 replace:
console.log("after replace:")
let result4 = hashMap.replace("sparrow", 357);
hashMap.forEach((value?: number, key?: string) => {
  console.log("value:" + value, "key:" + key);
});

@Entry
@Component
struct Index {

  build() {
  }
}