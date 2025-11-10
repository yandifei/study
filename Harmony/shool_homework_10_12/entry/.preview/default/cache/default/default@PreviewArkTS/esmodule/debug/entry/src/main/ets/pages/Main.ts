if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface Main_Params {
    menuItems?: Array<NavigationMenuItem>;
    toolBar?: Array<ToolbarItem>;
    isSearchFocus?: boolean;
    friend_list?: friendList[];
}
// 定义接口 （每个列表项的数据结构）
interface friendList {
    imagePath: string; // 好友图像路径
    name: string; // 好友名
    lastTime: string; //最后的聊天时间
    lastMessage: string; // 最后的消息
}
// 定义列表
let friend_list: friendList[] = [];
// for来添加
for (let i = 1; i < 12; i++) {
    friend_list.push({
        imagePath: `/friend_image/f${i}.png`,
        name: `爱丽丝${i}`,
        lastTime: `10月${i}日`,
        lastMessage: "莫西莫西"
    });
}
class Main extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__menuItems = new ObservedPropertyObjectPU([
            { value: 'menuItem2', icon: { "id": 16777250, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" } }
        ]
        // 底部工具栏
        , this, "menuItems");
        this.__toolBar = new ObservedPropertyObjectPU([
            {
                "value": "消息",
                "icon": { "id": 16777249, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" },
                "action": () => { },
                // symbolIcon: new SymbolGlyphModifier($r('sys.symbol.ohos_lungs')),
                // "status": ToolbarItemStatus.ACTIVE,
                // "activeSymbolIcon": new SymbolGlyphModifier($r('app.media.message')).fontColor([Color.Red]).renderingStrategy(SymbolRenderingStrategy.MULTIPLE_COLOR),
            },
            {
                "value": "好友",
                "icon": { "id": 16777254, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" },
                "action": () => { }
            },
            {
                "value": "设置",
                "icon": { "id": 16777251, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" },
                "action": () => { }
            }
        ]
        // 扩大搜索框的范围
        , this, "toolBar");
        this.__isSearchFocus = new ObservedPropertySimplePU(false
        //好友列表
        // @State friend_list: friendList[] = [{imagePath: "/friend_image/f1.png", name: "1", lastTime:"1", lastMessage: "1"}]
        , this, "isSearchFocus");
        this.__friend_list = new ObservedPropertyObjectPU(friend_list, this, "friend_list");
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: Main_Params) {
        if (params.menuItems !== undefined) {
            this.menuItems = params.menuItems;
        }
        if (params.toolBar !== undefined) {
            this.toolBar = params.toolBar;
        }
        if (params.isSearchFocus !== undefined) {
            this.isSearchFocus = params.isSearchFocus;
        }
        if (params.friend_list !== undefined) {
            this.friend_list = params.friend_list;
        }
    }
    updateStateVars(params: Main_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
        this.__menuItems.purgeDependencyOnElmtId(rmElmtId);
        this.__toolBar.purgeDependencyOnElmtId(rmElmtId);
        this.__isSearchFocus.purgeDependencyOnElmtId(rmElmtId);
        this.__friend_list.purgeDependencyOnElmtId(rmElmtId);
    }
    aboutToBeDeleted() {
        this.__menuItems.aboutToBeDeleted();
        this.__toolBar.aboutToBeDeleted();
        this.__isSearchFocus.aboutToBeDeleted();
        this.__friend_list.aboutToBeDeleted();
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    // 导航头
    private __menuItems: ObservedPropertyObjectPU<Array<NavigationMenuItem>>;
    get menuItems() {
        return this.__menuItems.get();
    }
    set menuItems(newValue: Array<NavigationMenuItem>) {
        this.__menuItems.set(newValue);
    }
    // 底部工具栏
    private __toolBar: ObservedPropertyObjectPU<Array<ToolbarItem>>;
    get toolBar() {
        return this.__toolBar.get();
    }
    set toolBar(newValue: Array<ToolbarItem>) {
        this.__toolBar.set(newValue);
    }
    // 扩大搜索框的范围
    private __isSearchFocus: ObservedPropertySimplePU<boolean>;
    get isSearchFocus() {
        return this.__isSearchFocus.get();
    }
    set isSearchFocus(newValue: boolean) {
        this.__isSearchFocus.set(newValue);
    }
    //好友列表
    // @State friend_list: friendList[] = [{imagePath: "/friend_image/f1.png", name: "1", lastTime:"1", lastMessage: "1"}]
    private __friend_list: ObservedPropertyObjectPU<friendList[]>;
    get friend_list() {
        return this.__friend_list.get();
    }
    set friend_list(newValue: friendList[]) {
        this.__friend_list.set(newValue);
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/Main.ets(65:5)", "entry");
            Column.linearGradient({
                /* angle这个参数用于指定渐变的方向。它的值以度（degrees）为单位。
                0: 渐变从左到右。
                90: 渐变从下到上。
                180: 渐变从上到下。这是您代码中使用的值。
                270: 渐变从右到左。
                */
                angle: 180,
                // Explicitly define the color stops with their positions
                colors: [
                    ['#46aeeac9', 0.1], ['#2fa295ae', 0.5], ['#9afee9e7', 1]
                ]
            });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Navigation.create(new NavPathStack(), { moduleName: "entry", pagePath: "entry/src/main/ets/pages/Main", isUserCreateStack: false });
            Navigation.debugLine("entry/src/main/ets/pages/Main.ets(66:7)", "entry");
            Navigation.mode(NavigationMode.Auto);
            Navigation.menus(ObservedObject.GetRawObject(this.menuItems));
            Navigation.toolbarConfiguration(ObservedObject.GetRawObject(this.toolBar));
            Navigation.title("通讯");
            Navigation.titleMode(NavigationTitleMode.Mini);
        }, Navigation);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/Main.ets(67:9)", "entry");
            Column.padding({ left: 10, right: 10, bottom: 10 });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 搜索框
            Row.create();
            Row.debugLine("entry/src/main/ets/pages/Main.ets(69:11)", "entry");
            // 搜索框
            Row.backgroundColor("#f4f6f5");
            // 搜索框
            Row.borderRadius(20);
            // 搜索框
            Row.onClick(() => {
                console.log("1", this.isSearchFocus);
                this.isSearchFocus = true;
                console.log("1", this.isSearchFocus);
            });
        }, Row);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 搜索矢量图标设置高度和颜色
            Image.create({ "id": 16777253, "type": 20000, params: [], "bundleName": "edu.yandifei.myapplication", "moduleName": "entry" });
            Image.debugLine("entry/src/main/ets/pages/Main.ets(71:13)", "entry");
            // 搜索矢量图标设置高度和颜色
            Image.height("3%");
            // 搜索矢量图标设置高度和颜色
            Image.fillColor(Color.Gray);
            // 搜索矢量图标设置高度和颜色
            Image.padding({ left: "40%" });
        }, Image);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            TextInput.create({ placeholder: "搜索" });
            TextInput.debugLine("entry/src/main/ets/pages/Main.ets(73:13)", "entry");
            TextInput.backgroundColor(Color.Transparent);
            TextInput.padding({ left: 0 });
            TextInput.defaultFocus(this.isSearchFocus);
            TextInput.focusOnTouch(true);
            TextInput.onFocus(() => {
                this.isSearchFocus = false;
            });
        }, TextInput);
        // 搜索框
        Row.pop();
        Column.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 好友滚动列表
            List.create();
            List.debugLine("entry/src/main/ets/pages/Main.ets(92:9)", "entry");
        }, List);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            ForEach.create();
            const forEachItemGenFunction = (_item, index: number) => {
                const item = _item;
                {
                    const itemCreation = (elmtId, isInitialRender) => {
                        ViewStackProcessor.StartGetAccessRecordingFor(elmtId);
                        itemCreation2(elmtId, isInitialRender);
                        if (!isInitialRender) {
                            // 单个好友列表
                            ListItem.pop();
                        }
                        ViewStackProcessor.StopGetAccessRecording();
                    };
                    const itemCreation2 = (elmtId, isInitialRender) => {
                        ListItem.create(deepRenderFunction, true);
                        ListItem.debugLine("entry/src/main/ets/pages/Main.ets(95:13)", "entry");
                    };
                    const deepRenderFunction = (elmtId, isInitialRender) => {
                        itemCreation(elmtId, isInitialRender);
                        this.observeComponentCreation2((elmtId, isInitialRender) => {
                            Row.create();
                            Row.debugLine("entry/src/main/ets/pages/Main.ets(96:15)", "entry");
                            Row.width("100%");
                            Row.padding(7);
                            Row.border({
                                width: {
                                    left: 0,
                                    right: 0,
                                    top: 3,
                                    bottom: 0
                                },
                                color: "#ccc", //颜色为红色
                            });
                            Row.justifyContent(FlexAlign.SpaceBetween);
                        }, Row);
                        this.observeComponentCreation2((elmtId, isInitialRender) => {
                            Image.create(item.imagePath);
                            Image.debugLine("entry/src/main/ets/pages/Main.ets(97:17)", "entry");
                            Image.width(40);
                            Image.borderRadius(5);
                        }, Image);
                        this.observeComponentCreation2((elmtId, isInitialRender) => {
                            Column.create({ space: 7 });
                            Column.debugLine("entry/src/main/ets/pages/Main.ets(98:17)", "entry");
                        }, Column);
                        this.observeComponentCreation2((elmtId, isInitialRender) => {
                            Row.create();
                            Row.debugLine("entry/src/main/ets/pages/Main.ets(99:19)", "entry");
                            Row.width("80%");
                            Row.justifyContent(FlexAlign.SpaceBetween);
                        }, Row);
                        this.observeComponentCreation2((elmtId, isInitialRender) => {
                            Text.create(item.name);
                            Text.debugLine("entry/src/main/ets/pages/Main.ets(100:21)", "entry");
                            Text.fontSize(17);
                            Text.fontWeight(FontWeight.Bold);
                        }, Text);
                        Text.pop();
                        this.observeComponentCreation2((elmtId, isInitialRender) => {
                            Text.create(item.lastTime);
                            Text.debugLine("entry/src/main/ets/pages/Main.ets(101:21)", "entry");
                            Text.fontColor("#8bcccccc");
                        }, Text);
                        Text.pop();
                        Row.pop();
                        this.observeComponentCreation2((elmtId, isInitialRender) => {
                            // 最后消息为灰色(默认居左)
                            Text.create(item.lastMessage);
                            Text.debugLine("entry/src/main/ets/pages/Main.ets(105:19)", "entry");
                            // 最后消息为灰色(默认居左)
                            Text.width("80%");
                            // 最后消息为灰色(默认居左)
                            Text.fontColor("#ccc");
                            // 最后消息为灰色(默认居左)
                            Text.fontSize(14);
                        }, Text);
                        // 最后消息为灰色(默认居左)
                        Text.pop();
                        Column.pop();
                        Row.pop();
                        // 单个好友列表
                        ListItem.pop();
                    };
                    this.observeComponentCreation2(itemCreation2, ListItem);
                    // 单个好友列表
                    ListItem.pop();
                }
            };
            this.forEachUpdateFunction(elmtId, this.friend_list, forEachItemGenFunction, undefined, true, false);
        }, ForEach);
        ForEach.pop();
        // 好友滚动列表
        List.pop();
        Navigation.pop();
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
        return "Main";
    }
}
registerNamedRoute(() => new Main(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/Main", pageFullPath: "entry/src/main/ets/pages/Main", integratedHsp: "false", moduleType: "followWithHap" });
