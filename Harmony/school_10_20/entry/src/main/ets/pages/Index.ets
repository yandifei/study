// 外部导入自己的结构体
import { ShuiXianHuaDialog } from  "../view/ShuiXianHuaDialogl"
import { JiuJiuBiaoDialog } from  "../view/JiuJiuBiaoDialog"
import { CommonConstants } from "../common/constants/Contants"
import hilog from '@ohos.hilog';


@Entry
@Component
struct Index {
  @State message: string = 'Hello World';
  // ShuiXianHuaDialog 创建一个 CustomDialogController，用于在点击事件的时候响应并打开对话框
  SXHNumberCustomDialogController: CustomDialogController | null = new CustomDialogController({
    builder: ShuiXianHuaDialog(), alignment: DialogAlignment.Center, offset: { dx: 0, dy: -25 }
  });

  // 乘法口诀的
  JiuJiuBiaoDialogController: CustomDialogController | null = new CustomDialogController({
    builder: JiuJiuBiaoDialog(), alignment: DialogAlignment.Center, offset: { dx: 0, dy: -25 }
  });



  build() {
    Column() {
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
    .height(CommonConstants.PERCENT_FULL)
  }
}


// 乘法的代码逻辑
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
