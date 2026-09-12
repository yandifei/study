import { HashSet } from '@kit.ArkTS';
let hashSet: HashSet<number> = new HashSet();
hashSet.add(1);
hashSet.add(2);
hashSet.add(3);
hashSet.add(4);
hashSet.add(5);
let res = hashSet.length;
console.log("res:", res);
hashSet.forEach((value?: number, key?: number): void => {
  console.log("value:" + value, "key:" + key);
});
let hashSet1: HashSet<string> = new HashSet();
hashSet1.add("sparrow");
hashSet1.add("squirrel");
hashSet1.forEach((value?: string, key?: string): void => {
  console.log("value:" + value, "key:" + key);
});

@Entry
@Component
struct Index {

  build() {
  }
}