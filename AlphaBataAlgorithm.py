# coding:utf-8
import random
import ChessValue
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
Vector = namedtuple('Vector', ['dx', 'dy'])
#=================
MAX = 999
sx = [1,0,1,1,0,-1,-1,-1]
sy = [1,1,-1,0,-1,1,0,-1]
queenx = [0 for col in range(101)]
queeny = [0 for col in range(101)]
qdeep = [0 for col in range(101)]
mchess = ChessValue.V_chess()
dchess = ChessValue.V_chess()
#==================

class AlphaBataAlgorithm():
    def __init__(self):
        self.depth = 1  # 初始化深度为1
        self.directions = []
        self.own_info = []
        self.foe_info = []
        self.board = []
        self.point1 = None
        self.point2 = None
        self.point3 = None
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.round = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                else:
                    self.directions.append(Vector(i, j))


    def search(self,board,own_info,foe_info):
        self.own_info = own_info
        self.foe_info = foe_info
        self.board = board
        self.deep_search(0, self.beta)

    def deep_search(self, depth, lastmaxmin):
        if(depth==self.depth):
            return self.estimate()
        if(depth%2==0):
            maxmin = self.alpha
            for player in self.own_info:#选择棋子
                x1=player.point.x
                y1=player.point.y
                for dx, dy in self.directions:#对八个方向进行走子
                    x2, y2 =  x1+ dx, y1 + dy#选定第一个走子位置
                    while(x2 < 10 and y2 < 10 and x2 > -1 and y2 > -1):#在棋盘内
                        if (self.board[x2][y2] == 0):  # 当前位置为空，可以置放棋子
                            self.board[x2][y2] = player.uid
                            self.board[x1][y1] = 0
                            player.point=Point(x2,y2)
                            #释放障碍
                            for temp_dx, temp_dy in self.directions:  # 对八个方向进行走子
                                x3, y3 = x2 + temp_dx, y2 + temp_dy  # 选定第一个置放障碍位置
                                while (x3 < 10 and y3 < 10 and x3 > -1 and y3 > -1):  # 在棋盘内
                                    if (self.board[x3][y3] == 0):  # 当前位置为空，可以置放障碍
                                        self.board[x3][y3] = 9
                                        value=self.deep_search(depth+1,maxmin)
                                        self.board[x3][y3] = 0
                                        if(depth!=0):
                                            maxmin=max(value,maxmin)
                                        elif value>maxmin:
                                            maxmin=value
                                            self.point1=Point(x1,y1)#x1,y1为原来棋子位置
                                            self.point2=Point(x2,y2)#x2,y2为当前棋子位置
                                            self.point3 = Point(x3, y3)#x3,y3为障碍位置
                                        if maxmin>=lastmaxmin:
                                            self.board[x1][y1]=player.uid
                                            self.board[x2][y2]=0
                                            player.point=Point(x1,y1)
                                            return maxmin
                                    else:
                                        break
                                    x3, y3 = x3 + temp_dx, y3 + temp_dy
                            #释放障碍结束
                            self.board[x1][y1]=player.uid
                            self.board[x2][y2]=0
                            player.point = Point(x1, y1)
                        else:
                            break
                        x2, y2 = x2 + dx, y2 + dy
                    continue
            if (maxmin == self.alpha) :
                return self.estimate()
        else:#玩家进行行棋
            maxmin=self.beta
            for player in self.foe_info:#选择棋子
                x1=player.point.x
                y1=player.point.y
                for dx, dy in self.directions:#对八个方向进行走子
                    x2, y2 =  x1+ dx, y1 + dy#选定第一个走子位置
                    while(x2 < 10 and y2 < 10 and x2 > -1 and y2 > -1):#在棋盘内
                        if (self.board[x2][y2] == 0):  # 当前位置为空，可以置放棋子
                            self.board[x2][y2] = player.uid
                            self.board[x1][y1] = 0
                            player.point.x=x2
                            player.point.y=y2
                            #释放障碍
                            for temp_dx, temp_dy in self.directions:  # 对八个方向进行走子
                                x3, y3 = x2 + temp_dx, y2 + temp_dy  # 选定第一个置放障碍位置
                                while (x3 < 10 and y3 < 10 and x3 > -1 and y3 > -1):  # 在棋盘内
                                    if (self.board[x3][y3] == 0):  # 当前位置为空，可以置放障碍
                                        self.board[x3][y3] = 9
                                        value=self.deep_search(depth+1,maxmin)
                                        self.board[x3][y3] = 0
                                        maxmin=min(value,maxmin)
                                        if maxmin<=lastmaxmin:
                                            self.board[x1][y1]=player.uid
                                            self.board[x2][y2]=0
                                            player.point=Point(x1,y1)
                                            return maxmin
                                    else:
                                        break
                                    x3, y3 = x3 + temp_dx, y3 + temp_dy
                            #释放障碍结束
                            self.board[x1][y1]=player.uid
                            self.board[x2][y2]=0
                            player.point = Point(x1, y1)
                        else:
                            break
                        x2, y2 = x2 + dx, y2 + dy
                    continue
            if (maxmin == self.beta) :
                return self.estimate()
        return maxmin
    def estimate(self):
        # return random.randint(0,1000)
        t1 = 0.00
        t2 = 0.00
        p1 = 0.00
        p2 = 0.00
        m = 0.00
        mchess._init_chess(1,self.board)
        dchess._init_chess(0,self.board)
        mchess.init_chess()
        dchess.init_chess()
        mchess.qMove()
        mchess.kMove()
        dchess.kMove()
        dchess.qMove()

        for i in range(10):
            for j in range(10):
                if(mchess.queen[j][i] > 1):continue
                mm = 0
                for p in range(8):
                    if(ChessValue.isout(i+sx[p],j+sy[p])): continue
                    if(self.board[i+sx[p]][j+sy[p]]):continue
                    mm+=1
                m+=mm/mchess.king[i][j]

        for i in range(10):
            for j in range(10):
                if(mchess.king[i][j] > dchess.king[i][j]): t1 += -1
                else:
                    if(mchess.king[i][j] < dchess.king[i][j]): t1 += 1
                    else:
                        if(mchess.king[i][j] == max):t1 += 0
                        else: t1 += 0.17

            for j in range(10):
                if(mchess.queen[i][j] > dchess.queen[i][j]): t2 += -1
                else:
                    if(mchess.queen[i][j] < dchess.queen[i][j]): t2 += 1
                    else:
                        if(mchess.queen[i][j] == max):t2 += 0
                        else: t2 += 0.17
                p1 += 2.0*(pow(2.0,-1*mchess.queen[i][j])-pow(2.0,-1*dchess.queen[i][j]))
                p2 += min(1.0,max(-1.0,(dchess.king[i][j] - mchess.king[i][j]/6.0)))
        if(self.round < 7):
            vv = 0.24*t1 + 0.47*t2 + 0.13*p1 + 0.13*p2 + 0.20*m
        else:
            if(self.round <= 16):
                vv = 0.30*t1 + 0.25*t2 + 0.30*p1 + 0.30*p2 + 0.05*m
            else:
                vv = 0.8*t1 + 0.1*t2 + 0.1*p1 + 0.1*p2
        return vv