if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface StylesDemo_Params {
    message?: string;
    bgColor?: ResourceColor;
}
class StylesDemo extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__message = new ObservedPropertySimplePU('@styles', this, "message");
        this.__bgColor = new ObservedPropertyObjectPU(Color.Blue, this, "bgColor");
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: StylesDemo_Params) {
        if (params.message !== undefined) {
            this.message = params.message;
        }
        if (params.bgColor !== undefined) {
            this.bgColor = params.bgColor;
        }
    }
    updateStateVars(params: StylesDemo_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
        this.__message.purgeDependencyOnElmtId(rmElmtId);
        this.__bgColor.purgeDependencyOnElmtId(rmElmtId);
    }
    aboutToBeDeleted() {
        this.__message.aboutToBeDeleted();
        this.__bgColor.aboutToBeDeleted();
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
    private __bgColor: ObservedPropertyObjectPU<ResourceColor>;
    get bgColor() {
        return this.__bgColor.get();
    }
    set bgColor(newValue: ResourceColor) {
        this.__bgColor.set(newValue);
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create({ space: 10 });
            Column.debugLine("entry/src/main/ets/pages/StylesDemo.ets(13:5)", "entry");
            Column.width('100%');
            Column.height('100%');
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(this.message);
            Text.debugLine("entry/src/main/ets/pages/StylesDemo.ets(14:7)", "entry");
            Text.fontColor(Color.White);
            Text.width(100);
            Text.height(100);
            Text.backgroundColor(ObservedObject.GetRawObject(this.bgColor));
            Text.onClick(() => {
                this.bgColor = Color.Orange;
            });
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/StylesDemo.ets(22:7)", "entry");
            Column.width(100);
            Column.height(100);
            Column.backgroundColor(ObservedObject.GetRawObject(this.bgColor));
            Column.onClick(() => {
                this.bgColor = Color.Orange;
            });
        }, Column);
        Column.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Button.createWithLabel('按钮');
            Button.debugLine("entry/src/main/ets/pages/StylesDemo.ets(29:7)", "entry");
            Button.width(100);
            Button.height(100);
            Button.backgroundColor(ObservedObject.GetRawObject(this.bgColor));
            Button.onClick(() => {
                this.bgColor = Color.Orange;
            });
        }, Button);
        Button.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
    static getEntryName(): string {
        return "StylesDemo";
    }
}
registerNamedRoute(() => new StylesDemo(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/StylesDemo", pageFullPath: "entry/src/main/ets/pages/StylesDemo", integratedHsp: "false", moduleType: "followWithHap" });
