import os

def printBoard(board):
    print(f"{board['TopLeft']}|{board['TopMid']}|{board['TopRight']}")
    print("-+-+-")
    print(f"{board['MidLeft']}|{board['MidMid']}|{board['MidRight']}")
    print("-+-+-")
    print(f"{board['BotLeft']}|{board['BotMid']}|{board['BotRight']}")
    
def gameInit(gamestart, p1, p2):
    print("You have started a game of Tic Tac Toe!")
    p1 = input("Player 1 - Choose your symbol (X or O): ")
    if p1 == 'X':
        p2 = 'O'
        print(f"Player 2, you have the symbol {p2}")
        gamestart = 1
    elif p1 == 'O':
        p2 = 'X'
        print(f"Player 2, you have the symbol {p2}")
        gamestart = 1
    else:
        print("You have entered wrong symbol! terminating game!")
        gamestart = 0
    return gamestart, p1, p2

def gameEnd(board):
    if (board["TopLeft"]=='X' and board["TopMid"]=='X' and board["TopRight"]=='X') or \
    (board["TopLeft"]=='O' and board["TopMid"]=='O' and board["TopRight"]=='O'):
        print("The game has ended")
        win = 1
        return win
    if (board["MidLeft"]=='X' and board["MidMid"]=='X' and board["MidRight"]=='X') or \
    (board["MidLeft"]=='O' and board["MidMid"]=='O' and board["MidRight"]=='O'):
        print("The game has ended")
        win = 1
        return win
    if (board["BotLeft"]=='X' and board["BotMid"]=='X' and board["BotRight"]=='X') or \
    (board["BotLeft"]=='O' and board["BotMid"]=='O' and board["BotRight"]=='O'):
        print("The game has ended")
        win = 1
        return win
    if (board["TopLeft"]=='X' and board["MidLeft"]=='X' and board["BotLeft"]=='X') or \
    (board["TopLeft"]=='O' and board["MidLeft"]=='O' and board["BotLeft"]=='O'):
        print("The game has ended")
        win = 1
        return win
    if (board["TopMid"]=='X' and board["MidMid"]=='X' and board["BotMid"]=='X') or \
    (board["TopMid"]=='O' and board["MidMid"]=='O' and board["BotMid"]=='O'):
        print("The game has ended")
        win = 1
        return win
    if (board["TopRight"]=='X' and board["MidRight"]=='X' and board["BotRight"]=='X') or \
    (board["TopRight"]=='O' and board["MidRight"]=='O' and board["BotRight"]=='O'):
        print("The game has ended")
        win = 1
        return win
    if (board["TopLeft"]=='X' and board["MidMid"]=='X' and board["BotRight"]=='X') or \
    (board["TopLeft"]=='O' and board["MidMid"]=='O' and board["BotRight"]=='O'):
        print("The game has ended")
        win = 1
        return win
    if (board["TopRight"]=='X' and board["MidMid"]=='X' and board["BotLeft"]=='X') or \
    (board["TopRight"]=='O' and board["MidMid"]=='O' and board["BotLeft"]=='O'):
        print("The game has ended")
        win = 1
        return win
    

TicTacToeBoard = {'TopLeft': ' ', 'TopMid':' ', 'TopRight':' ',
                 'MidLeft':' ', 'MidMid':' ', 'MidRight':' ',
                 'BotLeft':' ', 'BotMid':' ', 'BotRight':' '}

win = 0
gamestart = 0
turn = 1
place = ''
p1 = ''
p2 = ''

gamestart, p1, p2 = gameInit(gamestart, p1, p2)

while not win:
    if gamestart:
        if turn == 1:
            print("Player 1, Its your turn! Choose position where you want to place the symbol (TopLeft, TopMid, TopRight,\
            MidLeft, MidMid, MidRight, BotLeft, BotMid, BotRight): ")
            place = input()
            if place in TicTacToeBoard.keys():
                TicTacToeBoard[place] = p1
                turn = 0
                printBoard(TicTacToeBoard)
            else:
                print("Invalid move")
                turn = 1
            win = gameEnd(TicTacToeBoard)
        elif turn == 0:
            print("Player 2, Its your turn! Choose position where you want to place the symbol (TopLeft, TopMid, TopRight,\
            MidLeft, MidMid, MidRight, BotLeft, BotMid, BotRight): ")
            place = input()
            if place in TicTacToeBoard.keys():
                TicTacToeBoard[place] = p2
                turn = 1
                printBoard(TicTacToeBoard)
            else:
                print("Invalid move")
                turn = 0
            win = gameEnd(TicTacToeBoard)
    
