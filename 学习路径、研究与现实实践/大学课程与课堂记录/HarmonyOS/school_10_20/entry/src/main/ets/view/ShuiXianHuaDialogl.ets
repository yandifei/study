
// 判断是否是水仙花数
function shuiXianHuaNumber(): number[] {
  let result: number[] = [];
  for (let i = 100; i < 1000; i++) {
    let unitsDigit: number = i % 10;
    let tenthsDigit: number = Math.floor(i / 10) - Math.floor(i / 100) * 10;
    let hundredthsDigit: number = Math.floor(i / 100);
    if (i === unitsDigit * unitsDigit * unitsDigit + tenthsDigit * tenthsDigit *tenthsDigit +
      hundredthsDigit * hundredthsDigit * hundredthsDigit) {
      result.push(i);
    }
  }
  return result;
}

@Preview // 声明这是一个自定义对话框
@CustomDialog // 声明这是一个自定义对话框
export struct ShuiXianHuaDialog {
  IsPalindromicStringCustomDialogController?: CustomDialogController;
  build() {
    Column() {
      Column() {
        Text('ArkTS 实例')
          .height('40vp')
          .font({ size: $r('sys.float.ohos_id_text_size_headline8') })
          .fontColor($r('sys.color.ohos_id_color_text_primary'))
          .margin({ top: '8vp' })
        Text('1000 以内的水仙花数判断')
          .font({ size: $r('sys.float.ohos_id_text_size_body2') })
          .fontColor($r('sys.color.ohos_id_color_text_secondary'))
          .margin({ left: '10vp' })
      }
      .alignItems(HorizontalAlign.Center)
      .width('100%')
      .height('72vp')
      // 改成输出调用函数
      Text(shuiXianHuaNumber().toString())
        .font({ size: $r('sys.float.ohos_id_text_size_body1') })
        .fontColor($r('sys.color.ohos_id_color_text_primary'))
        .margin({ top: '24vp' })
    }
    .alignItems(HorizontalAlign.Center)
    .padding({
      left: '24vp', right: '24vp', bottom: '24vp' })
  }
}

