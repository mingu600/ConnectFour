from __future__ import print_function
import connect4game as c4
import math as m
import time

neighbors = [-1,0,1]
#bot that takes board state c4 game and chooses a move

#return all valid moves for a given board state
def find_moves(board):
    valid = []
    for i in range(0,c4.width):
        for j in range(0, c4.height):
            if board.state[i][j]['player'] is 0 and (j is 0 or board.state[i][j-1]['player'] is not 0):
                valid.append((i,j))
                break
    return valid

#evaluate the board position for a player, returns in the form [winning_move, position_strength]
def eval(board, player, valid_moves, off_turn = False):
    strength = 0
    #hard-coded variable to indicate if game is over
    closed = False
    #loop over every entry in the board
    for i in range(0,c4.width):
        for j in range(0,c4.height):
            if board.state[i][j]['player'] is player:
                #check all neighbors
                for k in neighbors:
                    for l in neighbors:
                        #if neighboring space is empty, evaluate closeness c4
                        if not (l is 0 and k is 0) and not (i + k < 0 or i + k > c4.width-1 or j + l < 0 or j + l > c4.height-1 ):
                            filled = 1
                            viable = True
                            for slot in range(1,c4.n):
                                if i + slot*(-k) < 0 or i + slot*(-k) > c4.width-1 or j + slot*(-l) < 0 or j + slot*(-l) > c4.height-1 or board.state[i+slot*(-k)][j+slot*(-l)]['player'] is not player:
                                    break
                                else:
                                    filled+=1
                            for slot in range(1,c4.n-filled+1):
                                if i + slot*(k) < 0 or i + slot*(k) > c4.width-1 or j + slot*(l) < 0 or j + slot*(l) > c4.height-1 or board.state[i+slot*(k)][j+slot*(l)]['player'] is 1+(player%2):
                                    viable = False
                                    break
                                elif  board.state[i+slot*(k)][j+slot*(l)]['player'] is player:
                                    filled+=1
                            #score of individual position
                            '''
                            if filled is 3 and (i + k, j + l) in valid_moves):
                                return [(i + k, j + l), None]
                            
                            else:
                            '''
                            #heuristic to weight towards fewer bigger sequences
                            if viable:
                                if filled is c4.n:
                                    strength += 100000
                                    closed = True
                                elif filled is c4.n-1 and off_turn and (i + k,j + l) in valid_moves:
                                    strength += 10000
                                    closed = True
                                strength += filled**1.5

    return [closed, strength]

#returns tuple of best move and score                             
def choose(board, player, depth):
    valid = find_moves(board)

    best_move = None
    best_score = None
    for move in valid:
        #hacky workaround using same object, lookup how to copy object when home
        board.state[move[0]][move[1]]['player'] = player
        new_valid = find_moves(board)
        dif = None
        score1 = eval(board,player,new_valid)
        score2 = eval(board,1 + (player % 2), new_valid, True)
        #if we have reached bottom of game tree or is losing position, return evaluation
        if depth is 1:
            dif = score1[1] - score2[1]
        #if we have a winning move, stop recursing from this level
        #if we have a losing move, stop going down this path but not this level
        elif score1[0] or score2[0]:
            dif = score1[1] - score2[1]
            if dif > 0:
                depth = 1
        else:
            opp = choose(board, 1 + (player % 2), 1)
            board.state[opp[0][0]][opp[0][1]]['player'] = 1 + (player % 2)
            dif = choose(board, player, depth-1)[1]
            board.state[opp[0][0]][opp[0][1]]['player'] = 0
#reverse the hack
        board.state[move[0]][move[1]]['player'] = 0
       
#print("Move: %d,%d Score: %f; " % (move[0],move[1],dif),end="")
        if dif > best_score:
            best_move = move
            best_score = dif

    print("")
    ret = (best_move, best_score)
    print("Choosing: %s" % repr(ret))
    return (best_move, best_score)



def robbot(board, player = 1):
    start = time.time()
    choice = choose(board, player, 3)[0]
    print("Time to choose: %f" % (time.time() - start))
    return choice
 
