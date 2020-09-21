'''
A connect four game against an A.I.
The A.I. is a WIP.
'''
import random

def transform(x):
    if x == 'X':
        return -1.01
    else:
        return 1

def endtext(x):
    if x > 90000:
        return 'I won, yay!'
    if x < -90000:
        return 'You won, well done!'
    else:
        return 'It\'s a draw.'


# set up the board at the start of the game:
def setup():
    global board
    board = []
    for i in range(7):
        board.append(['_', '_', '_', '_', '_', '_'])


# this function draws the board at the beginning of each turn:
def draw(board):
    print(' _ _ _ _ _ _ _ ')
    for i in range(5,-1,-1):
        print('|'+board[0][i]+'|'+board[1][i]+'|'+board[2][i]+
              '|'+board[3][i]+'|'+board[4][i]+'|'+board[5][i]+
              '|'+board[6][i]+'|')
    print(' 1 2 3 4 5 6 7 ')


# put a *player* (X or O) counter in the chosen *column*
# on the chosen *board*:
def move(column, player, board):
    done = False
    for i in range(6):
        if board[column-1][i] == '_' and done == False:
            board[column-1][i] = player
            done = True


# ask the user for a column number. Only return it, if
# it's an integer between 1 and 7 inclusive, and that column
# isn't full yet:
def get_move_x():

    try:
        w = int(input('Pick a column (1-7): '))
        if 0 < w < 8 and board[w-1][5]=='_':
            return w
        else:
            return get_move_x()
    except:
        return get_move_x()

def delmove(x, board):
    if board[x-1][5] != '_':
        board[x-1][5] = '_'
    else:
        for z in range(5,-1,-1):
            if board[x-1][z] == '_' and board[x-1][z-1] != '_':
                board[x-1][z-1] = '_'
                break
            

        
# the algorithm that will decide the computer's next move. Minimax:
def get_move_o():

    # make a copy of the board:
    copy = board

    # make a dictionary of all the possible moves and
    
    # their values:
    pos_moves = {}

    for a in range(1,8):
        if copy[a-1][5] == '_':
            move(a, 'O', copy)

            if evaluate(copy) > 90000:
                pos_moves[evaluate(copy)] = a
            else:
                
                listb = []
                for b in range(1,8):
                    if copy[b-1][5] == '_':
                        move(b, 'X', copy)

                        if evaluate(copy) > 90000:
                            listb.append(evaluate(copy))
                        else:

                            listc = []
                            for c in range(1,8):
                                if board[c-1][5] == '_':
                                    move(c, 'O', copy)

                                    if evaluate(copy) > 90000:
                                        listc.append(evaluate(copy))
                                    else:
                                        listd = []
                                        for d in range(1,8):
                                            if board[d-1][5] == '_':
                                                move(d, 'X', copy)

                                                listd.append(evaluate(copy))

                                                delmove(d, copy)

                                        if listd != []:
                                            listc.append(evaluate(copy))
                
                                    delmove(c, copy)
                    
                            if listc != []:
                                listb.append(max(listc))
                        
                        delmove(b, copy)
                            
                if listb != []:
                    pos_moves[min(listb)] = a

            delmove(a, board)

    if pos_moves == {}:
        return None
    else:
        return pos_moves[max(pos_moves)]


