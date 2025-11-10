// 导包
import { CType, GameLogic, Coordinate } from '../logic/GameLogic'

@Entry
@Component
struct Index {
  @State board: CType[][] = []
  @State currentPlayer: CType = CType.B
  private gameName: string = '黑白棋'
  @State blackScore: number = 0 // 黑棋分数
  @State whiteScore: number = 0 // 白棋分数
  private gameLogic: GameLogic = new GameLogic()
  @State tip: string = "玩家黑方先手"

  aboutToAppear() {
    this.restartGame()
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
    ]
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

    this.currentPlayer = CType.B
  }

  // 构建提示框左右的黑白棋图标(这里改成按钮，点击一下就用贪心走一遍)
  @Builder
  aiButton(color: Color) {
    Button()
      .backgroundColor(color)
      .height(32)
      .borderRadius(16)
      .onClick(() => { // 点击显示分数
        // 贪心算法获得落子位置
        const location = this.gameLogic.findGreedyMove(this.currentPlayer, this.board)
        // 手动判断有位置（这里是必要的，不然强类型不给我过），外加判断当前回合方为玩家才可以用，不然白方可以无限回合
        if ((location != null) && (this.currentPlayer === CType.B)) {
          // 模拟点击，实际就是调用点击的逻辑
          this.handleCellClick(location.row, location.col)
        }
      })
  }

  // 点击逻辑事件，UI更新核心
  handleCellClick(row: number, col: number) {
    // 调用 GameLogic 中的 checkValidMove 方法，检查当前玩家在 (row, col) 处落子是否合法，
    const moveResult = this.gameLogic.checkValidMove(row, col, this.currentPlayer, this.board)
    // 检查走法是否有效
    if (moveResult.isValid) {
      // 创建新棋盘副本
      let newBoard: CType[][] = this.board.map(r => [...r])
      // 在用户点击的位置放置当前玩家的棋子。
      newBoard[row][col] = this.currentPlayer
      // 遍历所有可以被“夹住”并需要翻转的对方棋子坐标。
      moveResult.piecesToFlip.forEach((coord: Coordinate) => {
        // 将这些棋子改为当前玩家的类型（颜色）。
        newBoard[coord.row][coord.col] = this.currentPlayer
      })
      // 将更新后的newBoard 赋值给 @State 变量 this.board，触发UI重新渲染棋盘。
      this.board = newBoard
      // 重新计算分数
      let bScore = 0 // 黑棋分数计数器
      let wScore = 0 // 白棋分数计数器
      // 遍历新棋盘，统计黑棋 (B) 和白棋 (W) 的数量。
      newBoard.forEach(r => {
        r.forEach(c => {
          if (c === CType.B) {
            bScore++
          }
          if (c === CType.W) {
            wScore++
          }
        })
      })
      // 更新分数
      this.blackScore = bScore
      this.whiteScore = wScore
      // 如果当前是黑棋 (B)，则切换为白棋 (W)；否则切换为黑棋 (B)。
      this.currentPlayer = (this.currentPlayer === CType.B) ? CType.W : CType.B
      // 更新提示框
      this.tip = (this.currentPlayer === CType.B) ? "黑方回合" : "白方回合"
    } else {
      this.tip = "无效走法" // 刷新提示栏
    }

    // 白方棋手为AI选手
    if (this.currentPlayer === CType.W) {
      // 上贪心加权重的自动落子
      const aiMove: Coordinate | null = this.gameLogic.findGreedyMove(CType.W, this.board)
      if (aiMove) {   // 有可以走的
        // 调用自己的方法更新棋盘，一次递归
        this.handleCellClick(aiMove.row, aiMove.col)
      }
    }

    // 当前棋手可落子的有效位置数量
    let possible_num = this.gameLogic.findAllValidMoves(this.currentPlayer, this.board).length
    // 当前棋手无棋可走，游戏结束
    if (possible_num === 0) {
      //分数转文本(不搞下面的太长了，难看，虽然已经很难看了)
      let result_msg: String = `(${this.blackScore}:${this.whiteScore})`
      // 弹出对话框
      this.getUIContext().showAlertDialog({
        // 判断谁无棋走
        message: (
          this.currentPlayer === CType.B ? `黑方无棋可走，${result_msg},` : `白方无棋可走，${result_msg}` ) +
          // 判断是否是平局
          (this.blackScore === this.whiteScore ? "平局" : (
            // 判断是哪方获胜
            this.blackScore > this.whiteScore ? "黑方获胜" : "白方获胜"
          ))
      })
      this.tip = "玩家黑方先手" // 重启时重置提示文本
      this.restartGame() // 直接重置棋盘
      // 重置双方分数
      this.blackScore = this.whiteScore = 0
    }
  }

  build() {
    Column() {
      // 游戏名
      Text(this.gameName)
        .fontSize(32)
        .fontWeight(FontWeight.Bold)
        .fontColor('#2C3E50')
        .padding({ top: 40, bottom: 20 })

      // 打架的地方
      Grid() {
        // 遍历棋盘的行数据
        ForEach(this.board, (rowItems: CType[], rowIndex: number) => {
          // 遍历每行内的棋子数据
          ForEach(rowItems, (piece: CType, colIndex: number) => {
            // 单个栏栅格样式
            GridItem() {
              // 这里是栈，也就是重叠样式
              Stack({ alignContent: Alignment.Center }) {
                // 棋盘格子按钮 (作为落子区域)
                Button()
                  .width('98%')
                  .aspectRatio(1)// 保持宽高比为1 (正方形)
                  .border({ width: 1, color: Color.Black, radius: 0 })// 边框 [cite: 799]
                  .backgroundColor("#ff2a81e9")// 棋盘落子颜色
                  .onClick(() => {
                    this.handleCellClick(rowIndex, colIndex) // 绑定点击事件
                  })

                // 棋子 (如果该位置有棋子)
                if (piece !== CType.E) {
                  Circle()
                    .width('80%')
                    .aspectRatio(1)// 根据棋子类型 (B/W) 填充颜色
                    .fill(piece === CType.B ? Color.Black : Color.White)
                }
              }
            }
          }, // 这里必须是字符串，箭头函数执行的结果必须为字符串
            (piece: CType, colIndex: number) => `${rowIndex}-${colIndex}`) // 内部循环的key
        }, // 这里也必须是字符串，箭头函数执行的结果必须为字符串
        ) // (rowItems: CType[], rowIndex: number) => `${rowIndex}`
      }
      .columnsTemplate('1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr') // 8列，每列等宽
      .rowsTemplate('1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr') // 8行，每行等高
      .width('100%') // 棋盘宽度占父容器100%
      .aspectRatio(1) // 保持正方形棋盘
      .padding(10) // 内边距10
      .backgroundColor(Color.Black) // 棋盘背景色
      // 额外
      .margin(10)
      .borderRadius(20)

      // 提示框
      Row() {
        // 黑方棋图标
        this.aiButton(Color.Black)

        // 黑方分数
        Text(this.blackScore.toString())
          .fontSize(30)
          .fontWeight(FontWeight.Bold)

        // 文本提示
        Text(this.tip)
          .fontSize(25)
          .fontWeight(FontWeight.Bold)

        // 白方分数
        Text(this.whiteScore.toString())
          .fontSize(30)
          .fontWeight(FontWeight.Bold)

        // 白色图标
        this.aiButton(Color.White)
      }
      .height("50")
      .width("95%")
      .padding({ left: 20, right: 20 })
      .margin({
        left: 10,
        top: 10,
        right: 10,
        bottom: 10
      })
      .backgroundColor(Color.Gray)
      .justifyContent(FlexAlign.SpaceBetween) // 设置间距策略
      .borderRadius(10)

      // 重置按钮
      Button("重新开始")
        .width("50%")
        .onClick(() => {
          this.tip = "玩家黑方先手" // 重启时重置提示文本
          this.restartGame() // 直接重置棋盘
          this.blackScore = this.whiteScore = 0 // 重置双方分数
        })

    }
    .height("100%")
    // linearGradient的api学习：https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-universal-attributes-gradient-color#lineargradient
    .linearGradient({
      angle: 135, //视频里面是左上到右下的颜色过度
      colors: [
        // 左上角的浅青色
        ['#AEEAE6', 0.0],
        // 渐变到中间的白色
        ['#FFFFFF', 0.3],
        // 底部和右侧的浅桃色
        ['#FEE9E7', 1]
      ]
    })
  }
}