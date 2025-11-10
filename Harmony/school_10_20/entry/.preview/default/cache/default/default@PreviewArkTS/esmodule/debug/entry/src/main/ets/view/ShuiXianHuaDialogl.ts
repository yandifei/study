if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface ShuiXianHuaDialog_Params {
    IsPalindromicStringCustomDialogController?: CustomDialogController;
}
// 判断是否是水仙花数
function shuiXianHuaNumber(): number[] {
    let result: number[] = [];
    for (let i = 100; i < 1000; i++) {
        let unitsDigit: number = i % 10;
        let tenthsDigit: number = Math.floor(i / 10) - Math.floor(i / 100) * 10;
        let hundredthsDigit: number = Math.floor(i / 100);
        if (i === unitsDigit * unitsDigit * unitsDigit + tenthsDigit * tenthsDigit * tenthsDigit +
            hundredthsDigit * hundredthsDigit * hundredthsDigit) {
            result.push(i);
        }
    }
    return result;
}
export class ShuiXianHuaDialog extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.IsPalindromicStringCustomDialogController = undefined;
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: ShuiXianHuaDialog_Params) {
        if (params.IsPalindromicStringCustomDialogController !== undefined) {
            this.IsPalindromicStringCustomDialogController = params.IsPalindromicStringCustomDialogController;
        }
    }
    updateStateVars(params: ShuiXianHuaDialog_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
    }
    aboutToBeDeleted() {
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    private IsPalindromicStringCustomDialogController?: CustomDialogController;
    setController(ctr: CustomDialogController) {
        this.IsPalindromicStringCustomDialogController = ctr;
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/view/ShuiXianHuaDialogl.ets(22:5)", "entry");
            Column.alignItems(HorizontalAlign.Center);
            Column.padding({
                left: '24vp', right: '24vp', bottom: '24vp'
            });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/view/ShuiXianHuaDialogl.ets(23:7)", "entry");
            Column.alignItems(HorizontalAlign.Center);
            Column.width('100%');
            Column.height('72vp');
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('ArkTS 实例');
            Text.debugLine("entry/src/main/ets/view/ShuiXianHuaDialogl.ets(24:9)", "entry");
            Text.height('40vp');
            Text.font({ size: { "id": 125829676, "type": 10002, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" } });
            Text.fontColor({ "id": 125829210, "type": 10001, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Text.margin({ top: '8vp' });
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('1000 以内的水仙花数判断');
            Text.debugLine("entry/src/main/ets/view/ShuiXianHuaDialogl.ets(29:9)", "entry");
            Text.font({ size: { "id": 125829685, "type": 10002, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" } });
            Text.fontColor({ "id": 125829216, "type": 10001, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Text.margin({ left: '10vp' });
        }, Text);
        Text.pop();
        Column.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 改成输出调用函数
            Text.create(shuiXianHuaNumber().toString());
            Text.debugLine("entry/src/main/ets/view/ShuiXianHuaDialogl.ets(38:7)", "entry");
            // 改成输出调用函数
            Text.font({ size: { "id": 125829684, "type": 10002, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" } });
            // 改成输出调用函数
            Text.fontColor({ "id": 125829210, "type": 10001, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            // 改成输出调用函数
            Text.margin({ top: '24vp' });
        }, Text);
        // 改成输出调用函数
        Text.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
}
if (getPreviewComponentFlag()) {
    storePreviewComponents(1, "ShuiXianHuaDialog", new ShuiXianHuaDialog(undefined, {}));
    previewComponent();
}
else {
}
