import { curves } from '@kit.ArkUI';
class Spring {
  public title: string;
  public subTitle: string;
  public iCurve: ICurve;
  constructor(title: string, subTitle: string, iCurve: ICurve) {
    this.title = title;
    this.iCurve = iCurve;
    this.subTitle = subTitle;
  }
}
@Entry
@Component
export struct SpringCurve {
  build() {
  }
}