if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface JiuJiuBiaoDialog_Params {
    IsPalindromicStringCustomDialogController?: CustomDialogController;
}
export class JiuJiuBiaoDialog extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.IsPalindromicStringCustomDialogController = undefined;
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: JiuJiuBiaoDialog_Params) {
        if (params.IsPalindromicStringCustomDialogController !== undefined) {
            this.IsPalindromicStringCustomDialogController = params.IsPalindromicStringCustomDialogController;
        }
    }
    updateStateVars(params: JiuJiuBiaoDialog_Params) {
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
            Column.debugLine("entry/src/main/ets/view/JiuJiuBiaoDialog.ets(8:5)", "entry");
            Column.alignItems(HorizontalAlign.Center);
            Column.padding({
                left: '24vp', right: '24vp', bottom: '24vp'
            });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/view/JiuJiuBiaoDialog.ets(9:7)", "entry");
            Column.alignItems(HorizontalAlign.Center);
            Column.width('100%');
            Column.height('72vp');
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('ArkTS 实例');
            Text.debugLine("entry/src/main/ets/view/JiuJiuBiaoDialog.ets(10:9)", "entry");
            Text.height('40vp');
            Text.font({ size: { "id": 125829676, "type": 10002, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" } });
            Text.fontColor({ "id": 125829210, "type": 10001, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Text.fontColor({ "id": 125829210, "type": 10001, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Text.margin({ top: '8vp' });
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('九九乘方表');
            Text.debugLine("entry/src/main/ets/view/JiuJiuBiaoDialog.ets(16:9)", "entry");
            Text.font({ size: { "id": 125829685, "type": 10002, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" } });
            Text.fontColor({ "id": 125829216, "type": 10001, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Text.margin({ left: '10vp' });
        }, Text);
        Text.pop();
        Column.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('请查看 Log 中打印出来的结果');
            Text.debugLine("entry/src/main/ets/view/JiuJiuBiaoDialog.ets(24:7)", "entry");
            Text.font({ size: { "id": 125829684, "type": 10002, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" } });
            Text.fontColor({ "id": 125829210, "type": 10001, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Text.margin({ top: '24vp' });
        }, Text);
        Text.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
}
if (getPreviewComponentFlag()) {
    storePreviewComponents(1, "JiuJiuBiaoDialog", new JiuJiuBiaoDialog(undefined, {}));
    previewComponent();
}
else {
}
