import { Deque } from '@kit.ArkTS';
class C1 {
  name: string = ""
  age: string = ""
}
let deque: Deque<string | number | boolean | Array<number> | C1> = new Deque();
deque.insertEnd("a");
deque.insertEnd(1);
let b = [1, 2, 3];
deque.insertEnd(b);
let c: C1 = {name : "Dylan", age : "13"};
deque.insertEnd(c);
deque.insertEnd(false);
console.log("now the deque is: ", JSON.stringify(deque));

// 提供的 API 不多。再尝试 insertFront，forEach 和 popFirst:
let deque1: Deque<number> = new Deque();
deque1.insertFront(1);
deque1.insertFront(2);
deque1.insertEnd(5);
deque1.insertFront(3);
deque1.insertFront(4);
console.log("now the deque1 is: ", JSON.stringify(deque1));
deque1.forEach((value: number, index?: number | undefined, deque?: Deque<number>|undefined):void => {
  console.log("value:" + value, "index:" + index);
});
let result = deque1.popFirst();
console.log("result is: ", result);

// 试一下 popLast():
let result2 = deque1.popLast();
console.log("result2 is: ", result2);

@Entry
@Component
struct Index {

  build() {
  }
}