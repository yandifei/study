if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface LinkDemo_Params {
    count?: number;
    stu1?: Student;
}
interface SonComponent_Params {
    sonCount?: number;
    sonStu1?: Student;
}
interface Student {
    name: string;
    age: number;
}
class SonComponent extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__sonCount = new SynchedPropertySimpleTwoWayPU(params.sonCount, this, "sonCount");
        this.__sonStu1 = new SynchedPropertyObjectTwoWayPU(params.sonStu1, this, "sonStu1");
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: SonComponent_Params) {
    }
    updateStateVars(params: SonComponent_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
        this.__sonCount.purgeDependencyOnElmtId(rmElmtId);
        this.__sonStu1.purgeDependencyOnElmtId(rmElmtId);
    }
    aboutToBeDeleted() {
        this.__sonCount.aboutToBeDeleted();
        this.__sonStu1.aboutToBeDeleted();
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    private __sonCount: SynchedPropertySimpleTwoWayPU<number>;
    get sonCount() {
        return this.__sonCount.get();
    }
    set sonCount(newValue: number) {
        this.__sonCount.set(newValue);
    }
    private __sonStu1: SynchedPropertySimpleOneWayPU<Student>;
    get sonStu1() {
        return this.__sonStu1.get();
    }
    set sonStu1(newValue: Student) {
        this.__sonStu1.set(newValue);
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create({ space: 20 });
            Column.debugLine("entry/src/main/ets/pages/LinkDemo.ets(11:5)", "entry");
            Column.backgroundColor('#a6c398');
            Column.alignItems(HorizontalAlign.Center);
            Column.width('80%');
            Column.margin({ top: 100 });
            Column.padding(10);
            Column.borderRadius(10);
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('我是子组件');
            Text.debugLine("entry/src/main/ets/pages/LinkDemo.ets(12:7)", "entry");
            Text.fontSize(20);
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(this.sonCount.toString());
            Text.debugLine("entry/src/main/ets/pages/LinkDemo.ets(14:7)", "entry");
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/LinkDemo.ets(15:7)", "entry");
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Button.createWithLabel('修改 count');
            Button.debugLine("entry/src/main/ets/pages/LinkDemo.ets(16:9)", "entry");
            Button.onClick(() => {
                this.sonCount++;
            });
        }, Button);
        Button.pop();
        Column.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
}
class LinkDemo extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__count = new ObservedPropertySimplePU(0, this, "count");
        this.__stu1 = new ObservedPropertyObjectPU({
            name: "张三",
            age: 18,
        }, this, "stu1");
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: LinkDemo_Params) {
        if (params.count !== undefined) {
            this.count = params.count;
        }
        if (params.stu1 !== undefined) {
            this.stu1 = params.stu1;
        }
    }
    updateStateVars(params: LinkDemo_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
        this.__count.purgeDependencyOnElmtId(rmElmtId);
        this.__stu1.purgeDependencyOnElmtId(rmElmtId);
    }
    aboutToBeDeleted() {
        this.__count.aboutToBeDeleted();
        this.__stu1.aboutToBeDeleted();
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    private __count: ObservedPropertySimplePU<number>;
    get count() {
        return this.__count.get();
    }
    set count(newValue: number) {
        this.__count.set(newValue);
    }
    private __stu1: ObservedPropertyObjectPU<Student>;
    get stu1() {
        return this.__stu1.get();
    }
    set stu1(newValue: Student) {
        this.__stu1.set(newValue);
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/LinkDemo.ets(39:5)", "entry");
            Column.padding(10);
            Column.height('100%');
            Column.backgroundColor('#eee');
            Column.width('100%');
            Column.alignItems(HorizontalAlign.Center);
            Column.padding({ top: 100 });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create('父组件');
            Text.debugLine("entry/src/main/ets/pages/LinkDemo.ets(40:7)", "entry");
            Text.fontSize(30);
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(this.count.toString());
            Text.debugLine("entry/src/main/ets/pages/LinkDemo.ets(42:7)", "entry");
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Text.create(`${this.stu1.name}, ${this.stu1.age}`);
            Text.debugLine("entry/src/main/ets/pages/LinkDemo.ets(43:7)", "entry");
        }, Text);
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Button.createWithLabel('修改数据');
            Button.debugLine("entry/src/main/ets/pages/LinkDemo.ets(44:7)", "entry");
            Button.onClick(() => {
                this.count++;
                this.stu1.age++;
            });
        }, Button);
        Button.pop();
        {
            this.observeComponentCreation2((elmtId, isInitialRender) => {
                if (isInitialRender) {
                    let componentCall = new SonComponent(this, {
                        sonCount: this.__count,
                        sonStu1: this.__stu1
                    }, undefined, elmtId, () => { }, { page: "entry/src/main/ets/pages/LinkDemo.ets", line: 49, col: 7 });
                    ViewPU.create(componentCall);
                    let paramsLambda = () => {
                        return {
                            sonCount: this.count,
                            sonStu1: this.stu1
                        };
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
    static getEntryName(): string {
        return "LinkDemo";
    }
}
registerNamedRoute(() => new LinkDemo(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/LinkDemo", pageFullPath: "entry/src/main/ets/pages/LinkDemo", integratedHsp: "false", moduleType: "followWithHap" });
