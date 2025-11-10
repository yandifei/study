if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface SonComponent_Params {
}
interface ParentComponent_Params {
}
interface RootComponent_Params {
}
class RootComponent extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: RootComponent_Params) {
    }
    updateStateVars(params: RootComponent_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
    }
    aboutToBeDeleted() {
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/ProvideConsumeDemo.ets(6:5)", "entry");
            Column.padding(10);
            Column.height('100%');
            Column.backgroundColor('#ccc');
            Column.width('100%');
            Column.alignItems(HorizontalAlign.Center);
            Column.padding({ top: 100 });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('顶级组件');
            Text.debugLine("entry/src/main/ets/pages/ProvideConsumeDemo.ets(7:7)", "entry");
            Text.fontSize(30);
            Text.fontWeight(900);
        }, Text);
        Text.pop();
        {
            this.observeComponentCreation2((elmtId, isInitialRender) => {
                if (isInitialRender) {
                    let componentCall = new ParentComponent(this, {}, undefined, elmtId, () => { }, { page: "entry/src/main/ets/pages/ProvideConsumeDemo.ets", line: 10, col: 7 });
                    ViewPU.create(componentCall);
                    let paramsLambda = () => {
                        return {};
                    };
                    componentCall.paramsGenerator_ = paramsLambda;
                }
                else {
                    this.updateStateVarsOfChildByElmtId(elmtId, {});
                }
            }, { name: "ParentComponent" });
        }
        {
            this.observeComponentCreation2((elmtId, isInitialRender) => {
                if (isInitialRender) {
                    let componentCall = new ParentComponent(this, {}, undefined, elmtId, () => { }, { page: "entry/src/main/ets/pages/ProvideConsumeDemo.ets", line: 11, col: 7 });
                    ViewPU.create(componentCall);
                    let paramsLambda = () => {
                        return {};
                    };
                    componentCall.paramsGenerator_ = paramsLambda;
                }
                else {
                    this.updateStateVarsOfChildByElmtId(elmtId, {});
                }
            }, { name: "ParentComponent" });
        }
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
    static getEntryName(): string {
        return "RootComponent";
    }
}
class ParentComponent extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: ParentComponent_Params) {
    }
    updateStateVars(params: ParentComponent_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
    }
    aboutToBeDeleted() {
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    // 编写 UI
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create({ space: 20 });
            Column.debugLine("entry/src/main/ets/pages/ProvideConsumeDemo.ets(26:5)", "entry");
            Column.backgroundColor('#a6c398');
            Column.alignItems(HorizontalAlign.Center);
            Column.width('90%');
            Column.margin({ top: 50 });
            Column.padding(10);
            Column.borderRadius(10);
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('我是二级组件');
            Text.debugLine("entry/src/main/ets/pages/ProvideConsumeDemo.ets(27:7)", "entry");
            Text.fontSize(22);
            Text.fontWeight(900);
        }, Text);
        Text.pop();
        {
            this.observeComponentCreation2((elmtId, isInitialRender) => {
                if (isInitialRender) {
                    let componentCall = new SonComponent(this, {}, undefined, elmtId, () => { }, { page: "entry/src/main/ets/pages/ProvideConsumeDemo.ets", line: 30, col: 7 });
                    ViewPU.create(componentCall);
                    let paramsLambda = () => {
                        return {};
                    };
                    componentCall.paramsGenerator_ = paramsLambda;
                }
                else {
                    this.updateStateVarsOfChildByElmtId(elmtId, {});
                }
            }, { name: "SonComponent" });
        }
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
}
class SonComponent extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: SonComponent_Params) {
    }
    updateStateVars(params: SonComponent_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
    }
    aboutToBeDeleted() {
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    // 编写 UI
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create({ space: 20 });
            Column.debugLine("entry/src/main/ets/pages/ProvideConsumeDemo.ets(45:5)", "entry");
            Column.backgroundColor('#bf94e4');
            Column.alignItems(HorizontalAlign.Center);
            Column.width('90%');
            Column.margin({ top: 50 });
            Column.padding(10);
            Column.borderRadius(10);
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('我是内层组件');
            Text.debugLine("entry/src/main/ets/pages/ProvideConsumeDemo.ets(46:7)", "entry");
            Text.fontSize(20);
            Text.fontWeight(900);
        }, Text);
        Text.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
}
registerNamedRoute(() => new RootComponent(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/ProvideConsumeDemo", pageFullPath: "entry/src/main/ets/pages/ProvideConsumeDemo", integratedHsp: "false", moduleType: "followWithHap" });
