if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface Index_Params {
    message?: string;
    // ShuiXianHuaDialog 创建一个 CustomDialogController，用于在点击事件的时候响应并打开对话框
    SXHNumberCustomDialogController?: CustomDialogController | null;
    // 乘法口诀的
    JiuJiuBiaoDialogController?: CustomDialogController | null;
}
import { ShuiXianHuaDialog } from "@normalized:N&&&entry/src/main/ets/view/ShuiXianHuaDialogl&";
import { JiuJiuBiaoDialog } from "@normalized:N&&&entry/src/main/ets/view/JiuJiuBiaoDialog&";
import { CommonConstants } from "@normalized:N&&&entry/src/main/ets/common/constants/Contants&";
import hilog from "@ohos:hilog";
class Index extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__message = new ObservedPropertySimplePU('Hello World', this, "message");
        this.SXHNumberCustomDialogController = new CustomDialogController({
            builder: () => {
                let jsDialog = new ShuiXianHuaDialog(this, {}, undefined, -1, () => { }, { page: "entry/src/main/ets/pages/Index.ets", line: 14, col: 14 });
                jsDialog.setController(this.
                // ShuiXianHuaDialog 创建一个 CustomDialogController，用于在点击事件的时候响应并打开对话框
                SXHNumberCustomDialogController);
                ViewPU.create(jsDialog);
                let paramsLambda = () => {
                    return {};
                };
                jsDialog.paramsGenerator_ = paramsLambda;
            }, alignment: DialogAlignment.Center, offset: { dx: 0, dy: -25 }
        }, this);
        this.JiuJiuBiaoDialogController = new CustomDialogController({
            builder: () => {
                let jsDialog = new JiuJiuBiaoDialog(this, {}, undefined, -1, () => { }, { page: "entry/src/main/ets/pages/Index.ets", line: 19, col: 14 });
                jsDialog.setController(this.
                // 乘法口诀的
                JiuJiuBiaoDialogController);
                ViewPU.create(jsDialog);
                let paramsLambda = () => {
                    return {};
                };
                jsDialog.paramsGenerator_ = paramsLambda;
            }, alignment: DialogAlignment.Center, offset: { dx: 0, dy: -25 }
        }, this);
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: Index_Params) {
        if (params.message !== undefined) {
            this.message = params.message;
        }
        if (params.SXHNumberCustomDialogController !== undefined) {
            this.SXHNumberCustomDialogController = params.SXHNumberCustomDialogController;
        }
        if (params.JiuJiuBiaoDialogController !== undefined) {
            this.JiuJiuBiaoDialogController = params.JiuJiuBiaoDialogController;
        }
    }
    updateStateVars(params: Index_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
        this.__message.purgeDependencyOnElmtId(rmElmtId);
    }
    aboutToBeDeleted() {
        this.__message.aboutToBeDeleted();
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    private __message: ObservedPropertySimplePU<string>;
    get message() {
        return this.__message.get();
    }
    set message(newValue: string) {
        this.__message.set(newValue);
    }
    // ShuiXianHuaDialog 创建一个 CustomDialogController，用于在点击事件的时候响应并打开对话框
    private SXHNumberCustomDialogController: CustomDialogController | null;
    // 乘法口诀的
    private JiuJiuBiaoDialogController: CustomDialogController | null;
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/Index.ets(25:5)", "entry");
            Column.justifyContent(FlexAlign.Start);
            Column.width(CommonConstants.PERCENT_FULL);
            Column.height(CommonConstants.PERCENT_FULL);
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('通过案例学习 ArkTS');
            Text.debugLine("entry/src/main/ets/pages/Index.ets(26:7)", "entry");
            Text.width('90%');
            Text.margin({
                top: '64vp', bottom: '8vp', left: '12vp', right: '20vp'
            });
            Text.fontSize('30fp');
            Text.fontWeight(700);
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Button.createWithLabel('水仙花数');
            Button.debugLine("entry/src/main/ets/pages/Index.ets(32:7)", "entry");
            Button.width('288vp');
            Button.height('40vp');
            Button.onClick(() => {
                // 调用这个对象的方法open
                this.SXHNumberCustomDialogController?.open();
            });
        }, Button);
        Button.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 乘法按钮
            Button.createWithLabel('打印九九乘法表');
            Button.debugLine("entry/src/main/ets/pages/Index.ets(40:7)", "entry");
            // 乘法按钮
            Button.width('288vp');
            // 乘法按钮
            Button.height('40vp');
            // 乘法按钮
            Button.margin({ top: '10vp' });
            // 乘法按钮
            Button.onClick(() => {
                this.JiuJiuBiaoDialogController?.open();
                let result = multiplicationTable();
                hilog.isLoggable(0xFF00, "testTag", hilog.LogLevel.INFO);
                for (let index = 0; index < result.length; index++) {
                    hilog.info(0xFF00, "testTag", result[index].toString());
                }
            });
        }, Button);
        // 乘法按钮
        Button.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
    static getEntryName(): string {
        return "Index";
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
registerNamedRoute(() => new Index(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/Index", pageFullPath: "entry/src/main/ets/pages/Index", integratedHsp: "false", moduleType: "followWithHap" });