# the function that will find the winner 
def evaluate(board):

    w = 0

    # check for winners vertically:
    for c in range(7):
        for r in range(3):
            if board[c][r]==board[c][r+1]==board[c][r+2]==board[c][r+3]!='_':
                w += transform(board[c][r])*100000


    # horizontally:
    for c in range(4):
        for r in range(6):
            if board[c][r]==board[c+1][r]==board[c+2][r]==board[c+3][r]!='_':
                w += transform(board[c][r])*100000


    # / diagonally:
    for c in range(4):
        for r in range(3):
            if board[c][r]==board[c+1][r+1]==board[c+2][r+2]==board[c+3][r+3]!='_':
                w += transform(board[c][r])*100000

    # \ diagonally:
    for c in range(3,7):
        for r in range(3):
            if board[c][r]==board[c-1][r+1]==board[c-2][r+2]==board[c-3][r+3]!='_':
                w += transform(board[c][r])*100000


    # Check for threats:

    # vertically:
    # XX_
    for c in range(7):
        for r in range(4):
            if board[c][r]==board[c][r+1]!='_' and board[c][r+2]=='_':
                w += transform(board[c][r])*100
    # XXX_
    for c in range(7):
        for r in range(3):
            if board[c][r]==board[c][r+1]==board[c][r+2]!='_' and board[c][r+3]=='_':
                w += transform(board[c][r])*1000

    
    # horixontally:
    # XX_
    for c in range(5):
        for r in range(6):
            if board[c][r]==board[c+1][r]!='_' and board[c+2][r]=='_':
                if board[c+2][r-1] != '_' or r == 0:
                    w += transform(board[c][r])*100
    # _XX
    for c in range(1,6):
        for r in range(6):
            if board[c][r]==board[c+1][r]!='_' and board[c-1][r]=='_':
                if board[c-1][r-1] != '_' or r == 0:
                    w += transform(board[c][r])*100
    # X_X     
            if board[c-1][r]==board[c+1][r]!='_' and board[c][r]=='_':
                if board[c][r-1] != '_' or r==0:
                    w += transform(board[c-1][r])*100
    # XXX_
    for c in range(4):
        for r in range(6):
            if board[c][r]==board[c+1][r]==board[c+2][r]!='_' and board[c+3][r]=='_':
                if r == 0 or board[c+3][r-1]!='_':
                    w += transform(board[c][r])*1000
    # _XXX
            if board[c+1][r]==board[c+2][r]==board[c+3][r]!='_' and board[c][r]=='_':
                if r == 0 or board[c][r-1]!='_':
                    w += transform(board[c+1][r])*1000
    # X_XX
    for c in range(3):
        for r in range(6):
            if board[c][r]==board[c+2][r]==board[c+3][r]!='_' and board[c+1][r]=='_':
                if r == 0 or board[c+1][r-1] != '_':
                    w += transform(board[c][r])*1000
    # XX_X
            if board[c][r]==board[c+1][r]==board[c+3][r]!='_' and board[c+2][r]=='_':
                if r == 0 or board[c+2][r-1] != '_':
                    w += transform(board[c][r])*1000

    
    # / diagonally:
    # XX_
    for c in range(5):
        for r in range(4):
            if board[c][r]==board[c+1][r+1]!='_' and board[c+2][r+2]=='_':
                if board[c+2][r+1]!='_':
                    w += transform(board[c][r])*100
    # _XX
    for c in range(1,5):
        for r in range(1,5):
            if board[c][r]==board[c+1][r+1]!='_' and board[c-1][r-1]=='_':
                if board[c-1][r-2]!='_' or r == 1:
                    w += transform(board[c][r])*100
    # X_X
    for c in range(4):
        for r in range(3):
            if board[c][r]==board[c+2][r+2]!='_' and board[c+1][r+1]=='_':
                w += transform(board[c][r])*100
    # XXX_
            if board[c][r]==board[c+1][r+1]==board[c+2][r+2]!='_' and board[c+3][r+3]=='_':
                if board[c+3][r+2]!='_':
                    w += transform(board[c][r])*1000

    # \ diagonally:
    # XX_
    for c in range(3,7):
        for r in range(3):
            if board[c][r]==board[c-1][r+1]!='_' and board[c-2][r+2]=='_':
                if board[c-2][r+1]=='_':
                    w += transform(board[c][r])*100
    # XXX_
            if board[c][r]==board[c-1][r+1]==board[c-2][r+2]!='_' and board[c-3][r+3]=='_':
                if board[c-3][r+2]!='_':
                    w += transform(board[c][r])*1000
    # _XX
    for c in range(2,6):
        for r in range(1,4):
            if board[c][r]==board[c-1][r+1]!='_' and board[c-2][r+2]=='_':
                if r==0 or board[c+1][r-1]=='_':
                    w += transform(board[c][r])*100
    # X_X
    for c in range(2,6):
        for r in range(3):
            if board[c][r]==board[c-2][r+2]!='_' and board[c-1][r+1]=='_':
                if board[c-1][r]!='_':
                    w += transform(board[c][r])*100

    # horizontally _X_
    for c in range(1,6):
        for r in range(6):
            if board[c][r]!='_' and board[c-1][r]==board[c+1][r]=='_':
                if r == 0 or board[c-1][r-1]==board[c+1][r-1]=='_':
                    w += transform(board[c][r])
    # / diagonally _X_
    for c in range(4):
        for r in range(4):
            if board[c+1][r+1]!='_' and board[c][r]==board[c+2][r+2]=='_':
                if r == 0 or board[c+1][r]==board[c][r-2]=='_':
                    w += transform(board[c+1][r+1])
            
    return w


def main():
    # at the beginning of each game, set up the board:
    setup()
    draw(board)



    if s%2 == 0:
        move(4, 'O', board)
        draw(board)
    
    while True:

        # get a move from the user, and implement it:
        move(get_move_x(), 'X', board)

        # draw the board in its new state:
        draw(board)

        # if evaluate(board) found a winner (i.e. if
        # abs(evaluate(board)) > 90000), then break
        if abs(evaluate(board)) > 90000:
            break

        # Now do the same thing, but for O:
        move(get_move_o(), 'O', board)
        
        draw(board)
        if abs(evaluate(board)) > 90000:
            break

    # after the while-loop broke, print the winner:
    print(endtext(evaluate(board)))

s = 1

print("This is a game of connect 4 against an AI. Play your moves by typing in the column you want to play in. Have fun :)\n")

while True:
    main()
    s += 1
    if input('\nPlay again (y or n)? ').lower()!='y':
        break
