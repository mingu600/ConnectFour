

def next_move(board, player):
    import connect4game
    for j in range(0, connect4game.height):
        for i in range (0, connect4game.width):
            if board.state[i][j]['player'] is 0:
                return i
