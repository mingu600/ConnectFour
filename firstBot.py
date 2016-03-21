#Mingu's first bot-minimax
import random

def matchFour(list):
    import connect4game
    bestscore = []
    for k in range(0, len(list)):
        if list[k] == 1:
            counter = 2
            top = min([connect4game.n - 2, len(list) - k - 1])
            for l in range(0, top):
                if list[k + l + 1] == 2 :
                    counter += 1
            bestscore.append(counter)
    if bestscore == []:
        bestscore = [2]
    return max(bestscore)

def findFour(board, x, y, direction, list):
    import connect4game
    if direction == 'vertical':
        bottom = max([-3, -1 * y])
        top = min([3, connect4game.height - y - 1])
        for j in range(bottom, top + 1):
            list.append(board.state[x][y + j][direction])
    elif direction == 'horizontal':
        bottom = max([-3, -1 * x])
        top = min([3, connect4game.width - x - 1])
        for j in range(bottom, top + 1):
            list.append(board.state[x + j][y][direction])
    elif direction == 'right':
        bottom = max([-3, -1 * y, -1 * x])
        top = min([3, connect4game.height - y - 1, connect4game.width - x - 1])
        for j in range(bottom, top + 1):
            list.append(board.state[x + j][y + j][direction])
    else:
        bottom = max([-3, y - connect4game.height + 1, -1 * x])
        top = min([3, y, connect4game.width - x - 1])
        for j in range(bottom, top + 1):
            list.append(board.state[x + j][y - j][direction])
    #print(list, [x,y], direction)
    #printBoard(board)
    return matchFour(list)

def checkStatus(board, last_move, x, y):
    scoreList = []
    for i in ['right', 'left', 'vertical', 'horizontal']:
        if last_move[i] is not 0:
            list = []
            scoreList.append(findFour(board, x, y, i, list))
    if len(scoreList) == 0:
        return 0
    return max(scoreList)

def findPlayer(board, player):
    import connect4game
    tokens = []
    for j in range(0, connect4game.height):
        for i in range (0, connect4game.width):
            if board.state[i][j]['player'] == player:
                tokens.append([i, j])
    return tokens

def available(board, x):
    import connect4game
    i = 0
    while i < connect4game.height and board.state[x][i]['player'] is not 0:
        i += 1
    if i >= connect4game.height:
        return -10
    else:
        return i

def printBoard(board):
    import connect4game
    print("")
    for k in range(0, connect4game.width):
        print(' ', k, ' ', end="")
    print("")
    print("")
    for j in range(0,connect4game.height):
        for i in range(0,connect4game.width):
            if board.state[i][connect4game.height-j-1]['player'] is 0:
                print('|', u'\u26AA', ' ',end="")
            elif board.state[i][connect4game.height-j-1]['player'] is 1:
                print('|', u'\U0001F534', ' ' ,end="")
            else:
                print('|', u'\u26AB', ' ',end="")
        print("|", end="")
        print("")
        grid = " ----"
        line = ''
        for k in range(0, connect4game.width):
            line += grid
        print(line)

def updateBoard(board, x, y, player):
    import connect4game
    neighbors = [-1, 0, 1]
    for i in neighbors:
        for j in neighbors:
            if (x + i >= 0 and x + i < connect4game.width) and (y + j >= 0 and y + j < connect4game.height) and (i is not 0 or j is not 0):
                updated_spot = board.state[x + i][y + j]
                if updated_spot['player'] == player:
                    if abs(i + j) == 2:
                        board.state[x][y]['right'] += 1
                        updated_spot['right'] += 1
                    elif i + j == 0:
                        board.state[x][y]['left'] += 1
                        updated_spot['left'] += 1
                    elif j == 0:
                        board.state[x][y]['horizontal'] += 1
                        updated_spot['horizontal'] += 1
                    else:
                        board.state[x][y]['vertical'] += 1
                        updated_spot['vertical'] += 1

def removeSpot(board, x, y, player):
    import connect4game
    neighbors = [-1, 0, 1]
    for i in neighbors:
        for j in neighbors:
            if (x + i >= 0 and x + i < connect4game.width) and (y + j >= 0 and y + j < connect4game.height) and (i is not 0 or j is not 0):
                updated_spot = board.state[x + i][y + j]
                if updated_spot['player'] == player:
                    if abs(i + j) == 2:
                        board.state[x][y]['right'] -= 1
                        updated_spot['right'] -= 1
                    elif i + j == 0:
                        board.state[x][y]['left'] -= 1
                        updated_spot['left'] -= 1
                    elif j == 0:
                        board.state[x][y]['horizontal'] -= 1
                        updated_spot['horizontal'] -= 1
                    else:
                        board.state[x][y]['vertical'] -= 1
                        updated_spot['vertical'] -= 1

