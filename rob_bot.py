import connect4game as c4
import math as m

neighbors = [-1,0,1]
#bot that takes board state c4 game and chooses a move

#return all valid moves for a given board state
def find_moves(board):
    valid = []
    for i in range(0,c4.width):
        for j in range(0, c4.height):
            if board.state[i][j]['player'] is 0 and (j is 0 or board.state[i][j-1]['player'] is not 0):
                valid.append((i,j))
    return valid

#evaluate the board position for a player, returns in the form [winning_move, position_strength]
def eval(board, player, valid_moves):
    strength = 0
    #loop over every entry in the board
    for i in range(0,c4.width):
        for j in range(0,c4.height):
            if board.state[i][j]['player'] is player:
                #check all neighbors
                for k in neighbors:
                    for l in neighbors:
                        #if neighboring space is empty, evaluate closeness c4
                        if not (l is 0 and k is 0) and not (i + k < 0 or i + k > c4.width-1 or j + l < 0 or j + l > c4.height-1 ) and board.state[k][l]['player'] is 0:
                            filled = 1
                            viable = True
                            for slot in range(1,c4.n-filled):
                                if i + slot*(-k) < 0 or i + slot*(-k) > c4.width-1 or j + slot*(-l) < 0 or j + slot*(-l) > c4.height-1 or board.state[i+slot*(-k)][j+slot*(-l)]['player'] is not player:
                                    break
                                else:
                                    filled+=1
                            for slot in range(1,c4.n-filled):
                                if i + slot*(k) < 0 or i + slot*(k) > c4.width-1 or j + slot*(l) < 0 or j + slot*(l) > c4.height-1 or board.state[i+slot*(-k)][j+slot*(-l)]['player'] is not 0:
                                    viable = False
                                    break
                            #score of individual position
                            '''
                            if filled is 3 and (i + k, j + l) in valid_moves):
                                return [(i + k, j + l), None]
                            
                            else:
                            '''
                            #heuristic to weight towards fewer bigger sequences
                            if viable:
                                strength += filled**1.5

    return [None, strength]
                            

def robbot(board, player = 1):
    valid = find_moves(board)
    orig = eval(board,player,valid)
    #if there's a winning move, play it
    if orig[0] is not None:
        return orig[0]

    best_move = None
    best_score = None
    for move in valid:
        #hacky workaround using same object, lookup how to copy object when home
        board.state[move[0]][move[1]]['player'] = player
        score1 = eval(board,player,valid)
        score2 = eval(board,1 + (player % 2), valid)
        #reverse the hack
        board.state[move[0]][move[1]]['player'] = 0
        if score1 - score2 > best_score:
            best_move = move

    return best_move

