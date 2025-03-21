/*MiGong.java -- 老鼠迷宫*/
public class MiGong {
	public static void main(String[] args) {
		//小球得到的路径

		//思路
		//1. 设置二维数组表示迷宫，用二维数组表示，int[][] map = new int[8][7];
		//2. 先表示map数组的元素值：0 表示可以走，1 表示障碍物
		int[][] map = new int[8][7];
		//3. 将最上面的一行和最下面的一行，全部设置为1
		for(int i = 0; i < 7; i++) {
			map[0][i] = 1;
			map[7][i] = 1;
		}
		//将最右面的一列和最左面的一列，全部设置为1
		for(int i = 0; i < 8; i++) {
			map[i][0] = 1;
			map[i][6] = 1; 
		}



		//输出当前的地图
		System.out.println("===========当前地图情况==========");
		for(int i = 0; i < map.length; i++) {
			for(int j = 0; j < map[i].length; j++) {
				System.out.print(map[i][j] + " "); //输出一行
			}
			System.out.println();
		}

		//使用findway给老鼠找路
		T t1 = new T();
		t1.findway(map, 1, 1);

		System.out.println("\n==========找路的情况如下==========");
		for(int i = 0; i < map.length; i++) {
			for(int j = 0; j < map[i].length; j++) {
				System.out.print(map[i][j] + " "); //输出一行
			}
			System.out.println();
		}


	}
}

class T {
	//使用递归回溯的思想来解决老鼠出迷宫
	//1. findway方法就是专门来找迷宫的路径
	//2. 如果过找到就返回true，否则返回false
	//3. map就是二维数组，即表示迷宫
	//4. i，j 就是老鼠的位置，初始化的位置为(1,1)
	//5. 因为我们是递归的找路，所以我先规定，map数组的各个值的含义
	//	0 表示可以走，1 表示障碍物， 2 表示可以走， 3表示走过，但是走不通是死路
	//6. 当map[0][5] = 2 就说明找到通路就可以结束，否则就继续找。
	//7. 先确定老鼠找路策略，下->右->上->左
	public boolean findway(int[][] map, int i, int j) {
		if(map[6][5] == 2) { //说明已经找到
			return true;
		} else {
			if(map[i][j] == 0) { //当前这个位置为0，说明表示可以走 
				//我们假定可以走通
				map[i][j] = 2;
				//下->右->上->左
				if(findway(map, i + 1, j)) { //先坐下
					return true;
				} else if(findway(map, i, j + 1)) { //右
					return true;
				} else if(findway(map, i - 1, j)) { //上
					return true;
				} else if(findway(map, i, j - 1)) { //左
					return true;
				} else{
					map[i][j] = 3;
					return false;
				}
			} else {	//map[i][j] = 1, 2, 3
				return false;
			}
		}
	}
}