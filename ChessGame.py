# coding:utf-8
from AlphaBataAlgorithm import *

class Chess():
    def __init__(self, color, point, uid):
        self.color = color
        self.point = point
        self.uid = uid
        self.is_dead=False


class ChessGame():
    def __init__(self):
        self.player_list = []
        self.board_list = []
        # 初始化棋局
        self.board = self.init_chess()
        # 存储初始化棋局
        self.board_list.append(self.board)
        #设置默认值
        self.current_player_color = "red"  # 默认玩家先行棋
        self.own_player_color = "black"  # 默认电脑执黑棋
        # 初始化双方棋子信息
        self.own_info = []
        self.foe_info = []
        self.init_player_info()
        self.alpha_beta_algorithm = AlphaBataAlgorithm()
        self.round = 0#棋局开始轮数为0

        self.directions = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                else:
                    self.directions.append(Vector(i, j))

    '''
    game_war:进行对局
    uid:玩家棋子编号
    point1:玩家棋子目标移动位置
    point2:玩家棋子释放障碍位置
    return:None
    '''
    def game_war(self, point, point1, point2):
        if (self.place_chess(point, point1, point2)):  # 玩家棋子走子、释放障碍完毕
            print "玩家走子:(" + str(point.x) +","+ str(point.y) + ")->(" + str(point1.x)+"," + str(point1.y) + ")->" + str(
                point2.x)+"," + str(point2.y) + ")"
            self.check_chess()
            if self.check_game_over(self.own_info):
                self.show_board()
                print "MSG:游戏结束，玩家胜"
                print "-------------"
                return
            self.reverse_player()
            self.change_depth()
            self.alpha_beta_algorithm.search(self.board,self.own_info,self.foe_info)
            point=self.alpha_beta_algorithm.point1
            point1=self.alpha_beta_algorithm.point2
            point2=self.alpha_beta_algorithm.point3
            if (self.place_chess(point, point1, point2)):
                print "电脑走子:(" + str(point.x) +","+ str(point.y) + ")->(" + str(point1.x) +","+ str(point1.y) + ")->" + str(
                    point2.x) +","+ str(point2.y) + ")"
                self.reverse_player()
                self.check_chess()
                if self.check_game_over(self.foe_info):
                    self.show_board()
                    print "MSG:游戏结束，AI胜"
                    return
                self.round += 1
                self.board_list.append(self.board)
                self.show_board()
            else:
                self.board = self.board_list[self.board_list.__len__() - 1]
                print "ERROR:电脑走子失败"
                self.show_board()
        else:
            print "ERROR:玩家走子失败"

    def check_chess_dead(self,chess_list):
        dead_list=[]
        for chess in chess_list:
            surround_barriers_num = 0
            for dx, dy in self.directions:
                x, y = chess.point.x + dx, chess.point.y + dy
                if (x > 9 or y > 9 or x < 0 or y < 0):
                    surround_barriers_num+=1
                    continue
                if (self.board[x][y] == -1):
                    surround_barriers_num += 1
            if(surround_barriers_num==8):
                dead_list.append(chess.uid)
        return dead_list

    def check_chess(self):
        dead_list=self.check_chess_dead(self.foe_info)
        for uid in dead_list:
            self.player_list[uid-1].is_dead=True
            for chess in self.foe_info:
                if(chess.uid==uid):
                    self.foe_info.remove(chess)

        dead_list=self.check_chess_dead(self.own_info)
        for uid in dead_list:
            self.player_list[uid-1].is_dead=True
            for chess in self.own_info:
                if(chess.uid==uid):
                    self.foe_info.remove(chess)


    def check_game_over(self,players):
        for player in players:
            if not player.is_dead:
                return False
        return True

    #根据棋局进行轮数改变遍历深度
    def change_depth(self):
        if (self.round < 8):
            self.alpha_beta_algorithm.depth = 1
        elif (self.round < 16):
            self.alpha_beta_algorithm.depth = 2
        elif (self.round < 24):
            self.alpha_beta_algorithm.depth = 4
        else:
            self.alpha_beta_algorithm.depth = 6



    # 调换执棋方
    def reverse_player(self):
        if (self.current_player_color == "red"):
            self.current_player_color = "black"
        else:
            self.current_player_color = "red"



    # owner_of_chess:判断棋子属于哪方
    def owner_of_chess(self, uid):
        return self.player_list[uid - 1].color



    '''
       is_able_to_put:是否符合走子规范
       point1:起始位置
       point2:结束位置
       return:True/False
       '''

    def is_able_to_put(self, point1, point2):
        for dx, dy in self.directions:
            x, y = point1.x + dx, point1.y + dy
            while (x < 10 and y < 10 and x >= 0 and y >= 0):
                if (self.board[x][y] != 0):
                    break
                elif (x == point2.x and y == point2.y):
                    return True
                else:
                    x, y = x + dx, y + dy
        return False



    '''
    place_chess:玩家棋子进行走子操作
    uid:棋子编号
    point1:棋子目标移动位置
    point2:棋子释放障碍位置
    return:True/False
    '''
    def place_chess(self, point, point1, point2):
        # 判断是否为当前执棋方的棋子
        play_chess=None
        uid=-1
        if(self.current_player_color=="black"):
            for chess in self.own_info:
                if(chess.point.x==point.x and chess.point.y==point.y):
                    uid=chess.uid
                    play_chess=chess
                    break
        else:
            for chess in self.foe_info:
                if(chess.point.x==point.x and chess.point.y==point.y):
                    uid=chess.uid
                    play_chess = chess
                    break

        if(uid==-1):
            print("ERROR:该坐标下的棋子无法移动或者该坐标下无棋子")
            return False
        if (self.owner_of_chess(uid) != self.current_player_color):
            print("ERROR:非当前玩家走子")
            return False
        if (self.is_able_to_put(point, point1)):
            print"MSG:当前编号为", uid, "的棋子走法符合规范"
            if (self.is_able_to_put(point1, point2)):
                self.board[point2.x][point2.y] = 9  # 释放障碍
                self.board[point1.x][point1.y] = uid
                self.board[point.x][point.y] = 0  # 移动棋子位置
                play_chess.point = point1  # 改变棋子信息
                self.check_chess()
                return True
            else:
                print("ERROR:障碍释放坐标有误")
        else:
            print "ERROR:当前编号为", uid, "的棋子走法不符合规范"
        return False

    # 显示当前棋盘信息
    def show_board(self):
        print "----------当前第", str(self.round), "轮棋盘信息----------"
        num = "  0  1  2  3  4  5  6  7  8  9"
        print num
        i = 0
        for msg in self.board:
            print str(i) + str(msg)
            i += 1
        print "======================================="

    # 初始化棋子棋子信息
    def init_player_info(self):
        if (self.own_player_color == "black"):
            for i in range(0, 4):
                self.own_info.append(self.player_list[i])
            for i in range(4, 8):
                self.foe_info.append(self.player_list[i])
        else:
            for i in range(0, 4):
                self.foe_info.append(self.player_list[i])
            for i in range(4, 8):
                self.own_info.append(self.player_list[i])

    # 初始化棋子信息
    def init_chess(self):
        map = [[0] * 10 for i in range(10)]
        map[0][3] = 1  # 黑棋
        map[0][6] = 2
        map[3][0] = 3
        map[3][9] = 4
        black0 = Point(0, 3)
        black1 = Point(0, 6)
        black2 = Point(3, 0)
        black3 = Point(3, 9)
        self.player_list.append(Chess("black", black0, 1))
        self.player_list.append(Chess("black", black1, 2))
        self.player_list.append(Chess("black", black2, 3))
        self.player_list.append(Chess("black", black3, 4))
        map[6][0] = 5  # 白棋
        map[6][9] = 6
        map[9][3] = 7
        map[9][6] = 8
        red0 = Point(6, 0)
        red1 = Point(6, 9)
        red2 = Point(9, 3)
        red3 = Point(9, 6)
        self.player_list.append(Chess("red", red0, 5))
        self.player_list.append(Chess("red", red1, 6))
        self.player_list.append(Chess("red", red2, 7))
        self.player_list.append(Chess("red", red3, 8))
        return map

