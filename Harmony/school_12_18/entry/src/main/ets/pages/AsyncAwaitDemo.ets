// 定义一个函数makeRequest，接受一个位置参数location，返回一个Promise<string>类型的值
function makeRequest(location: string) {
  // 返回一个新的Promise对象，该Promise将解析为string类型
  return new Promise<string>((resolve: Function, reject: Function) => {
    // 在控制台打印正在向指定位置发出请求的信息
    console.log(`Making Request to ${location}`);
    // 判断传入的位置是否为'Huawei'
    if (location == 'Huawei') {
      // 如果是'Huawei'，则调用resolve函数，将Promise状态变为fulfilled，并返回'Huawei says welcome'
      resolve('Huawei says welcome');
    } else {
      // 如果不是'Huawei'，则调用reject函数，将Promise状态变为rejected，并返回'We can only talk to Huawei'作为拒绝理由
      reject('We can only talk to Huawei');
    }
  });
}

// 定义一个函数processRequest，接受一个响应字符串参数response，返回一个Promise<string>类型的值
function processRequest(response: string) {
  // 返回一个新的Promise对象，该Promise将解析为string类型
  return new Promise<string>((resolve: Function, reject: Function) => {
    // 在控制台打印正在处理响应的信息
    console.log('Processing response');
    // 调用resolve函数，将Promise状态变为fulfilled，并返回拼接后的字符串'Extra Information + ${response}'
    resolve(`Extra Information + ${response}`);
  });
}

// 定义一个名为doWork的异步函数，使用async关键字表明这是一个异步函数
async function doWork() {
  // 使用await关键字等待makeRequest('Huawei') Promise的完成
  // await会暂停当前async函数的执行，直到Promise被解决（resolved）或被拒绝（rejected）
  // 一旦Promise完成，将结果赋值给response变量
  const response = await makeRequest('Huawei');
  
  // 在控制台打印"Response Received"消息，表示已经收到了响应
  console.log('Response Received');
  
  // 使用await关键字等待processRequest(response) Promise的完成
  // 同样，await会暂停当前async函数的执行，直到Promise被解决或被拒绝
  // 一旦Promise完成，将处理后的结果赋值给processedResponse变量
  const processedResponse = await processRequest(response);
  
  // 在控制台打印处理后的响应结果
  console.log(processedResponse);
}

// 调用doWork函数来执行异步操作
// 由于doWork是异步函数，它会立即返回一个Promise，但实际执行会在稍后进行
doWork();