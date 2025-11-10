if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface BuilderDemo_Params {
    message?: string;
}
class BuilderDemo extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__message = new ObservedPropertySimplePU('@Builder', this, "message");
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: BuilderDemo_Params) {
        if (params.message !== undefined) {
            this.message = params.message;
        }
    }
    updateStateVars(params: BuilderDemo_Params) {
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
    navItem(icon: ResourceStr, txt: string, parent = null) {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create({ space: 10 });
            Column.debugLine("entry/src/main/ets/pages/BuilderDemo.ets(23:5)", "entry");
            Column.width('25%');
            Column.onClick(() => {
                AlertDialog.show({
                    message: '点了' + txt
                });
            });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Image.create(icon);
            Image.debugLine("entry/src/main/ets/pages/BuilderDemo.ets(24:7)", "entry");
            Image.width('80%');
        }, Image);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(txt);
            Text.debugLine("entry/src/main/ets/pages/BuilderDemo.ets(26:7)", "entry");
        }, Text);
        Text.pop();
        Column.pop();
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create({ space: 20 });
            Column.debugLine("entry/src/main/ets/pages/BuilderDemo.ets(37:5)", "entry");
            Column.width('100%');
            Column.height('100%');
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(this.message);
            Text.debugLine("entry/src/main/ets/pages/BuilderDemo.ets(38:7)", "entry");
            Text.fontSize(30);
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Row.create();
            Row.debugLine("entry/src/main/ets/pages/BuilderDemo.ets(40:7)", "entry");
        }, Row);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Row.create();
            Row.debugLine("entry/src/main/ets/pages/BuilderDemo.ets(41:9)", "entry");
        }, Row);
        this.navItem.bind(this)({ "id": 16777230, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" }, '阿里拍卖');
        this.navItem.bind(this)({ "id": 16777228, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" }, '菜鸟');
        this.navItem.bind(this)({ "id": 16777231, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" }, '巴巴农场');
        this.navItem.bind(this)({ "id": 16777229, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" }, '阿里药房');
        Row.pop();
        Row.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
    static getEntryName(): string {
        return "BuilderDemo";
    }
}
registerNamedRoute(() => new BuilderDemo(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/BuilderDemo", pageFullPath: "entry/src/main/ets/pages/BuilderDemo", integratedHsp: "false", moduleType: "followWithHap" });
