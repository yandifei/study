// 定义棋盘上格子的三种状态：E (Empty) - 空，B (Black) - 黑棋，W (White) - 白棋
export enum CType {
  E, // 空
  B, // 黑棋
  W // 白棋
}

// 根据 ArkTS 的严格模式要求，使用 class 来定义坐标
export class Coordinate {
  row: number; // 行
  col: number; // 列
  constructor(row: number, col: number) {
    this.row = row;
    this.col = col;
  }
}


// 使用 class 来定义 每一步落子后的结果
export class MoveCheckResult {
  isValid: boolean; // 标记当前走法是否有效
  piecesToFlip: Coordinate[]; // 记录如果当前走法有效，可以翻转的对方棋子坐标列表
  constructor(isValid: boolean, piecesToFlip: Coordinate[]) {
    this.isValid = isValid;
    this.piecesToFlip = piecesToFlip;
  }
}

// 游戏核心逻辑类
export class GameLogic {
  // 定义 8 个方向的坐标偏移量，用于检查棋子周围的情况
  private directions: Coordinate[] = [
    new Coordinate(-1, 0), new Coordinate(1, 0), // 上、下
    new Coordinate(0, -1), new Coordinate(0, 1), // 左、右
    new Coordinate(-1, -1), new Coordinate(-1, 1), // 左上、右上(对角线)
    new Coordinate(1, -1), new Coordinate(1, 1)// 左下、右下 (对角线)
  ];

  /**
   * AI 逻辑：从所有有效落子位置中随机选择一个
   * @param player - AI 玩家的棋子类型 (B 或 W)
   * @param board - 当前的 8x8 棋盘状态
   * @returns 返回一个随机选择的有效落子坐标，如果没有有效走法则返回null
   * */
  public findRandomMove(player: CType, board: CType[][]): Coordinate | null {
    const validMoves = this.findAllValidMoves(player, board);
    if (validMoves.length === 0) {
      return null; // 没有有效走法
    }
    const randomIndex = Math.floor(Math.random() * validMoves.length);
    return validMoves[randomIndex];
  }

