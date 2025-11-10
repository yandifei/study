if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface FatherCom_Params {
    fHouse?: string;
}
interface SonCom_Params {
    sHouse?: string;
}
class SonCom extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.sHouse = '';
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: SonCom_Params) {
        if (params.sHouse !== undefined) {
            this.sHouse = params.sHouse;
        }
    }
    updateStateVars(params: SonCom_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
    }
    aboutToBeDeleted() {
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    private sHouse: string;
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/PropDemo.ets(5:5)", "entry");
            Column.padding(20);
            Column.backgroundColor(Color.Orange);
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(`子组件 ${this.sHouse}`);
            Text.debugLine("entry/src/main/ets/pages/PropDemo.ets(6:7)", "entry");
        }, Text);
        Text.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
}
class FatherCom extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__fHouse = new ObservedPropertySimplePU('市区公寓', this, "fHouse");
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: FatherCom_Params) {
        if (params.fHouse !== undefined) {
            this.fHouse = params.fHouse;
        }
    }
    updateStateVars(params: FatherCom_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
        this.__fHouse.purgeDependencyOnElmtId(rmElmtId);
    }
    aboutToBeDeleted() {
        this.__fHouse.aboutToBeDeleted();
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    private __fHouse: ObservedPropertySimplePU<string>;
    get fHouse() {
        return this.__fHouse.get();
    }
    set fHouse(newValue: string) {
        this.__fHouse.set(newValue);
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create({ space: 10 });
            Column.debugLine("entry/src/main/ets/pages/PropDemo.ets(17:3)", "entry");
            Column.padding(50);
            Column.backgroundColor(Color.Pink);
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(`父组件 - ${this.fHouse}`);
            Text.debugLine("entry/src/main/ets/pages/PropDemo.ets(18:5)", "entry");
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Button.createWithLabel('换房子');
            Button.debugLine("entry/src/main/ets/pages/PropDemo.ets(19:5)", "entry");
            Button.onClick(() => {
                this.fHouse = '郊区别墅';
            });
        }, Button);
        Button.pop();
        {
            this.observeComponentCreation2((elmtId, isInitialRender) => {
                if (isInitialRender) {
                    let componentCall = new SonCom(this, {
                        sHouse: this.fHouse,
                    }, undefined, elmtId, () => { }, { page: "entry/src/main/ets/pages/PropDemo.ets", line: 21, col: 5 });
                    ViewPU.create(componentCall);
                    let paramsLambda = () => {
                        return {
                            sHouse: this.fHouse
                        };
                    };
                    componentCall.paramsGenerator_ = paramsLambda;
                }
                else {
                    this.updateStateVarsOfChildByElmtId(elmtId, {});
                }
            }, { name: "SonCom" });
        }
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
    static getEntryName(): string {
        return "FatherCom";
    }
}
registerNamedRoute(() => new FatherCom(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/PropDemo", pageFullPath: "entry/src/main/ets/pages/PropDemo", integratedHsp: "false", moduleType: "followWithHap" });
