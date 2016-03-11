from __future__ import print_function

'''
Implements Game class for connect-4
'''

width = 7
height = 6
directions = ['right', 'left', 'vertical', 'horizontal']
n = 4
finished = False

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

    def updateBoard(self, x, y, player):
        neighbors = [-1, 0, 1]
        for i in neighbors:
            for j in neighbors:
                if (x + i >= 0 and x + i < width) and (y + j >= 0 and y + j < height) and (i is not 0 or j is not 0):
                    updated_spot = self.state[x + i][y + j]
                    if updated_spot['player'] == player:
                        if abs(i + j) == 2:
                            self.state[x][y]['right'] += 1
                            updated_spot['right'] += 1
                        elif i + j == 0:
                            self.state[x][y]['left'] += 1
                            updated_spot['left'] += 1
                        elif j == 0:
                            self.state[x][y]['horizontal'] += 1
                            updated_spot['horizontal'] += 1
                        else:
                            self.state[x][y]['vertical'] += 1
                            updated_spot['vertical'] += 1

class Game:
    def __init__(self,a,b):
        self.player1 = a
        self.player2 = b
        
        #constuct empty board
        self.board = Board([[{'player':0,'right':0,'left':0,'vertical':0,'horizontal':0, 'x': j, 'y': i} for i in range(0,height)] for j in range(0,width)])

    def matchFour(self, list):
        global finished
        for k in range(0, len(list) - n + 1):
            if list[k] == 1:
                counter = 0
                for l in range(0, n - 2):
                    if list[k + l + 1] == 2:
                        counter += 1
                if counter == n - 2:
                    if list[k + n - 1] is not 0:
                        finished = True


    def findFour(self, x, y, direction, list):
        global finished
        if direction == 'vertical':
            bottom = max([-3, -1 * y])
            top = min([3, height - y - 1])
            for j in range(bottom, top + 1):
                list.append(self.board.state[x][y + j][direction])
        elif direction == 'horizontal':
            bottom = max([-3, -1 * x])
            top = min([3, width - x - 1])
            for j in range(bottom, top + 1):
                list.append(self.board.state[x + j][y][direction])
        elif direction == 'right':
            bottom = max([-3, -1 * y, -1 * x])
            top = min([3, height - y - 1, width - x - 1])
            for j in range(bottom, top + 1):
                list.append(self.board.state[x + j][y + j][direction])
        else:
            bottom = max([-3, y - height + 1, -1 * x])
            top = min([3, y, width - x - 1])
            for j in range(bottom, top + 1):
                list.append(self.board.state[x + j][y - j][direction])
        self.matchFour(list)



    def checkStatus(self, last_move, x, y):
        global finished
        for i in directions:
            if last_move[i] is not 0:
                list = []
                self.findFour(x, y, i, list)

    def play(self):
        global finished
        cur_player = 1
        turn = 1
        while not finished:
            move = self.player1(self.board) if cur_player is 1 else self.player2(self.board)
            desired_spot = self.board.state[move[0]][move[1]]
            #verify that slot is open, and position below it is filled
            if desired_spot['player'] is 0 and (move[1] is 0 or self.board.state[move[0]][move[1]-1]['player'] is not 0):
                desired_spot['player'] = cur_player
                self.board.updateBoard(move[0], move[1], cur_player)
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
            self.checkStatus(desired_spot, move[0], move[1])
            if finished is True:
                print("Player %d has won!" % cur_player)
            else:
                cur_player = 1 + (cur_player % 2)

            if turn is width * height:
                finished = True
                print("Tie Game!")
            else:
                turn += 1




Game(Hodor, Hodor).play()