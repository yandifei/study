if (!("finalizeConstruction" in ViewPU.prototype)) {
    Reflect.set(ViewPU.prototype, "finalizeConstruction", () => { });
}
interface Index_Params {
    board?: CType[][];
    currentPlayer?: CType;
    gameName?: string;
    blackScore?: number;
    whiteScore?: number;
    gameLogic?: GameLogic;
    tip?: string;
}
import { CType, GameLogic } from "@normalized:N&&&entry/src/main/ets/logic/GameLogic&";
import type { Coordinate } from "@normalized:N&&&entry/src/main/ets/logic/GameLogic&";
class Index extends ViewPU {
    constructor(parent, params, __localStorage, elmtId = -1, paramsLambda = undefined, extraInfo) {
        super(parent, __localStorage, elmtId, extraInfo);
        if (typeof paramsLambda === "function") {
            this.paramsGenerator_ = paramsLambda;
        }
        this.__board = new ObservedPropertyObjectPU([], this, "board");
        this.__currentPlayer = new ObservedPropertySimplePU(CType.B, this, "currentPlayer");
        this.gameName = '黑白棋';
        this.__blackScore = new ObservedPropertySimplePU(0 // 黑棋分数
        , this, "blackScore");
        this.__whiteScore = new ObservedPropertySimplePU(0 // 白棋分数
        , this, "whiteScore");
        this.gameLogic = new GameLogic();
        this.__tip = new ObservedPropertySimplePU("玩家黑方先手", this, "tip");
        this.setInitiallyProvidedValue(params);
        this.finalizeConstruction();
    }
    setInitiallyProvidedValue(params: Index_Params) {
        if (params.board !== undefined) {
            this.board = params.board;
        }
        if (params.currentPlayer !== undefined) {
            this.currentPlayer = params.currentPlayer;
        }
        if (params.gameName !== undefined) {
            this.gameName = params.gameName;
        }
        if (params.blackScore !== undefined) {
            this.blackScore = params.blackScore;
        }
        if (params.whiteScore !== undefined) {
            this.whiteScore = params.whiteScore;
        }
        if (params.gameLogic !== undefined) {
            this.gameLogic = params.gameLogic;
        }
        if (params.tip !== undefined) {
            this.tip = params.tip;
        }
    }
    updateStateVars(params: Index_Params) {
    }
    purgeVariableDependenciesOnElmtId(rmElmtId) {
        this.__board.purgeDependencyOnElmtId(rmElmtId);
        this.__currentPlayer.purgeDependencyOnElmtId(rmElmtId);
        this.__blackScore.purgeDependencyOnElmtId(rmElmtId);
        this.__whiteScore.purgeDependencyOnElmtId(rmElmtId);
        this.__tip.purgeDependencyOnElmtId(rmElmtId);
    }
    aboutToBeDeleted() {
        this.__board.aboutToBeDeleted();
        this.__currentPlayer.aboutToBeDeleted();
        this.__blackScore.aboutToBeDeleted();
        this.__whiteScore.aboutToBeDeleted();
        this.__tip.aboutToBeDeleted();
        SubscriberManager.Get().delete(this.id__());
        this.aboutToBeDeletedInternal();
    }
    private __board: ObservedPropertyObjectPU<CType[][]>;
    get board() {
        return this.__board.get();
    }
    set board(newValue: CType[][]) {
        this.__board.set(newValue);
    }
    private __currentPlayer: ObservedPropertySimplePU<CType>;
    get currentPlayer() {
        return this.__currentPlayer.get();
    }
    set currentPlayer(newValue: CType) {
        this.__currentPlayer.set(newValue);
    }
    private gameName: string;
    private __blackScore: ObservedPropertySimplePU<number>; // 黑棋分数
    get blackScore() {
        return this.__blackScore.get();
    }
    set blackScore(newValue: number) {
        this.__blackScore.set(newValue);
    }
    private __whiteScore: ObservedPropertySimplePU<number>; // 白棋分数
    get whiteScore() {
        return this.__whiteScore.get();
    }
    set whiteScore(newValue: number) {
        this.__whiteScore.set(newValue);
    }
    private gameLogic: GameLogic;
    private __tip: ObservedPropertySimplePU<string>;
    get tip() {
        return this.__tip.get();
    }
    set tip(newValue: string) {
        this.__tip.set(newValue);
    }
    aboutToAppear() {
        this.restartGame();
    }
    restartGame() {
        this.board = [
            [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
            [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
            [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
            [CType.E, CType.E, CType.E, CType.W, CType.B, CType.E, CType.E, CType.E],
            [CType.E, CType.E, CType.E, CType.B, CType.W, CType.E, CType.E, CType.E],
            [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
            [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
            [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        ];
        // this.board = [
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.W, CType.W, CType.B, CType.B, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.W, CType.W, CType.B, CType.B, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.B, CType.B, CType.W, CType.W, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.B, CType.B, CType.W, CType.W, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
        //   [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E]
        // ]
        this.currentPlayer = CType.B;
    }
    // 构建提示框左右的黑白棋图标(这里改成按钮，点击一下就用贪心走一遍)
    aiButton(color: Color, parent = null) {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Button.createWithLabel();
            Button.debugLine("entry/src/main/ets/pages/Index.ets(55:5)", "entry");
            Button.backgroundColor(color);
            Button.height(32);
            Button.borderRadius(16);
            Button.onClick(() => {
                // 贪心算法获得落子位置
                const location = this.gameLogic.findGreedyMove(this.currentPlayer, ObservedObject.GetRawObject(this.board));
                // 手动判断有位置（这里是必要的，不然强类型不给我过），外加判断当前回合方为玩家才可以用，不然白方可以无限回合
                if ((location != null) && (this.currentPlayer === CType.B)) {
                    // 模拟点击，实际就是调用点击的逻辑
                    this.handleCellClick(location.row, location.col);
                }
            });
        }, Button);
        Button.pop();
    }
    // 点击逻辑事件，UI更新核心
    handleCellClick(row: number, col: number) {
        // 调用 GameLogic 中的 checkValidMove 方法，检查当前玩家在 (row, col) 处落子是否合法，
        const moveResult = this.gameLogic.checkValidMove(row, col, this.currentPlayer, this.board);
        // 检查走法是否有效
        if (moveResult.isValid) {
            // 创建新棋盘副本
            let newBoard: CType[][] = this.board.map(r => [...r]);
            // 在用户点击的位置放置当前玩家的棋子。
            newBoard[row][col] = this.currentPlayer;
            // 遍历所有可以被“夹住”并需要翻转的对方棋子坐标。
            moveResult.piecesToFlip.forEach((coord: Coordinate) => {
                // 将这些棋子改为当前玩家的类型（颜色）。
                newBoard[coord.row][coord.col] = this.currentPlayer;
            });
            // 将更新后的newBoard 赋值给 @State 变量 this.board，触发UI重新渲染棋盘。
            this.board = newBoard;
            // 重新计算分数
            let bScore = 0; // 黑棋分数计数器
            let wScore = 0; // 白棋分数计数器
            // 遍历新棋盘，统计黑棋 (B) 和白棋 (W) 的数量。
            newBoard.forEach(r => {
                r.forEach(c => {
                    if (c === CType.B) {
                        bScore++;
                    }
                    if (c === CType.W) {
                        wScore++;
                    }
                });
            });
            // 更新分数
            this.blackScore = bScore;
            this.whiteScore = wScore;
            // 如果当前是黑棋 (B)，则切换为白棋 (W)；否则切换为黑棋 (B)。
            this.currentPlayer = (this.currentPlayer === CType.B) ? CType.W : CType.B;
            // 更新提示框
            this.tip = (this.currentPlayer === CType.B) ? "黑方回合" : "白方回合";
        }
        else {
            this.tip = "无效走法"; // 刷新提示栏
        }
        // 白方棋手为AI选手
        if (this.currentPlayer === CType.W) {
            // 上贪心加权重的自动落子
            const aiMove: Coordinate | null = this.gameLogic.findGreedyMove(CType.W, this.board);
            if (aiMove) { // 有可以走的
                // 调用自己的方法更新棋盘，一次递归
                this.handleCellClick(aiMove.row, aiMove.col);
            }
        }
        // 当前棋手可落子的有效位置数量
        let possible_num = this.gameLogic.findAllValidMoves(this.currentPlayer, this.board).length;
        // 当前棋手无棋可走，游戏结束
        if (possible_num === 0) {
            //分数转文本(不搞下面的太长了，难看，虽然已经很难看了)
            let result_msg: String = `(${this.blackScore}:${this.whiteScore})`;
            // 弹出对话框
            this.getUIContext().showAlertDialog({
                // 判断谁无棋走
                message: (this.currentPlayer === CType.B ? `黑方无棋可走，${result_msg},` : `白方无棋可走，${result_msg}`) +
                    // 判断是否是平局
                    (this.blackScore === this.whiteScore ? "平局" : (
                    // 判断是哪方获胜
                    this.blackScore > this.whiteScore ? "黑方获胜" : "白方获胜"))
            });
            this.tip = "玩家黑方先手"; // 重启时重置提示文本
            this.restartGame(); // 直接重置棋盘
            // 重置双方分数
            this.blackScore = this.whiteScore = 0;
        }
    }
    initialRender() {
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            Column.create();
            Column.debugLine("entry/src/main/ets/pages/Index.ets(147:5)", "entry");
            Column.height("100%");
            Column.linearGradient({
                angle: 135,
                colors: [
                    // 左上角的浅青色
                    ['#AEEAE6', 0.0],
                    // 渐变到中间的白色
                    ['#FFFFFF', 0.3],
                    // 底部和右侧的浅桃色
                    ['#FEE9E7', 1]
                ]
            });
        }, Column);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 游戏名
            Text.create(this.gameName);
            Text.debugLine("entry/src/main/ets/pages/Index.ets(149:7)", "entry");
            // 游戏名
            Text.fontSize(32);
            // 游戏名
            Text.fontWeight(FontWeight.Bold);
            // 游戏名
            Text.fontColor('#2C3E50');
            // 游戏名
            Text.padding({ top: 40, bottom: 20 });
        }, Text);
        // 游戏名
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 打架的地方
            Grid.create();
            Grid.debugLine("entry/src/main/ets/pages/Index.ets(156:7)", "entry");
            // 打架的地方
            Grid.columnsTemplate('1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr');
            // 打架的地方
            Grid.rowsTemplate('1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr');
            // 打架的地方
            Grid.width('100%');
            // 打架的地方
            Grid.aspectRatio(1);
            // 打架的地方
            Grid.padding(10);
            // 打架的地方
            Grid.backgroundColor(Color.Black);
            // 打架的地方
            Grid.margin(10);
            // 打架的地方
            Grid.borderRadius(20);
        }, Grid);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 遍历棋盘的行数据
            ForEach.create();
            const forEachItemGenFunction = (_item, rowIndex: number) => {
                const rowItems = _item;
                this.observeComponentCreation2((elmtId, isInitialRender) => {
                    // 遍历每行内的棋子数据
                    ForEach.create();
                    const forEachItemGenFunction = (_item, colIndex: number) => {
                        const piece = _item;
                        {
                            const itemCreation2 = (elmtId, isInitialRender) => {
                                GridItem.create(() => { }, false);
                                GridItem.debugLine("entry/src/main/ets/pages/Index.ets(162:13)", "entry");
                            };
                            const observedDeepRender = () => {
                                this.observeComponentCreation2(itemCreation2, GridItem);
                                this.observeComponentCreation2((elmtId, isInitialRender) => {
                                    // 这里是栈，也就是重叠样式
                                    Stack.create({ alignContent: Alignment.Center });
                                    Stack.debugLine("entry/src/main/ets/pages/Index.ets(164:15)", "entry");
                                }, Stack);
                                this.observeComponentCreation2((elmtId, isInitialRender) => {
                                    // 棋盘格子按钮 (作为落子区域)
                                    Button.createWithLabel();
                                    Button.debugLine("entry/src/main/ets/pages/Index.ets(166:17)", "entry");
                                    // 棋盘格子按钮 (作为落子区域)
                                    Button.width('98%');
                                    // 棋盘格子按钮 (作为落子区域)
                                    Button.aspectRatio(1);
                                    // 棋盘格子按钮 (作为落子区域)
                                    Button.border({ width: 1, color: Color.Black, radius: 0 });
                                    // 棋盘格子按钮 (作为落子区域)
                                    Button.backgroundColor("#ff2a81e9");
                                    // 棋盘格子按钮 (作为落子区域)
                                    Button.onClick(() => {
                                        this.handleCellClick(rowIndex, colIndex); // 绑定点击事件
                                    });
                                }, Button);
                                // 棋盘格子按钮 (作为落子区域)
                                Button.pop();
                                this.observeComponentCreation2((elmtId, isInitialRender) => {
                                    If.create();
                                    // 棋子 (如果该位置有棋子)
                                    if (piece !== CType.E) {
                                        this.ifElseBranchUpdateFunction(0, () => {
                                            this.observeComponentCreation2((elmtId, isInitialRender) => {
                                                Circle.create();
                                                Circle.debugLine("entry/src/main/ets/pages/Index.ets(177:19)", "entry");
                                                Circle.width('80%');
                                                Circle.aspectRatio(1);
                                                Circle.fill(piece === CType.B ? Color.Black : Color.White);
                                            }, Circle);
                                        });
                                    }
                                    else {
                                        this.ifElseBranchUpdateFunction(1, () => {
                                        });
                                    }
                                }, If);
                                If.pop();
                                // 这里是栈，也就是重叠样式
                                Stack.pop();
                                // 单个栏栅格样式
                                GridItem.pop();
                            };
                            observedDeepRender();
                        }
                    };
                    this.forEachUpdateFunction(elmtId, rowItems, forEachItemGenFunction, // 这里必须是字符串，箭头函数执行的结果必须为字符串
                    (piece: CType, colIndex: number) => `${rowIndex}-${colIndex}`, true, true);
                }, ForEach);
                // 遍历每行内的棋子数据
                ForEach.pop();
            };
            this.forEachUpdateFunction(elmtId, this.board, forEachItemGenFunction, undefined, true, false);
        }, ForEach);
        // 遍历棋盘的行数据
        ForEach.pop();
        // 打架的地方
        Grid.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 提示框
            Row.create();
            Row.debugLine("entry/src/main/ets/pages/Index.ets(200:7)", "entry");
            // 提示框
            Row.height("50");
            // 提示框
            Row.width("95%");
            // 提示框
            Row.padding({ left: 20, right: 20 });
            // 提示框
            Row.margin({
                left: 10,
                top: 10,
                right: 10,
                bottom: 10
            });
            // 提示框
            Row.backgroundColor(Color.Gray);
            // 提示框
            Row.justifyContent(FlexAlign.SpaceBetween);
            // 提示框
            Row.borderRadius(10);
        }, Row);
        // 黑方棋图标
        this.aiButton.bind(this)(Color.Black);
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 黑方分数
            Text.create(this.blackScore.toString());
            Text.debugLine("entry/src/main/ets/pages/Index.ets(205:9)", "entry");
            // 黑方分数
            Text.fontSize(30);
            // 黑方分数
            Text.fontWeight(FontWeight.Bold);
        }, Text);
        // 黑方分数
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 文本提示
            Text.create(this.tip);
            Text.debugLine("entry/src/main/ets/pages/Index.ets(210:9)", "entry");
            // 文本提示
            Text.fontSize(25);
            // 文本提示
            Text.fontWeight(FontWeight.Bold);
        }, Text);
        // 文本提示
        Text.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 白方分数
            Text.create(this.whiteScore.toString());
            Text.debugLine("entry/src/main/ets/pages/Index.ets(215:9)", "entry");
            // 白方分数
            Text.fontSize(30);
            // 白方分数
            Text.fontWeight(FontWeight.Bold);
        }, Text);
        // 白方分数
        Text.pop();
        // 白色图标
        this.aiButton.bind(this)(Color.White);
        // 提示框
        Row.pop();
        this.observeComponentCreation2((elmtId, isInitialRender) => {
            // 重置按钮
            Button.createWithLabel("重新开始");
            Button.debugLine("entry/src/main/ets/pages/Index.ets(236:7)", "entry");
            // 重置按钮
            Button.width("50%");
            // 重置按钮
            Button.onClick(() => {
                this.tip = "玩家黑方先手"; // 重启时重置提示文本
                this.restartGame(); // 直接重置棋盘
                this.blackScore = this.whiteScore = 0; // 重置双方分数
            });
        }, Button);
        // 重置按钮
        Button.pop();
        Column.pop();
    }
    rerender() {
        this.updateDirtyElements();
    }
    static getEntryName(): string {
        return "Index";
    }
}
registerNamedRoute(() => new Index(undefined, {}), "", { bundleName: "edu.yandifei.myapplication", moduleName: "entry", pagePath: "pages/Index", pageFullPath: "entry/src/main/ets/pages/Index", integratedHsp: "false", moduleType: "followWithHap" });
