import { CType, GameLogic, Coordinate } from './GameLogic'; // 导入 CType, GameLogic 和 Coordinate
import * as readline from 'readline'; // 导入 readline 模块用于处理命令行输入

// 创建 readline 接口用于接收用户输入
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// 创建游戏逻辑实例
const game = new GameLogic();

/**
 * 在控制台打印当前棋盘状态
 */
function printBoard(board: CType[][]) {
  console.log('\n 0 1 2 3 4 5 6 7');
  console.log(' +-----------------+');
  for (let i = 0; i < 8; i++) {
    let rowStr = `${i}|`;
    for (let j = 0; j < 8; j++) {
      switch (board[i][j]) {
        case CType.B: rowStr += ' ⬤'; break; // 黑棋 (Nerd Font: nf-fa-circle)
        case CType.W: rowStr += ' ◯'; break; // 白棋 (Nerd Font: nf-fa-circle_o)
        default: rowStr += ' ·'; break; // 空
      }
    }
    console.log(rowStr + ' |');
  }
  console.log(' +-----------------+');
}

/**
 * 提示玩家输入并返回坐标（行,列）
 */
function promptMove(player: CType): Promise<Coordinate> {
  const playerName = player === CType.B ? '黑棋' : '白棋';
  const playerIcon = player === CType.B ? '⬤' : '◯';

  return new Promise((resolve) => {
    rl.question(`轮到【${playerIcon} ${playerName}】走，请输入坐标 (格式: 行,列): `,
      (input: string) => { // <<-- 修复 TS7006: 明确类型为 string
        const parts = input.split(',');
        if (parts.length !== 2) {
          console.log('输入格式错误，请重新输入！');
          return resolve(promptMove(player));
        }
        const row = parseInt(parts[0], 10);
        const col = parseInt(parts[1], 10);

        if (isNaN(row) || isNaN(col) || row < 0 || row > 7 || col < 0 || col > 7) {
          console.log('坐标超出范围，请重新输入！');
          return resolve(promptMove(player));
        }
        resolve(new Coordinate(row, col));
      });
  });
}

/**
 * 游戏主循环
 */
async function gameLoop() {
  // 修改游戏标题为“AI 黑白棋”
  console.log("AI 黑白棋游戏-命令行版");

  let board: CType[][] = [ // 初始化棋盘
    [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
    [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
    [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
    [CType.E, CType.E, CType.E, CType.W, CType.B, CType.E, CType.E, CType.E],
    [CType.E, CType.E, CType.E, CType.B, CType.W, CType.E, CType.E, CType.E],
    [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
    [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
    [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E],
  ];

  let currentPlayer: CType = CType.B; // 初始玩家为黑棋 (玩家)

  while (true) {
    printBoard(board);

    const opponent: CType = currentPlayer === CType.B ? CType.W : CType.B; // <<-- 修复 TS7022: 明确类型为 CType
    const playerValidMoves = game.findAllValidMoves(currentPlayer, board); // 检查当前玩家的有效走法
    const opponentValidMoves = game.findAllValidMoves(opponent, board); // 检查对手的有效走法

    // 游戏结束条件：双方都无棋可走
    if (playerValidMoves.length === 0 && opponentValidMoves.length === 0) {
      console.log('游戏结束！双方均无有效走法。');
      break;
    }

    // 如果当前玩家无棋可走，则轮到对方
    if (playerValidMoves.length === 0) {
      const playerName = currentPlayer === CType.B ? '黑棋' : '白棋';
      const playerIcon = currentPlayer === CType.B ? '⬤' : '◯';
      console.log(`【${playerIcon} ${playerName}】无有效走法，跳过此回合。`);
      currentPlayer = opponent;
      continue;
    }

    let move: Coordinate | null = null;
    let moveResult = null;

    if (currentPlayer === CType.B) { // 玩家回合
      while (true) {
        move = await promptMove(currentPlayer);
        moveResult = game.checkValidMove(move.row, move.col, currentPlayer, board);

        if (moveResult.isValid) {
          board = game.applyMove(board, move, moveResult.piecesToFlip, currentPlayer);
          break;
        } else {
          console.log('无效的走法，请重新选择位置！');
        }
      }
    } else { // AI 回合 (白棋)
      console.log(`轮到【◯ 白棋】(AI)走...`);

      // 使用 AI 贪心算法选择走法
      move = game.findGreedyMove(currentPlayer, board);

      if (move) {
        console.log(`AI 选择走在 (${move.row}, ${move.col})`);
        moveResult = game.checkValidMove(move.row, move.col, currentPlayer, board);
        // 注意：由于 findGreedyMove 保证了 move 是有效的，这里可以直接应用走法
        board = game.applyMove(board, move, moveResult.piecesToFlip, currentPlayer);
      }
      // 如果 AI 无棋可走，则 move 为 null，但已经在前面的 playerValidMoves 检查中处理
    }

    // 切换玩家
    currentPlayer = opponent;
  }

  // 游戏结束后计分
  let blackCount = 0;
  let whiteCount = 0;
  for (const row of board) {
    for (const cell of row) {
      if (cell === CType.B) blackCount++;
      if (cell === CType.W) whiteCount++;
    }
  }

  console.log(`\n--- 最终得分 ---`);
  console.log(` ⬤ 黑棋: ${blackCount}`);
  console.log(` ◯ 白棋: ${whiteCount}`);

  if (blackCount > whiteCount) {
    console.log('恭喜，你赢了！');
  } else if (whiteCount > blackCount) {
    console.log('很遗憾，AI 赢了。');
  } else {
    console.log('平局！');
  }

  rl.close(); // 关闭 readline 接口
}

// 启动游戏
gameLoop();