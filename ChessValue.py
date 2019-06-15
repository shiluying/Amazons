# coding:utf-8
MAX = 999
sx = [1,0,1,1,0,-1,-1,-1]
sy = [1,1,-1,0,-1,1,0,-1]

class V_chess():
    def __init__(self):
        self.player = 2 #黑棋 1 白棋 0
        self.x = []
        self.y = []
        self.queen = []
        self.king = []
        self.chess_map = None

    def _init_chess(self,player,chess_map):
        self.player = player #黑棋 1 白棋 0
        self.chess_map = chess_map

    def init_chess(self):
        for k in range(10):
            for j in range(10):
                if(self.chess_map[k][j] >0 and self.chess_map[k][j] <= 4):
                    p = 1
                else:
                    if(self.chess_map[j][k] > 4 and self.chess_map[k][j] < 9):
                        p = 0
                    else:
                        p = -1
                if(p == self.player):
                        self.x.append(k)
                        self.y.append(j) 

    def kMove(self):
        self.king = [[MAX for col in range(10)] for row in range(10)]
        for z in range(4):
            bj = [[0 for col in range(10)] for row in range(10)]
            queenx = [0 for col in range(101)]
            queeny = [0 for col in range(101)]
            qdeep = [0 for col in range(101)]
            top = 0
            end = 1
            queenx[0] = self.x[z]
            queeny[0] = self.y[z]
            qdeep[0] = 0
            bj[self.x[z]][self.y[z]] = 1
            while(top!=end):
                x = queenx[top]
                y = queeny[top]
                deep = qdeep[top]
                self.king[x][y] = min(self.king[x][y],deep)
                for i in range(8):
                    if(isout(x+sx[i],y+sy[i])): continue
                    if(bj[x+sx[i]][y+sy[i]]): continue
                    if(self.chess_map[x+sx[i]][y+sy[i]]):continue
                    queenx[end] = x + sx[i]
                    queeny[end] = y + sy[i]
                    qdeep[end] = deep + 1
                    bj[x+sx[i]][y+sy[i]] = 1
                    end+=1
                top+=1    
            self.king[self.x[z]][self.y[z]] = MAX

    def qMove(self):
        self.queen = [[MAX for col in range(10)] for row in range(10)]
        for z in range(4):
            bj = [[0 for col in range(10)] for row in range(10)]
            queenx = [0 for col in range(101)]
            queeny = [0 for col in range(101)]
            qdeep = [0 for col in range(101)]
            top = 0
            end = 1
            queenx[0] = self.x[z]
            queeny[0] = self.y[z]
            qdeep[0] = 0
            bj[self.x[z]][self.y[z]] = 1
            while(top!=end):
                x = queenx[top]
                y = queeny[top]
                deep = qdeep[top]
                self.queen[x][y] = min(self.queen[x][y],deep)
                for i in range(8):
                    for p in range(50):
                        if(isout(x+p*sx[i],y+p*sy[i])): break
                        if(bj[x+p*sx[i]][y+p*sy[i]]): continue
                        if(self.chess_map[x+p*sx[i]][y+p*sy[i]]):break
                        queenx[end] = x + p*sx[i]
                        queeny[end] = y + p*sy[i]
                        qdeep[end] = deep + 1 
                        bj[x+p*sx[i]][y+p*sy[i]] = 1
                        end+=1
                top+=1
            self.queen[self.x[z]][self.y[z]] = MAX

def isout(x,y):
    if(x<0 or x>=10 or y<0 or y>=10):
        return 1
    else:
        return 0