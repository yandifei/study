if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface Index_Params {
    message?: string;
}
import router from "@ohos:router";
class Index extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__message = new ObservedPropertySimplePU('Hello World', this, "message");
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: Index_Params) {
        if (params.message !== undefined) {
            this.message = params.message;
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
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/Index.ets(9:5)", "entry");
            Column.height('100%');
            Column.width('100%');
            Column.padding({ right: 20, left: 20 });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // log图标
            Image.create({ "id": 16777239, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Image.debugLine("entry/src/main/ets/pages/Index.ets(11:7)", "entry");
            // log图标
            Image.width("50%");
        }, Image);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 文本控价
            Text.create("欢迎回来");
            Text.debugLine("entry/src/main/ets/pages/Index.ets(15:7)", "entry");
            // 文本控价
            Text.fontSize(FontWeight.Bolder);
            // 文本控价
            Text.fontSize(35);
            // 文本控价
            Text.margin({ top: 20, bottom: 20 });
        }, Text);
        // 文本控价
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 账号输入区域
            Row.create();
            Row.debugLine("entry/src/main/ets/pages/Index.ets(21:7)", "entry");
            // 账号输入区域
            Row.backgroundColor("#f4f6f5");
            // 账号输入区域
            Row.borderRadius(20);
        }, Row);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            //左侧图标
            Image.create({ "id": 16777232, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Image.debugLine("entry/src/main/ets/pages/Index.ets(23:9)", "entry");
            //左侧图标
            Image.width("7%");
            //左侧图标
            Image.margin({ left: 10 });
        }, Image);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 账号输入框
            TextInput.create({ placeholder: "请输入用户名" });
            TextInput.debugLine("entry/src/main/ets/pages/Index.ets(27:9)", "entry");
            // 账号输入框
            TextInput.placeholderColor("#c1c1c1");
            // 账号输入框
            TextInput.placeholderFont({ size: 20, weight: FontWeight.Medium });
            // 账号输入框
            TextInput.backgroundColor(Color.Transparent);
            // 账号输入框
            TextInput.margin({ right: 30 });
        }, TextInput);
        // 账号输入区域
        Row.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 密码输入框区域
            Row.create();
            Row.debugLine("entry/src/main/ets/pages/Index.ets(37:7)", "entry");
            // 密码输入框区域
            Row.width("100%");
            // 密码输入框区域
            Row.backgroundColor("#f4f6f5");
            // 密码输入框区域
            Row.borderRadius(25);
            // 密码输入框区域
            Row.margin({ top: 15, bottom: 15 });
        }, Row);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            //左侧图标
            Image.create({ "id": 16777235, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Image.debugLine("entry/src/main/ets/pages/Index.ets(39:9)", "entry");
            //左侧图标
            Image.width("7%");
            //左侧图标
            Image.margin({ left: 10 });
        }, Image);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 密码输入框
            TextInput.create({ placeholder: "请输入密码" });
            TextInput.debugLine("entry/src/main/ets/pages/Index.ets(43:9)", "entry");
            // 密码输入框
            TextInput.type(InputType.Password);
            // 密码输入框
            TextInput.placeholderColor("#c1c1c1");
            // 密码输入框
            TextInput.placeholderFont({ size: 20, weight: FontWeight.Medium });
            // 密码输入框
            TextInput.backgroundColor(Color.Transparent);
            // 密码输入框
            TextInput.margin({ right: 30 });
        }, TextInput);
        // 密码输入框区域
        Row.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 注册和忘记密码区域
            Row.create();
            Row.debugLine("entry/src/main/ets/pages/Index.ets(56:7)", "entry");
            // 注册和忘记密码区域
            Row.width('100%');
            // 注册和忘记密码区域
            Row.justifyContent(FlexAlign.SpaceBetween);
        }, Row);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 立即注册
            Text.create("立即登陆");
            Text.debugLine("entry/src/main/ets/pages/Index.ets(58:9)", "entry");
            // 立即注册
            Text.backgroundColor("#fff");
            // 立即注册
            Text.fontColor("#ff5f5f5f");
        }, Text);
        // 立即注册
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 忘记密码
            Text.create("忘记密码");
            Text.debugLine("entry/src/main/ets/pages/Index.ets(62:9)", "entry");
            // 忘记密码
            Text.backgroundColor("#fff");
            // 忘记密码
            Text.fontColor("#ff5f5f5f");
        }, Text);
        // 忘记密码
        Text.pop();
        // 注册和忘记密码区域
        Row.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 登陆按钮
            Button.createWithLabel("登陆");
            Button.debugLine("entry/src/main/ets/pages/Index.ets(70:7)", "entry");
            // 登陆按钮
            Button.fontSize(20);
            // 登陆按钮
            Button.fontWeight(FontWeight.Bold);
            // 登陆按钮
            Button.width("100%");
            // 登陆按钮
            Button.margin({ top: 25, bottom: 200 });
            // 登陆按钮
            Button.onClick(() => {
                this.getUIContext().getRouter().pushUrl({
                    url: "pages/Main", // 目标url
                }, router.RouterMode.Standard, (err) => {
                    if (err) {
                        console.error(`跳转失败， 错误代码：${err.code}，错误信息 ${err.message}`);
                        return;
                    }
                    console.info("跳转成功");
                });
            });
        }, Button);
        // 登陆按钮
        Button.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 其他的登陆方式
            Row.create();
            Row.debugLine("entry/src/main/ets/pages/Index.ets(89:7)", "entry");
            // 其他的登陆方式
            Row.width("80%");
            // 其他的登陆方式
            Row.justifyContent(FlexAlign.SpaceBetween);
        }, Row);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // QQ
            Image.create({ "id": 16777228, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Image.debugLine("entry/src/main/ets/pages/Index.ets(91:9)", "entry");
            // QQ
            Image.width("14%");
            // QQ
            Image.borderRadius(25);
        }, Image);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 微信
            Image.create({ "id": 16777230, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Image.debugLine("entry/src/main/ets/pages/Index.ets(95:9)", "entry");
            // 微信
            Image.width("14%");
            // 微信
            Image.borderRadius(25);
        }, Image);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // GitHub
            Image.create({ "id": 16777246, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Image.debugLine("entry/src/main/ets/pages/Index.ets(99:9)", "entry");
            // GitHub
            Image.width("14%");
            // GitHub
            Image.borderRadius(25);
        }, Image);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // Gitee
            Image.create({ "id": 16777248, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Image.debugLine("entry/src/main/ets/pages/Index.ets(103:9)", "entry");
            // Gitee
            Image.width("14%");
            // Gitee
            Image.borderRadius(25);
        }, Image);
        // 其他的登陆方式
        Row.pop();
        Column.pop();
    }
    // 禁用界面入场和出场有动画
    pageTransition() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            PageTransition.create();
        }, null);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            PageTransitionEnter.create({ type: RouteType.None, duration: 0 });
        }, null);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            PageTransitionExit.create({ type: RouteType.None, duration: 0 });
        }, null);
        PageTransition.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
    static getEntryName(): string {
        return "Index";
    }
}
registerNamedRoute(() => new Index(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/Index", pageFullPath: "entry/src/main/ets/pages/Index", integratedHsp: "false", moduleType: "followWithHap" });
