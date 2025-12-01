import { PlainArray } from '@kit.ArkTS';
const plainArray: PlainArray<string> = new PlainArray();
let result = plainArray.isEmpty();
console.log("is it empty: ", result);
plainArray.add(1, "squirrel");
let result1 = plainArray.has(1);
console.log("key 1 exist? ", result1);
plainArray.add(2, "sparrow");
let result2 = plainArray.get(2);
console.log("key 2 value ", result2);
let result3 = plainArray.getIndexOfKey(2);
console.log("key 2 index ", result3);
let result4 = plainArray.getIndexOfValue("squirrel");
console.log("index is: ", result4);
plainArray.forEach((value: string, index?: number) => {
  console.log("value:" + value, "index:" + index);
});