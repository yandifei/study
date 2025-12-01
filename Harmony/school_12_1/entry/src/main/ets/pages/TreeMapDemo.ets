import { TreeMap } from '@kit.ArkTS';
//使用 comparator firstValue < secondValue，表示期望结果为升序排序。反之firstValue>secondValue，表示为降序排序。
let treeMap : TreeMap<string,string> = new TreeMap<string,string>((firstValue: string, secondValue: string) : boolean => {return firstValue > secondValue});
// let treeMap : TreeMap<string,string> = new TreeMap<string,string>((firstValue: string,secondValue: string) : boolean => {return firstValue < secondValue});
treeMap.set("aa","3");
treeMap.set("dd","1");
treeMap.set("cc","2");
treeMap.set("bb","4");
let numbers = Array.from(treeMap.keys())
for (let item of numbers) {
  console.log("treeMap:" + item);
}

//当插入自定义类型时，则必须要提供比较函数。
class TestEntry{
  public id: number = 0;
  public name: string = '';
}
let ts1: TreeMap<TestEntry, string> = new TreeMap<TestEntry, string>((t1: TestEntry, t2:
  TestEntry): boolean => {return t1.id < t2.id;});
let entry1: TestEntry = {
  id: 0, name: 'zhangshan' };
let entry2: TestEntry = {
  id: 1, name: 'lisi' }
ts1.set(entry1, "0");
ts1.set(entry2, "1");
console.log("treeMap: ", ts1.length);
let objects = Array.from(ts1.keys())
for (let item of objects) {
  console.log("treeMap:" + JSON.stringify(item));
}