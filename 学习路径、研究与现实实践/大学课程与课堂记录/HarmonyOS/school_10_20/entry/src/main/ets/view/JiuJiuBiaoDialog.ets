

@Preview
@CustomDialog
export struct JiuJiuBiaoDialog {
  IsPalindromicStringCustomDialogController?: CustomDialogController;
  build() {
    Column() {
      Column() {
        Text('ArkTS 实例')
          .height('40vp')
          .font({ size: $r('sys.float.ohos_id_text_size_headline8') })
          .fontColor($r('sys.color.ohos_id_color_text_primary'))
          .fontColor($r('sys.color.ohos_id_color_text_primary'))
          .margin({ top: '8vp' })
        Text('九九乘方表')
          .font({ size: $r('sys.float.ohos_id_text_size_body2') })
          .fontColor($r('sys.color.ohos_id_color_text_secondary'))
          .margin({ left: '10vp' })
      }
      .alignItems(HorizontalAlign.Center)
      .width('100%')
      .height('72vp')
      Text('请查看 Log 中打印出来的结果')
        .font({ size: $r('sys.float.ohos_id_text_size_body1') })
        .fontColor($r('sys.color.ohos_id_color_text_primary'))
        .margin({ top: '24vp' })
    }
    .alignItems(HorizontalAlign.Center)
    .padding({
      left: '24vp', right: '24vp', bottom: '24vp' })
  }
}