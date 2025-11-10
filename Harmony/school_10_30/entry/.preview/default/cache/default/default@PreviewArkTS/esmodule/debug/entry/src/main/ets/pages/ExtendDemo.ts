if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface ExtendDemo_Params {
    message?: string;
}
function __Text__bannerItem(bgColor: ResourceColor, msg: string): void {
    Text.textAlign(TextAlign.Center);
    Text.backgroundColor(bgColor);
    Text.fontColor(Color.White);
    Text.fontSize(30);
    Text.onClick(() => {
        AlertDialog.show({
            message: msg
        });
    });
}
function __Text__textFn(): void {
    Text.fontSize(20);
    Text.fontWeight(FontWeight.Bold);
    Text.margin({ top: 20, bottom: 20 });
}
class ExtendDemo extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__message = new ObservedPropertySimplePU('@Extend-扩展组件(样式,事件)', this, "message");
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: ExtendDemo_Params) {
        if (params.message !== undefined) {
            this.message = params.message;
        }
    }
    updateStateVars(params: ExtendDemo_Params) {
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
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/ExtendDemo.ets(26:5)", "entry");
            Column.width('100%');
            Column.height('100%');
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(this.message);
            Text.debugLine("entry/src/main/ets/pages/ExtendDemo.ets(27:7)", "entry");
            __Text__textFn();
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Swiper.create();
            Swiper.debugLine("entry/src/main/ets/pages/ExtendDemo.ets(29:7)", "entry");
            Swiper.width('100%');
            Swiper.height(160);
        }, Swiper);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('1');
            Text.debugLine("entry/src/main/ets/pages/ExtendDemo.ets(30:9)", "entry");
            __Text__bannerItem(Color.Orange, '轮播图 1 号');
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('2');
            Text.debugLine("entry/src/main/ets/pages/ExtendDemo.ets(32:9)", "entry");
            __Text__bannerItem(Color.Brown, '轮播图 2 号');
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('3');
            Text.debugLine("entry/src/main/ets/pages/ExtendDemo.ets(34:9)", "entry");
            __Text__bannerItem(Color.Green, '轮播图 3 号');
        }, Text);
        Text.pop();
        Swiper.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
    static getEntryName(): string {
        return "ExtendDemo";
    }
}
registerNamedRoute(() => new ExtendDemo(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/ExtendDemo", pageFullPath: "entry/src/main/ets/pages/ExtendDemo", integratedHsp: "false", moduleType: "followWithHap" });
