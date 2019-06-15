# coding:utf-8
from ChessGame import *
game=ChessGame()
game.show_board()
round=0
while(round<20):
    # try:
        player_msg=input('请输入你所选择移动的棋子的坐标,移动后棋子的坐标，释放障碍的坐标：\n')
        game.game_war(Point(int(player_msg[0]),int(player_msg[1])),Point(int(player_msg[2]),int(player_msg[3])),Point(int(player_msg[4]),int(player_msg[5])))
        round += 1
    # except:
    #     print "输入有误请重新输入"

# 6,0,3,3,1,1
# 3,3,2,2,2,3

