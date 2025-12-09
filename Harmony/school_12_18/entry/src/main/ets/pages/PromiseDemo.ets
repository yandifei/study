// 导入基础服务包中的BusinessError类型，用于处理错误信息
import { BusinessError } from '@kit.BasicServicesKit';

// 创建一个返回字符串类型的Promise对象p
let p: Promise<string> = new Promise((resolve: Function, reject: Function) => {
  // 计算1+1的结果
  let a = 1 + 1;
  // 判断a是否等于2（这个条件总是成立的）
  if (a == 2) {
    // 如果条件成立，调用resolve函数，表示Promise成功完成，传递'Success'作为结果
    resolve('Success');
  } else {
    // 如果条件不成立（实际上不会发生），调用reject函数，表示Promise失败，传递'Failed'作为原因
    reject('Failed');
  }
});

// 使用then方法处理Promise成功的情况，catch方法处理Promise失败的情况
p.then((message: string) => {
  // 当Promise成功时，输出成功信息到控制台
  console.log('This is the promise fulfilled: ' + message);
}).catch((message: string) => {
  // 当Promise失败时，输出失败信息到控制台
  console.log('This is the promise rejected: ' + message);
});

// 创建另一个返回数字类型的Promise对象promise
const promise: Promise<number> = new Promise((resolve: Function, reject: Function) => {
  // 设置一个延时1秒的定时器
  setTimeout(() => {
    // 生成一个0到1之间的随机数
    const randomNumber: number = Math.random();
    // 判断随机数是否大于0.5
    if (randomNumber > 0.5) {
      // 如果大于0.5，调用resolve函数，表示Promise成功完成，传递随机数作为结果
      resolve(randomNumber);
    } else {
      // 如果小于等于0.5，调用reject函数，表示Promise失败，创建一个包含随机数信息的Error对象作为失败原因
      reject(new Error(`Random number is too small as it is ${randomNumber}`));
    }
  }, 1000); // 延时1秒执行
});

// 使用then方法处理Promise成功的情况，catch方法处理Promise失败的情况
promise.then((result: number) => {
  // 当Promise成功时，输出随机数到控制台（使用info级别日志）
  console.info(`Random number is ${result}`);
}).catch((error: BusinessError) => {
  // 当Promise失败时，输出错误信息到控制台（使用error级别日志）
  console.error(error.message);
});

// 注释：Promise.then()顺序执行，Promise.all()以及 Promise.race()
// 创建第一个Promise对象，1秒后完成
const actionPromise1: Promise<string> = new Promise((resolve: Function, reject: Function) => {
  setTimeout(() => {
    // 1秒后resolve，返回指定消息
    resolve('Action 1 fulfilled after 1 second!');
  }, 1000);
});

// 创建第二个Promise对象，5秒后完成
const actionPromise2: Promise<string> = new Promise((resolve: Function, reject: Function) => {
  setTimeout(() => {
    // 5秒后resolve，返回指定消息
    resolve('Action 2 fulfilled after 5 seconds!');
  }, 5000);
});

// 创建第三个Promise对象，10秒后完成
const actionPromise3: Promise<string> = new Promise((resolve: Function, reject: Function) => {
  setTimeout(() => {
    // 10秒后resolve，返回指定消息
    resolve('Action 3 fulfilled after 10 seconds!');
  }, 10000);
});

// 依次执行三个Promise操作
actionPromise1.then((message: string) => {
  // 当actionPromise1完成后，输出其结果
  console.log('Action 1: ' + message);
  // 继续处理actionPromise2
  actionPromise2.then((message: string) => {
    // 当actionPromise2完成后，输出其结果
    console.log('Action 2: ' + message);
    // 最后处理actionPromise3
    actionPromise3.then((message: string) => {
      // 当actionPromise3完成后，输出其结果
      console.log('Action 3: ' + message);
    });
  });
});