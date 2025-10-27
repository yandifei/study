import { CType, GameLogic, Coordinate } from './GameLogic';
import * as readline from 'readline';
// 创建 readline 接口用于接收用户输入
const rl = readline.createInterface({
  input: process.stdin, output: process.stdout
});
// 创建游戏逻辑实例
const game = new GameLogic();
/**
 * 提示玩家输入并返回坐标
 */
function promptMove(player: CType): Promise<Coordinate> {
  const playerName = player === CType.B ? '黑棋' : '白棋';
  const playerIcon = player === CType.B ? ' ' : ' ';
  return new Promise((resolve) => {
    rl.question(`轮到【${playerIcon} ${playerName}】走，请输入坐标(格式: 行,列): `, (input) => {
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
  console.log("黑白棋游戏-命令行版")
  let board: CType[][] = [
    [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E], [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E], [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E], [CType.E, CType.E, CType.E, CType.W, CType.B, CType.E, CType.E, CType.E], [CType.E, CType.E, CType.E, CType.B, CType.W, CType.E, CType.E, CType.E], [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E], [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E], [CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E, CType.E], ];
  let currentPlayer = CType.B; // 黑棋（玩家）先走
  while (true) {
    printBoard(board);
    const playerValidMoves = game.findAllValidMoves(currentPlayer, board);
    const opponent: CType = currentPlayer === CType.B ? CType.W : CType.B;
    const opponentValidMoves = game.findAllValidMoves(opponent, board);
    // 游戏结束条件：双方都无棋可走
    if (playerValidMoves.length === 0 && opponentValidMoves.length === 0) {
      console.log('游戏结束！双方均无有效走法。');
      break;
    }
    // 如果当前玩家无棋可走，则轮到对方
    if (playerValidMoves.length === 0) {
      const playerName = currentPlayer === CType.B ? '黑棋' : '白棋';
      const playerIcon = currentPlayer === CType.B ? ' ' : ' ';
      console.log(`【${playerIcon} ${playerName}】无有效走法，跳过此回合。`);
      currentPlayer = opponent;
      continue;
    }
    let move: Coordinate | null;
    if (currentPlayer === CType.B) { // 玩家回合
      while (true) {
        move = await promptMove(currentPlayer);
        const moveResult = game.checkValidMove(move.row, move.col, currentPlayer, board);
        if (moveResult.isValid) {
          board = game.applyMove(board, move, moveResult.piecesToFlip, currentPlayer);
          break;
        } else {
          console.log('无效的走法，请重新选择位置！');
        }
      }
    } else { // AI 回合
      console.log(`轮到【 白棋】(AI)走...`);
      move = game.findRandomMove(currentPlayer, board);
      if (move) {
        console.log(`AI 选择走在 (${move.row}, ${move.col})`);
        const moveResult = game.checkValidMove(move.row, move.col, currentPlayer, board);
        board = game.applyMove(board, move, moveResult.piecesToFlip, currentPlayer);
      }
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
  console.log(` 黑棋: ${blackCount}`);
  console.log(` 白棋: ${whiteCount}`);
  if (blackCount > whiteCount) {
    console.log('恭喜，你赢了！');
  } else if (whiteCount > blackCount) {
    console.log('很遗憾，AI 赢了。');
  } else {
    console.log('平局！');
  }
  rl.close();
}