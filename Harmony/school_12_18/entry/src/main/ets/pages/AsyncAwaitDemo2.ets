// 定义一个异步函数myAsyncFunction，该函数返回一个Promise<string>类型的值
async function myAsyncFunction(): Promise<string> {
  // 使用await关键字等待一个Promise的完成，该Promise将在3秒后resolve
  const result: string = await new Promise((resolve: Function) => {
    // 设置一个延时定时器，3秒后执行
    setTimeout(() => {
      // 3秒后调用resolve函数，将Promise状态变为fulfilled，并传递'Hello, world!'字符串作为结果
      resolve('Hello, world!');
    }, 3000); // 延时3000毫秒（即3秒）
  });
  // 在控制台打印result变量的值，这里会输出：Hello, world!
  console.info(result); // 输出： Hello, world!
  // 返回result变量的值
  return result;
}

// 使用@Entry装饰器标记这是一个页面入口组件
@Entry
// 使用@Component装饰器标记这是一个组件
@Component
// 定义一个名为Index的结构体，作为UI组件
struct Index {
  // 使用@State装饰器声明一个响应式状态变量message，初始值为'Hello World'
  @State message: string = 'Hello World';
  
  // build函数定义了组件的UI结构
  build() {
    // 创建一个Row布局容器
    Row() {
      // 创建一个Column布局容器
      Column() {
        // 创建一个Text组件显示message状态变量的值
        Text(this.message)
          .fontSize(50) // 设置字体大小为50
          .fontWeight(FontWeight.Bold) // 设置字体粗细为Bold（粗体）
          // 为Text组件添加点击事件处理器
          .onClick(async () => {
            // 使用async箭头函数作为点击事件处理器
            // 使用await关键字等待myAsyncFunction函数的完成，并将结果赋值给res变量
            let res = await myAsyncFunction();
            // 在控制台打印res变量的值
            console.info("res is: " + res);
          })
      }
      .width('100%') // 设置Column容器的宽度为父容器的100%
    }
    .height('100%') // 设置Row容器的高度为父容器的100%
  }
}