def next_move(board, player):
    import connect4game
    import hodor
    otherplayer = 3 - player
    bestScore = [0, -10000000]
    bestScore2 = [0, -10000000]
    finalScores = []
    finalScores2 = []
    totalScores = []
    result = []
    if findPlayer(board, player) == []:
        return round((connect4game.width - 1)/2)
    else:
        for i in range(0, connect4game.width):
            bestOppmove = []
            newBoard = board
            if available(newBoard, i) >= 0:
                new_spot = [i, available(newBoard, i)]
                desired_spot = newBoard.state[new_spot[0]][new_spot[1]]
                desired_spot['player'] = player
                updateBoard(newBoard, new_spot[0], new_spot[1], player)
                myBest = checkStatus(newBoard, desired_spot, new_spot[0], new_spot[1])
            else:
                continue
            #print("myBest:", myBest)
            for j in range(0, connect4game.width):
                if available(newBoard, j) >= 0:
                    new_opp_spot = [j, available(newBoard, j)]
                    opp_desired_spot = newBoard.state[new_opp_spot[0]][new_opp_spot[1]]
                    #print(new_opp_spot)
                    opp_desired_spot['player'] = otherplayer
                    updateBoard(newBoard, new_opp_spot[0], new_opp_spot[1], otherplayer)
                    oppBest = checkStatus(newBoard, opp_desired_spot, new_opp_spot[0], new_opp_spot[1])
                    bestOppmove.append(oppBest)
                    opp_desired_spot['player'] = 0
                else:
                    continue
                for k in range(0, connect4game.width):
                    bestOppmove2 = []
                    if available(newBoard, k) >= 0:
                        new_spot2 = [k, available(newBoard, k)]
                        desired_spot2 = newBoard.state[new_spot2[0]][new_spot2[1]]
                        desired_spot2['player'] = player
                        updateBoard(newBoard, new_spot2[0], new_spot2[1], player)
                        myBest2 = checkStatus(newBoard, desired_spot2, new_spot2[0], new_spot2[1])
                    else:
                        continue
                    for l in range(0, connect4game.width):
                        if available(newBoard, l) >= 0:
                            new_opp_spot2 = [l, available(newBoard, l)]
                            opp_desired_spot2 = newBoard.state[new_opp_spot2[0]][new_opp_spot2[1]]
                            #print(new_opp_spot)
                            opp_desired_spot2['player'] = otherplayer
                            updateBoard(newBoard, new_opp_spot2[0], new_opp_spot2[1], otherplayer)
                            oppBest2 = checkStatus(newBoard, opp_desired_spot2, new_opp_spot2[0], new_opp_spot2[1])
                            bestOppmove2.append(oppBest2)
                            opp_desired_spot2['player'] = 0
                        else:
                            continue
                        removeSpot(newBoard, new_opp_spot2[0], new_opp_spot2[1], otherplayer)
                    if bestOppmove2 == []:
                        desired_spot2['player'] = 0
                        opp_desired_spot['player'] = 0
                        desired_spot['player'] = 0
                        return i
                    finalScore = 5 ** myBest2 - 8 ** max(bestOppmove2) - 5 * abs(i - (connect4game.width - 1) / 2)
                    finalScores.append([i, j, k, l, finalScore])
                    desired_spot2['player'] = 0
                    opp_desired_spot['player'] = 0
                    opp_desired_spot2['player'] = 0
                    removeSpot(newBoard, new_spot2[0], new_spot2[1], player)
                removeSpot(newBoard, new_opp_spot[0], new_opp_spot[1], otherplayer)
            desired_spot['player'] = 0
            if bestOppmove == []:
                desired_spot2['player'] = 0
                opp_desired_spot['player'] = 0
                desired_spot['player'] = 0
                return i
            finalScore2 = 5 ** myBest - 8 ** max(bestOppmove) - 5 * abs(i - (connect4game.width - 1) / 2)
            finalScores2.append([i, j, finalScore2])
            for s in finalScores2:
                for t in finalScores:
                    if s[0] == t[0] and s[1] == t[1]:
                        totalScores.append([t[0], t[2], s[2] + t[4]])
            totalScores.sort(key=lambda x: x[2], reverse = True)
            result.append(totalScores[0])
            removeSpot(newBoard, new_spot[0], new_spot[1], player)
        result.sort(key=lambda x: x[2], reverse = True)
        if result == []:
            # for v in range(0, connect4game.width):
            #     print(board.state[v][5])
            for q in range(0, connect4game.width):
                if available(board, q) >= 0:
                    #print(board.state[q][available(board, q)]['player'], q)
                    return q
            #return random.randrange(0, connect4game.width)
        print(result[0])
        return result[0][0]
