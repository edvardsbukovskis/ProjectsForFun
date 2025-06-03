import os
import random


def printBoard(board):
    print(f"{board['TopLeft']}|{board['TopMid']}|{board['TopRight']}")
    print("-+-+-")
    print(f"{board['MidLeft']}|{board['MidMid']}|{board['MidRight']}")
    print("-+-+-")
    print(f"{board['BotLeft']}|{board['BotMid']}|{board['BotRight']}")


def gameInit():
    print("You have started a game of Tic Tac Toe!")
    p1 = input("Player 1 - Choose your symbol (X or O): ")
    if p1 == 'X':
        p2 = 'O'
    elif p1 == 'O':
        p2 = 'X'
    else:
        print("You have entered wrong symbol! terminating game!")
        return None, None, None
    cpu_choice = input("Do you want to play against the CPU? (y/n): ").lower()
    cpu_mode = cpu_choice == 'y'
    if cpu_mode:
        print("Player 2 will be controlled by the CPU")
    else:
        print(f"Player 2, you have the symbol {p2}")
    return p1, p2, cpu_mode


def checkWin(board, symbol):
    combos = [
        ('TopLeft', 'TopMid', 'TopRight'),
        ('MidLeft', 'MidMid', 'MidRight'),
        ('BotLeft', 'BotMid', 'BotRight'),
        ('TopLeft', 'MidLeft', 'BotLeft'),
        ('TopMid', 'MidMid', 'BotMid'),
        ('TopRight', 'MidRight', 'BotRight'),
        ('TopLeft', 'MidMid', 'BotRight'),
        ('TopRight', 'MidMid', 'BotLeft'),
    ]
    for combo in combos:
        if all(board[pos] == symbol for pos in combo):
            return True
    return False


def boardFull(board):
    return all(value != ' ' for value in board.values())


def resetBoard(board):
    for key in board.keys():
        board[key] = ' '


TicTacToeBoard = {
    'TopLeft': ' ', 'TopMid': ' ', 'TopRight': ' ',
    'MidLeft': ' ', 'MidMid': ' ', 'MidRight': ' ',
    'BotLeft': ' ', 'BotMid': ' ', 'BotRight': ' '
}

p1_score = 0
p2_score = 0
draw_count = 0

p1, p2, cpu_mode = gameInit()
if p1 is None:
    exit()

turn = 1
while True:
    printBoard(TicTacToeBoard)
    if turn == 1:
        place = input("Player 1, choose your position (TopLeft, TopMid, TopRight, MidLeft, MidMid, MidRight, BotLeft, BotMid, BotRight): ")
        if place in TicTacToeBoard and TicTacToeBoard[place] == ' ':
            TicTacToeBoard[place] = p1
            if checkWin(TicTacToeBoard, p1):
                printBoard(TicTacToeBoard)
                print("Player 1 wins!")
                p1_score += 1
                result = 'win'
            elif boardFull(TicTacToeBoard):
                printBoard(TicTacToeBoard)
                print("It's a draw!")
                draw_count += 1
                result = 'draw'
            else:
                turn = 0
                continue
        else:
            print("Invalid move")
            continue
    else:
        if cpu_mode:
            available = [k for k, v in TicTacToeBoard.items() if v == ' ']
            place = random.choice(available)
            print(f"CPU chooses {place}")
        else:
            place = input("Player 2, choose your position (TopLeft, TopMid, TopRight, MidLeft, MidMid, MidRight, BotLeft, BotMid, BotRight): ")
            if place not in TicTacToeBoard or TicTacToeBoard[place] != ' ':
                print("Invalid move")
                continue
        TicTacToeBoard[place] = p2
        if checkWin(TicTacToeBoard, p2):
            printBoard(TicTacToeBoard)
            if cpu_mode:
                print("CPU wins!")
            else:
                print("Player 2 wins!")
            p2_score += 1
            result = 'win'
        elif boardFull(TicTacToeBoard):
            printBoard(TicTacToeBoard)
            print("It's a draw!")
            draw_count += 1
            result = 'draw'
        else:
            turn = 1
            continue

    print(f"Score -> Player 1: {p1_score} | Player 2: {p2_score} | Draws: {draw_count}")
    play_again = input("Play again? (y/n): ").lower()
    if play_again == 'y':
        resetBoard(TicTacToeBoard)
        turn = 1
        continue
    else:
        print("Thanks for playing!")
        break
