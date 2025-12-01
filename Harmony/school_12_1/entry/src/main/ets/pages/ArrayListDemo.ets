import { ArrayList } from '@kit.ArkTS';
class C1 {
  name: string = ""
  age: string = ""
}
let arrayList: ArrayList<string | number | boolean | Array<number> | C1> = new ArrayList();
let result1 = arrayList.add("a");
console.log("after result1:", JSON.stringify(arrayList));
let result2 = arrayList.add(1);
console.log("after result2:", JSON.stringify(arrayList));
let b = [1, 2, 3];
let result3 = arrayList.add(b);
console.log("after result3:", JSON.stringify(arrayList));
let c : C1 = {name: "Dylan", age: "13"}
let result4 = arrayList.add(c);
console.log("after result4:", JSON.stringify(arrayList));
let result5 = arrayList.add(false);
console.log("after result5:", JSON.stringify(arrayList));


// insert 函数（位置参数是必填的，不能不填）
arrayList.insert("A", 0);
console.log("after insert:", JSON.stringify(arrayList));
arrayList.insert(0, 1);
console.log("after insert:", JSON.stringify(arrayList));
arrayList.insert(true, 2);
console.log("after insert:", JSON.stringify(arrayList));


// 添加代码，看一下 remove 的效果：
let res1: boolean = arrayList.remove(b); //前面 b=[1,2,3]
console.log("after remove:", JSON.stringify(arrayList));
let res2: boolean = arrayList.remove("a");
console.log("after remove:", JSON.stringify(arrayList));


// 添加代码，看一下 forEach 的作用：
arrayList.forEach((value: string | number | boolean | Array<number> | C1, index?: number)=> {
  console.log("value:" + value, "index:" + index);
});


// 再看一下函数 has 和 getIndexOf 的作用
let res3: boolean = arrayList.has("A");
console.log("Do we have it? ", res3);
let res4: number = arrayList.getIndexOf(c);
console.log("Index is: ", res4);

// 添加代码，看 replaceAllElements 的作用
let arrayList1: ArrayList<number>= new ArrayList();
arrayList1.add(2);
arrayList1.add(4);
arrayList1.add(5);
arrayList1.add(4);
console.log("before replace:", JSON.stringify(arrayList1));


@Entry
@Component
struct Index {

  build() {
  }
}