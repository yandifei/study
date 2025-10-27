// 导包
import { CType, GameLogic, Coordinate } from '../logic/GameLogic';

@Entry
@Component
struct Index {
  @State board: CType[][] = [];
  @State currentPlayer: CType = CType.B;
  private gameName: string = '黑白棋';
  @State blackScore: number = 0;    // 黑棋分数
  @State whiteScore: number = 0;    // 白棋分数
  private gameLogic: GameLogic = new GameLogic();

  // 响应每个 Grid 单元格里Button 被点击后处理逻辑
  handleCellClick(row: number, col: number) {
    const moveResult = this.gameLogic.checkValidMove(row,col,this.currentPlayer, this.board);
    if (moveResult.isValid) {
      let newBoard: CType[][] = this.board.map(r => [...r]);
      newBoard[row][col] = this.currentPlayer;
      moveResult.piecesToFlip.forEach((coord: Coordinate) => {
        newBoard[coord.row][coord.col] = this.currentPlayer;
      });
      this.board = newBoard;
      let bScore = 0;
      let wScore = 0;
      newBoard.forEach(r => {
        r.forEach(c => {
          if (c === CType.B) bScore++;
          if (c === CType.W) wScore++;
        });
      });
      this.blackScore = bScore;
      this.whiteScore = wScore;
      this.currentPlayer = (this.currentPlayer === CType.B) ? CType.W :CType.B;}
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
    // ];

    this.currentPlayer = CType.B;
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
                  .width('12%') //  GridItem 宽度
                  .height('12%') // GridItem 高度
                    // 边框：黑色实线，无圆角 (radius: 0)
                  .border({ width: 1, color: Color.Black, radius: 0 })
                  .onClick(() => {
                    this.handleCellClick(rowIndex, colIndex);
                  })

                // 棋子 (如果该位置有棋子)
                if (piece !== CType.E) {
                  Circle()
                    .width('9%') // 棋子占格子宽度
                    .height('9%') // 棋子占格子高度
                      // 根据棋子类型 (B/W) 填充颜色
                    .fill(piece === CType.B ? Color.Black : Color.White)
                }
              }
            }
          },// 这里必须是字符串，箭头函数执行的结果必须为字符串
            (piece: CType, colIndex: number) => `${rowIndex}-${colIndex}`) // ForEach 的 Key
        }, // 这里也必须是字符串，箭头函数执行的结果必须为字符串
          (rowItems: CType[], rowIndex: number) => `row-${rowIndex}`) // ForEach 的 Key
      }
      .width('100%') // 棋盘宽度占父容器90%
      .aspectRatio(1) // 保持正方形棋盘
      .padding({left: 10, top: 10}) // 内边距10
      .backgroundColor(Color.Gray) // 棋盘背景色

      // 额外加的
      .borderRadius(10) //圆角
      .margin(10) //外边距


      // 分数记录自己画
      Row() {
        // 白色
        Blank()
          .backgroundColor(Color.Black)
          .width(10)

        // 黑棋
        Blank()
          .backgroundColor(Color.White)
          .width(10)

      }
      .width("100%")
      .backgroundColor(Color.Gray) //
    }
  }
}