  /**
   * 找出指定玩家所有有效的落子位置
   * @param player - 当前玩家的棋子类型 (B 或 W) * @param board - 当前的 8x8 棋盘状态
   * @returns 返回一个包含所有有效落子坐标的数组
   */
  public findAllValidMoves(player: CType, board: CType[][]): Coordinate[] {
    const validMoves: Coordinate[] = [];
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        if (board[row][col] === CType.E) {
          const result = this.checkValidMove(row, col, player, board);
          if (result.isValid) {
            validMoves.push(new Coordinate(row, col));
          }
        }
      }
    }
    return validMoves;
  }

  /**
   * 检查在给定的坐标落子是否为一步有效的走法
   * @param row - 落子的行号
   * @param col - 落子的列号
   * @param player - 当前玩家的棋子类型 (B 或 W) * @param board - 当前的 8x8 棋盘状态
   * @returns MoveCheckResult - 包含走法是否有效以及可翻转棋子列表的对象
   * */

  public checkValidMove(row: number, col: number, player: CType, board: CType[][]): MoveCheckResult {
    // 规则 1：落子的位置必须是空的
    if (board[row][col] !== CType.E) {
      return new MoveCheckResult(false, []); // 如果非空，直接返回无效
    }
    // 确定对手的棋子类型
    const opponent: CType = player === CType.B ? CType.W : CType.B;
    // 用于存储所有可以被翻转的棋子
    let allPiecesToFlip: Coordinate[] = [];

    // 规则 2：遍历 8 个方向，检查是否能形成“夹击”
    for (const dir of this.directions) {
      // 存储当前方向上可能被翻转的棋子
      let piecesInThisLine: Coordinate[] = [];
      // 从落子点的邻近点开始沿当前方向检查
      let currentRow = row + dir.row;
      let currentCol = col + dir.col;
      // 只要还在棋盘内，并且遇到的是对手的棋子，就继续沿该方向前进
      while (currentRow >= 0 && currentRow < 8 && currentCol >= 0 && currentCol < 8 &&
        board[currentRow][currentCol] === opponent) {
        // 将这个对手棋子的坐标记录下来
        piecesInThisLine.push(new Coordinate(currentRow, currentCol));
        currentRow += dir.row;
        currentCol += dir.col;
      }
      // 循环结束后，如果仍在棋盘内，并且遇到了自己的棋子，说明形成了有效的“夹击”
      if (currentRow >= 0 && currentRow < 8 && currentCol >= 0 && currentCol < 8 &&
        board[currentRow][currentCol] === player) {
        // 只有在中间有对手棋子时，这个方向的走法才算有效
        if (piecesInThisLine.length > 0) {
          // 将这个方向上所有可翻转的棋子添加到总列表中
          allPiecesToFlip.push(...piecesInThisLine);
        }
      }

      // 规则 3：如果总的可翻转棋子列表不为空，说明这是一个有效的走法
      if (allPiecesToFlip.length > 0) {
        return new MoveCheckResult(true, allPiecesToFlip);
      }
    }
    // 如果遍历完所有方向都没有可翻转的棋子，则为无效走法
    return new MoveCheckResult(false, []);
  }

  /**
   * 将一步棋应用到棋盘上，并翻转相应的棋子
   * @param board - 当前的 8x8 棋盘状态
   * @param move - 要执行的落子坐标
   * @param piecesToFlip - 需要翻转的棋子坐标列表
   * @param player - 当前玩家的棋子类型 (B 或 W) * @returns 返回更新后的棋盘状态
   */

  public applyMove(board: CType[][], move: Coordinate, piecesToFlip: Coordinate[], player:
  CType): CType[][] {
    // 创建棋盘的深拷贝以避免直接修改原棋盘
    const newBoard = board.map(row => [...row]);
    // 在指定位置落子
    newBoard[move.row][move.col] = player;
    // 翻转所有“夹击”的棋子
    for (const piece of piecesToFlip) {
      newBoard[piece.row][piece.col] = player;
    }
    return newBoard;
  }

  // 8x8 棋盘上每个位置的战略价值分数
  private static readonly positionalValueMatrix = [
    [120, -20, 20, 5, 5, 20, -20, 120], // 角
    [-20, -40, -5, -5, -5, -5, -40, -20], // 边的旁边
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120]
  ];
  // // 16x16 棋盘上每个位置的战略价值分数
  // private static readonly positionalValueMatrix = [
  //   [120, 120, -20, -20, 20, 20, 5, 5, 5, 5, 20, 20, -20, -20, 120, 120],
  //   [120, 120, -20, -20, 20, 20, 5, 5, 5, 5, 20, 20, -20, -20, 120, 120],
  //   [-20, -20, -40, -40, -5, -5, -5, -5, -5, -5, -5, -5, -40, -40, -20, -20],
  //   [-20, -20, -40, -40, -5, -5, -5, -5, -5, -5, -5, -5, -40, -40, -20, -20],
  //   [20, 20, -5, -5, 15, 15, 3, 3, 3, 3, 15, 15, -5, -5, 20, 20],
  //   [20, 20, -5, -5, 15, 15, 3, 3, 3, 3, 15, 15, -5, -5, 20, 20],
  //   [5, 5, -5, -5, 3, 3, 3, 3, 3, 3, 3, 3, -5, -5, 5, 5],
  //   [5, 5, -5, -5, 3, 3, 3, 3, 3, 3, 3, 3, -5, -5, 5, 5],
  //   [5, 5, -5, -5, 3, 3, 3, 3, 3, 3, 3, 3, -5, -5, 5, 5],
  //   [5, 5, -5, -5, 3, 3, 3, 3, 3, 3, 3, 3, -5, -5, 5, 5],
  //   [20, 20, -5, -5, 15, 15, 3, 3, 3, 3, 15, 15, -5, -5, 20, 20],
  //   [20, 20, -5, -5, 15, 15, 3, 3, 3, 3, 15, 15, -5, -5, 20, 20],
  //   [-20, -20, -40, -40, -5, -5, -5, -5, -5, -5, -5, -5, -40, -40, -20, -20],
  //   [-20, -20, -40, -40, -5, -5, -5, -5, -5, -5, -5, -5, -40, -40, -20, -20],
  //   [120, 120, -20, -20, 20, 20, 5, 5, 5, 5, 20, 20, -20, -20, 120, 120],
  //   [120, 120, -20, -20, 20, 20, 5, 5, 5, 5, 20, 20, -20, -20, 120, 120]
  // ];

  /**
   * AI 贪心算法：基于位置价值选择最佳走法
   * @param player - AI 玩家的棋子类型 (B 或 W)
   * @param board - 当前的 8x8 棋盘状态
   * @returns 返回价值最高的有效落子坐标，如果没有有效走法则返回 null
   */
  public findGreedyMove(player: CType, board: CType[][]): Coordinate |
  null {
    const validMoves = this.findAllValidMoves(player, board);
    if (validMoves.length === 0) {
      return null;
    }
    let bestScore = -Infinity;
    let bestMoves: Coordinate[] = [];
    for (const move of validMoves) {
      const score = GameLogic.positionalValueMatrix[move.row][move.col];
      if (score > bestScore) {
        bestScore = score;
        bestMoves = [move];
      } else if (score === bestScore) {
        bestMoves.push(move);
      }
    }
    // 如果有多个价值相同的最佳走法，从中随机选择一个，让 AI 行为不那么固定
    const randomIndex = Math.floor(Math.random() * bestMoves.length);
    return bestMoves[randomIndex];
  }


}