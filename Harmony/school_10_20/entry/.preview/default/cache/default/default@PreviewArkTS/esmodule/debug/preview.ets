function multiplicationTable(): string[][] {
  let result: string[][] = [];
  for (let i = 1; i <= 9; i++) {
    let index: string[] = [];
    for (let j = 1; j <= i; j++) {
      let temp: string = j + ' * ' + i + ' = ' + i * j;
      index.push(temp);
    }
    result.push(index);
  }
  return result;
}
struct preview{build(){Column() {
      Text('通过案例学习 ArkTS')
        .width('90%')
        .margin({
          top: '64vp', bottom: '8vp', left: '12vp', right: '20vp'})
        .fontSize('30fp')
        .fontWeight(700)
      Button('水仙花数')
        .width('288vp')
        .height('40vp')
        .onClick(() => {
          // 调用这个对象的方法open
          this.SXHNumberCustomDialogController?.open();
        })
      // 乘法按钮
      Button('打印九九乘法表')
        .width('288vp')
        .height('40vp')
        .margin({ top: '10vp' })
        .onClick(() => {
          this.JiuJiuBiaoDialogController?.open();
          let result = multiplicationTable();
          hilog.isLoggable(0xFF00, "testTag", hilog.LogLevel.INFO);
          for (let index = 0; index < result.length; index++) {
            hilog.info(0xFF00, "testTag", result[index].toString());
          }
        })
    }
    .justifyContent(FlexAlign.Start)
    .width(CommonConstants.PERCENT_FULL)
    .height(CommonConstants.PERCENT_FULL)}}