from __future__ import print_function

'''
Implements Game class for connect-4
'''

width = 7
height = 6

#stupid bot, finds first available open spot
def Hodor(board):
    for j in range(0,height):
        for i in range (0,width):
            if board.state[i][j]['player'] is 0:
                return [i,j]

class Board:
    def __init__(self, state):
        self.state = state
    
    def printBoard(self):
        for j in range(0,height):
            for i in range(0,width):
                if self.state[i][height-j-1]['player'] is 0:
                    print("O",end="")
                elif self.state[i][height-j-1]['player'] is 1:
                    print("*",end="")
                else:
                    print("@",end="")
            print("")
                

class Game:
    def __init__(self,a,b):
        self.player1 = a
        self.player2 = b
        
        #constuct empty board
        self.board = Board([[{'player':0,'right':0,'left':0,'vertical':0,'horizontal':0} for i in range(0,height)] for i in range(0,width)])

    def play(self):
        finished = False
        cur_player = 1
        turn = 1
        while not finished:
            move = self.player1(self.board) if cur_player is 1 else self.player2(self.board)
            
            #verify that slot is open, and position below it is filled
            if self.board.state[move[0]][move[1]]['player'] is 0 and (move[1] is 0 or self.board.state[move[0]][move[1]-1]['player'] is not 0):
                self.board.state[move[0]][move[1]]['player'] = cur_player
                '''
                if move[0] is not 0:
                    self.board[move[0]][move[1]]['vertical'] = self.board[move[0]-1][move[1]]['vertical'] + 1
                if 
                '''
            else:
                print("Invalid move by player %d\n" % cur_player)
                continue

            print("Turn %d: Printing current board..." % turn)
            self.board.printBoard()
            
            if turn is 20:
                finished is True
            else:
                turn += 1

            if finished is True:
                print("Player %d has won!" % cur_player)
            else:
                cur_player = 1 + (cur_player % 2)

    
