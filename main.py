from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from auth import Ui_MainWindow
import numpy as np
import sys
from tkinter import *
from tkinter.messagebox import *
import random


def click_auth():
    with open('credentials.txt', 'r') as f:
        flag = 0
        credentials = log() + pas()
        for row in f:
            if row == Encrypt(credentials) + "\n":
                flag = 1
                break
    clear()
    if flag == 1:
        MainWindow.close()
        window.deiconify()
        rungame()
    else:
        message("Неверный логин или пароль, попробуте еще раз")

def click_reg():
    with open('login.txt', 'r') as f:
        for row in f:
            flag = 0
            if (Encrypt(log()) + "\n") == row:
                message("Такой логин уже существует")
                flag = 1
                break
        if flag == 0:
            checkLog = len(log())
            checkPas = len(pas())
            if checkLog < 16 and checkLog > 4 and checkPas < 16 and checkPas > 4:
                space = " "
                if space in log() or space in pas():
                    message("Недопустимый символ в логине или пароле: Пробел")
                else:
                    with open('login.txt', 'a') as f:
                        f.write(Encrypt(log()) + "\n")
                    with open('credentials.txt', 'a') as d:
                        credentials = log() + pas()
                        d.write(Encrypt(credentials) + '\n')
                    clear()
            else:
                message("Некорректные логин или пароль, попробуйте еще раз")

def log():
    log = ui.plainTextEditLog.toPlainText()
    return log

def pas():
    pas = ui.plainTextEditPass.toPlainText()
    return pas

def clear():
    ui.plainTextEditLog.setPlainText("")
    ui.plainTextEditPass.setPlainText("")

def Encrypt(word):
    a = np.array(
        [[" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "]])
    b = np.array(
        [[" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "]])

    l = len(word)
    lenFlag = 0
    for i in range(5):
        for j in range(6):
            if lenFlag < l:
                a[i, j] = word[lenFlag]
                lenFlag += 1

    b[0], b[1], b[2], b[3], b[4] = a[2], a[3], a[0], a[4], a[1]

    a[:, 0], a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5] = b[:, 1], b[:, 3], b[:, 5], b[:, 0], b[:, 2], b[:, 4]

    word = ""
    for i in range(5):
        for j in range(6):
            word += a[i,j]
    return word

def Decipher(word):
    a = np.array(
        [[" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "]])
    b = np.array(
        [[" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "], [" ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " "]])

    l = len(word)
    lenFlag = 0
    for i in range(5):
        for j in range(6):
            if lenFlag < l:
                a[i, j] = word[lenFlag]
                lenFlag = lenFlag + 1

    b[2], b[3], b[0], b[4], b[1] = a[0], a[1], a[2], a[3], a[4]

    a[:, 1], a[:, 3], a[:, 5], a[:, 0], a[:, 2], a[:, 4] = b[:, 0], b[:, 1], b[:, 2], b[:, 3], b[:, 4], b[:, 5]

    word = ""
    for i in range(5):
        for j in range(6):
            word += a[i, j]
    return word

def message(text):
    msg = QMessageBox()
    msg.setWindowTitle("Оповещение")
    msg.setText(text)
    msg.exec()

def computer_move(turn, board):

    c_move_finder(board)

    if MoveList[0][0] == "m":
        MoveList.remove("m")
        move = random.choice(MoveList)
        board[int(move[0])][int(move[1])] = 0
        board[int(move[2])][int(move[3])] = ComputerCheckers
        if int(move[3]) > int(move[1]):
            board[int(move[2]) - 1][int(move[3]) - 1] = 0
        else:
            board[int(move[2]) - 1][int(move[3]) + 1] = 0
        MoveList.clear()
        c_move_finder(board)
        if MoveList[0][0] == "m":
            computer_move(turn, board)
        else:
            turn_switch(turn)

    else:
        move = random.choice(MoveList)
        if board[int(move[0])][int(move[1])] == ComputerCheckers + 2:
            board[int(move[0])][int(move[1])] = 0
            board[int(move[2])][int(move[3])] = ComputerCheckers + 2
        else:
            board[int(move[0])][int(move[1])] = 0
            board[int(move[2])][int(move[3])] = ComputerCheckers
        turn_switch(turn)

    damka(board)
    MoveList.clear()
    draw_game(board)
    end_game(board)

def c_move_finder(board):
    global MoveList
    MoveList = []

    if turn == ComputerCheckers:
        m_move(colorH, turn)
        if m_move_flag == 1:
            MoveList.append("m")

            if x_m != -1:
                MoveList.append(str(x_m - 2) + str(y_m + 2) + str(x_m) + str(y_m) )
            if x_m2 != -1:
                MoveList.append(str(x_m2 - 2) + str(y_m2 - 2) + str(x_m2) + str(y_m2) )

        else:
            for i in range(8):
                for j in range(8):
                    if board[i][j] == ComputerCheckers:
                        if i < 7 and j > 0:
                            if board[i + 1][j - 1] == 0:
                                MoveList.append(str(i) + str(j) + str(i + 1) + str(j - 1))
                        if i < 7 and j < 7:
                            if board[i + 1][j + 1] == 0:
                                MoveList.append(str(i) + str(j) + str(i + 1) + str(j + 1))

                    if board[i][j] == ComputerCheckers + 2:
                        if i > 0 and j > 0:
                            if board[i - 1][j - 1] == 0:
                                MoveList.append(str(i) + str(j) + str(i - 1) + str(j - 1))

                        if i > 0 and j < 7:
                            if board[i - 1][j + 1] == 0:
                                MoveList.append(str(i) + str(j) + str(i - 1) + str(j + 1))

def new_game():
    if askyesno("Выбор хода", "Вы будете играть за белых?"):
        white = True
    else:
        white = False
    if white == True:
        board = [[0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [2, 0, 2, 0, 2, 0, 2, 0],
                 [0, 2, 0, 2, 0, 2, 0, 2],
                 [2, 0, 2, 0, 2, 0, 2, 0]]

    else:
        board = [[0, 2, 0, 2, 0, 2, 0, 2],
                 [2, 0, 2, 0, 2, 0, 2, 0],
                 [0, 2, 0, 2, 0, 2, 0, 2],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1, 0]]

    draw_game(board)

    return board, white

def draw_game(board):
    global select_board_canvas
    canvas.delete("all")

    for i in range(8):
        if i % 2 == 0:
            color = "white"
        else:
            color = "grey"
        for j in range(8):
            x1 = j * 100
            y1 = i * 100
            x2 = x1 + 100
            y2 = y1 + 100
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            if color == "grey":
                color = "white"
            else:
                color = "grey"

            if board[i][j] == 1:
                canvas.create_oval(j*100+10, i*100+10, j*100+90, i*100+90, fill="black", outline="white")
            if board[i][j] == 2:
                canvas.create_oval(j*100+10, i*100+10, j*100+90, i*100+90, fill="white", outline="black")
            if board[i][j] == 3:
                canvas.create_oval(j * 100 + 10, i * 100 + 10, j * 100 + 90, i * 100 + 90, fill="black",
                                   outline="red", width="3")
            if board[i][j] == 4:
                canvas.create_oval(j * 100 + 10, i * 100 + 10, j * 100 + 90, i * 100 + 90, fill="white",
                                   outline="red", width="3")
    canvas.pack()

def end_game(curr_board):
    global board, colorH, turn, m_move_flag, mFlag, x_m, x_m2, y_m, y_m2, possible_moves

    draw_game(board)
    w = 0
    b = 0
    newGame = None
    for i in range(8):
        for j in range(8):
            if curr_board[i][j] == 2 or curr_board[i][j] == 4:
                w += 1
            if curr_board[i][j] == 1 or curr_board[i][j] == 3:
                b += 1
    if w == 0 or b == 0:
        if askyesno("Конец партии", "Хотите начать новую игру?"):
            newGame = True
        else:
            newGame = False
    if newGame == True:
        if w == 0:
            board, colorH = new_game()
            if colorH == False:
                ComputerCheckers = 2
                computer_move(turn, board)
            else:
                ComputerCheckers = 1
            turn = 2
            m_move_flag = 0
            mFlag = -1
            x_m = -1
            y_m = -1
            x_m2 = -1
            y_m2 = -1
            possible_moves = [-1, -1, -1, -1, -1, -1, -1, -1]
        if b == 0:
            board, colorH = new_game()
            turn = 2
            m_move_flag = 0
            mFlag = -1
            x_m = -1
            y_m = -1
            x_m2 = -1
            y_m2 = -1
            possible_moves = [-1, -1, -1, -1, -1, -1, -1, -1]
    else:
        pass

def damka(board):
    if colorH == True:
        for i in range(8):
            if board[0][i] == 2:
                board[0][i] = 4
            if board[7][i] == 1:
                board[7][i] = 3
    if colorH == False:
        for i in range(8):
            if board[0][i] == 1:
                board[0][i] = 3
            if board[7][i] == 2:
                board[7][i] = 4

def turn_switch(a):
    global turn
    if a == 1:
        turn = 2
    else:
        turn = 1

def m_move(color,turn):
    global x_m, y_m, x_m2, y_m2, y_d, x_d, i, j, m_move_flag
    y_d, x_d = -1, -1
    x_m, x_m2, y_m2, y_m = -1, -1, -1, -1

    if color == True:
        if turn == 2:
            for i in range(8):
                for j in range(8):
                    if board[i][j] == 2:
                        if j > 1 and j < 6 and i > 1:
                            if (board[i-1][j-1] == 1 or board[i-1][j-1] == 3)  and board[i-2][j-2]== 0:
                                x_m, y_m =  i-2,j-2
                            if (board[i-1][j+1] == 1 or board[i-1][j+1] == 3) and board[i-2][j+2]== 0:
                                x_m2, y_m2 =  i-2,j+2
                        if j<2 and i > 1:
                            if (board[i-1][j+1] == 1 or board[i-1][j+1] == 3) and board[i-2][j+2]== 0:
                                x_m2, y_m2 =  i-2,j+2
                        if j>5 and i > 1:
                            if (board[i-1][j-1] == 1 or board[i-1][j-1] == 3) and board[i-2][j-2]== 0:
                                x_m, y_m =  i-2,j-2
        if turn == 1:
            for i in range(8):
                for j in range(8):
                    if board[i][j] == 1:
                        if j > 1 and j < 6 and i < 6:
                            if (board[i+1][j-1] == 2 or board[i+1][j-1] == 4) and board[i+2][j-2]== 0:
                                x_m, y_m =  i+2,j-2
                            if (board[i+1][j+1] == 2 or board[i+1][j+1] == 4) and board[i+2][j+2]== 0:
                                x_m2, y_m2 =  i+2,j+2
                        if j<2 and i < 6:
                            if (board[i+1][j+1] == 2 or board[i+1][j+1] == 4) and board[i+2][j+2]== 0:
                                x_m2, y_m2 =  i+2,j+2
                        if j>5 and i < 6:
                            if (board[i+1][j-1] == 2 or board[i+1][j-1] == 4) and board[i+2][j-2]== 0:
                                x_m, y_m =  i+2,j-2

    if color == False:
        if turn == 1:
            for i in range(8):
                for j in range(8):
                    if board[i][j] == 1:
                        if j > 1 and j < 6 and i > 1:
                            if (board[i-1][j-1] == 2 or board[i-1][j-1] == 4) and board[i-2][j-2]== 0:
                                x_m, y_m =  i-2,j-2
                            if (board[i-1][j+1] == 2 or board[i-1][j+1] == 4) and board[i-2][j+2]== 0:
                                x_m2, y_m2 =  i-2,j+2
                        if j<2 and i > 1:
                            if (board[i-1][j+1] == 2 or board[i-1][j+1] == 4) and board[i-2][j+2]== 0:
                                x_m2, y_m2 =  i-2,j+2
                        if j>5 and i > 1:
                            if (board[i-1][j-1] == 2 or board[i-1][j-1] == 4) and board[i-2][j-2]== 0:
                                x_m, y_m =  i-2,j-2
        if turn == 2:
            for i in range(8):
                for j in range(8):
                    if board[i][j] == 2:
                        if j > 1 and j < 6 and i < 6:
                            if (board[i+1][j-1] == 1 or board[i+1][j-1] == 3) and board[i+2][j-2]== 0:
                                x_m, y_m =  i+2,j-2
                            if (board[i+1][j+1] == 1 or board[i+1][j+1] == 3) and board[i+2][j+2]== 0:
                                x_m2, y_m2 =  i+2,j+2
                        if j<2 and i < 6:
                            if (board[i+1][j+1] == 1 or board[i+1][j+1] == 3) and board[i+2][j+2]== 0:
                                x_m2, y_m2 =  i+2,j+2
                        if j>5 and i < 6:
                            if (board[i+1][j-1] == 1 or board[i+1][j-1] == 3) and board[i+2][j-2]== 0:
                                x_m, y_m =  i+2,j-2

    for i in range(8):
        for j in range(8):
            if board[i][j] == 4 or board[i][j] == 3:
                y_d = j + 1
                x_d = i + 1
                stop_check = 0
                if y_d < 7 and x_d < 7:
                    while y_d != 7 and x_d != 7:
                        if turn == 2 and board[i][j] == 4:

                            if board[x_d][y_d] == 4 or board[x_d][y_d] == 2:
                                stop_check = 1

                            if board[x_d][y_d] == 1 or board[x_d][y_d] == 3:
                                if board[x_d + 1][y_d + 1] == 0 and (board[x_d - 1][y_d - 1] == 4 or board[x_d - 1][y_d - 1] == 0):
                                    x_m, y_m = i, j
                                    x_m2, y_m2 = x_d + 1, y_d + 1

                        if turn == 1 and board[i][j] == 3:

                            if board[x_d][y_d] == 1 or board[x_d][y_d] == 3:
                                stop_check = 1

                            if board[x_d][y_d] == 2 or board[x_d][y_d] == 4 :
                                if board[x_d + 1][y_d + 1] == 0 and (board[x_d - 1][y_d - 1] == 3 or board[x_d - 1][y_d - 1] == 0):
                                    x_m, y_m = i, j
                                    x_m2, y_m2 = x_d + 1, y_d + 1
                        x_d += 1
                        y_d += 1

                        if stop_check == 1:
                            break

                y_d = j - 1
                x_d = i + 1
                stop_check = 0
                if y_d > 0 and x_d < 7:
                    while y_d != 0 and x_d != 7:
                        if turn == 2 and board[i][j] == 4:

                            if board[x_d][y_d] == 4 or board[x_d][y_d] == 2:
                                stop_check = 1

                            if board[x_d][y_d] == 1 or board[x_d][y_d] == 3:
                                if board[x_d + 1][y_d - 1] == 0 and (board[x_d + 1][y_d - 1] == 0 or board[x_d + 1][y_d - 1] == 4):
                                    x_m, y_m = i, j
                                    x_m2, y_m2 = x_d + 1, y_d - 1
                        if turn == 1 and board[i][j] == 3:

                            if board[x_d][y_d] == 3 or board[x_d][y_d] == 1:
                                stop_check = 1

                                if board[x_d][y_d] == 2 or board[x_d][y_d] == 4:
                                    if board[x_d + 1][y_d - 1] == 0 and (board[x_d + 1][y_d - 1] == 0 or board[x_d + 1][y_d - 1] == 3):
                                        x_m, y_m = i, j
                                        x_m2, y_m2 = x_d + 1, y_d - 1
                        x_d += 1
                        y_d -= 1

                        if stop_check == 1:
                            break

                y_d = j + 1
                x_d = i - 1
                stop_check = 0
                if y_d < 7 and x_d > 0:
                    while y_d != 7 and x_d != 0:

                        if turn == 2 and board[i][j] == 4:

                            if board[x_d][y_d] == 4 or board[x_d][y_d] == 2:
                                stop_check = 1

                            if board[x_d][y_d] == 1 or board[x_d][y_d] == 3:
                                if board[x_d - 1][y_d + 1] == 0 and (board[x_d + 1][y_d - 1] == 0 or board[x_d + 1][y_d - 1] == 4):
                                    x_m, y_m = i, j
                                    x_m2, y_m2 = x_d - 1, y_d + 1
                        if turn == 1 and board[i][j] == 3:

                            if board[x_d][y_d] == 1 or board[x_d][y_d] == 3:
                                stop_check = 1

                            if board[x_d][y_d] == 2 or board[x_d][y_d] == 4:
                                if board[x_d - 1][y_d + 1] == 0 and (board[x_d + 1][y_d - 1] == 0 or board[x_d + 1][y_d - 1] == 3) :
                                    x_m, y_m = i, j
                                    x_m2, y_m2 = x_d - 1, y_d + 1
                        x_d -= 1
                        y_d += 1
                        if stop_check == 1:
                            break

                y_d = j - 1
                x_d = i - 1
                if y_d > 0 and x_d > 0:
                    while y_d != 0 and x_d != 0:

                        if turn == 2 and board[i][j] == 4:

                            if board[x_d][y_d] == 4 or board[x_d][y_d] == 2:
                                stop_check = 1

                            if board[x_d][y_d] == 1 or board[x_d][y_d] == 3:
                                if board[x_d - 1][y_d - 1] == 0 and (board[x_d + 1][y_d + 1] == 0 or board[x_d + 1][y_d + 1] == 4):
                                    x_m, y_m = i, j
                                    x_m2, y_m2 = x_d - 1, y_d - 1
                        if turn == 1 and board[i][j] == 3:

                            if board[x_d][y_d] == 1 or board[x_d][y_d] == 3:
                                stop_check = 1

                            if board[x_d][y_d] == 2 or board[x_d][y_d] == 4:
                                if board[x_d - 1][y_d - 1] == 0 and (board[x_d + 1][y_d + 1] == 0 or board[x_d + 1][y_d + 1] == 3):
                                    x_m, y_m = i, j
                                    x_m2, y_m2 = x_d - 1, y_d - 1
                        x_d -= 1
                        y_d -= 1
                        if stop_check == 1:
                            break
    if x_m != -1 or x_m2 != -1:
        m_move_flag = 1
    if x_m == -1 and x_m2 == -1:
        m_move_flag = 0

def checking_moves(x1,y1,turn, colorH):
    if colorH == True:
        if turn == 2 and board[y1][x1] == 2:
            if x1 > 0 and x1 < 7 and y1 > 0:
                if board[y1 - 1][x1 - 1] == 0:
                    possible_moves[0] = x1 - 1
                    possible_moves[1] = y1 - 1
                if board[y1 - 1][x1 + 1] == 0:
                    possible_moves[2] = x1 + 1
                    possible_moves[3] = y1 - 1
            if x1 > 1 and x1 < 6 and y1 > 2:
                if board[y1 - 1][x1 - 1] == 2 and board[y1 - 2][x1 - 2] == 0:
                    possible_moves[0],possible_moves[1] = x1 - 2, y1 - 2
                if board[y1 - 1][x1 + 1] == 2 and board[y1 - 2][x1 + 2] == 0:
                    possible_moves[2],possible_moves[3] = x1 + 2, y1 - 2

            if x1 == 0 and y1 > 1:
                if board[y1 - 1][x1 + 1] == 0:
                    possible_moves[2] = x1 + 1
                    possible_moves[3] = y1 - 1
            if x1 < 2 and y1 > 2:
                if board[y1 - 1][x1 + 1] == 2 and board[y1 - 2][x1 + 2] == 0:
                    possible_moves[2],possible_moves[3] = x1 + 2, y1 - 2

            if x1 == 7 and y1 > 1:
                if board[y1 - 1][x1 - 1] == 0:
                    possible_moves[0] = x1 - 1
                    possible_moves[1] = y1 - 1
            if x1 > 5 and y1 > 2:
                if board[y1 - 1][x1 - 1] == 2 and board[y1 - 2][x1 - 2] == 0:
                     possible_moves[0],possible_moves[1]= x1 - 2, y1 - 2
        if turn == 1 and board[y1][x1] == 1:
            if x1 > 0 and x1 < 7 and y1 < 7:
                if board[y1 + 1][x1 - 1] == 0:
                    possible_moves[0] = x1 - 1
                    possible_moves[1] = y1 + 1
                if board[y1 + 1][x1 + 1] == 0:
                    possible_moves[2] = x1 + 1
                    possible_moves[3] = y1 + 1
            if x1 > 1 and x1 < 6 and y1 < 6:
                if board[y1 + 1][x1 - 1] == 1 and board[y1 + 2][x1 - 2] == 0:
                    possible_moves[0],possible_moves[1]= x1 - 2, y1 + 2
                if board[y1 + 1][x1 + 1] == 1 and board[y1 + 2][x1 + 2] == 0:
                    possible_moves[2],possible_moves[3] = x1 + 2, y1 + 2

            if x1 == 0 and y1 < 7:
                if board[y1 + 1][x1 + 1] == 0:
                    possible_moves[2] = x1 + 1
                    possible_moves[3] = y1 + 1
            if x1 < 2 and y1 < 6:
                if board[y1 + 1][x1 + 1] == 1 and board[y1 + 2][x1 + 2] == 0:
                    possible_moves[2],possible_moves[3] = x1 + 2, y1 + 2

            if x1 == 7 and y1 < 6:
                if board[y1 + 1][x1 - 1] == 0:
                    possible_moves[0] = x1 - 1
                    possible_moves[1] = y1 + 1
            if x1 > 5 and y1 < 6:
                if board[y1 + 1][x1 - 1] == 1 and board[y1 + 2][x1 - 2] == 0:
                     possible_moves[0],possible_moves[1]= x1 - 2, y1 + 2

    if colorH == False:
        if turn == 1 and board[y1][x1] == 1:
            if x1 > 0 and x1 < 7 and y1 > 2:
                if board[y1 - 1][x1 - 1] == 0:
                    possible_moves[0] = x1 - 1
                    possible_moves[1] = y1 - 1
                if board[y1 - 1][x1 + 1] == 0:
                    possible_moves[2] = x1 + 1
                    possible_moves[3] = y1 - 1
            if x1 > 1 and x1 < 6 and y1 > 2:
                if board[y1 - 1][x1 - 1] == 1 and board[y1 - 2][x1 - 2] == 0:
                    possible_moves[0], possible_moves[1] = x1 - 2, y1 - 2
                if board[y1 - 1][x1 + 1] == 1 and board[y1 - 2][x1 + 2] == 0:
                    possible_moves[2], possible_moves[3] = x1 + 2, y1 - 2

            if x1 == 0 and y1 > 1:
                if board[y1 - 1][x1 + 1] == 0:
                    possible_moves[2] = x1 + 1
                    possible_moves[3] = y1 - 1
            if x1 < 2 and y1 > 2:
                if board[y1 - 1][x1 + 1] == 1 and board[y1 - 2][x1 + 2] == 0:
                    possible_moves[2], possible_moves[3] = x1 + 2, y1 - 2

            if x1 == 7 and y1 > 1:
                if board[y1 - 1][x1 - 1] == 0:
                    possible_moves[0] = x1 - 1
                    possible_moves[1] = y1 - 1
            if x1 > 5 and y1 > 2:
                if board[y1 - 1][x1 - 1] == 1 and board[y1 - 2][x1 - 2] == 0:
                    possible_moves[0], possible_moves[1] = x1 - 2, y1 - 2
        if turn == 2 and board[y1][x1] == 2:
            if x1 > 0 and x1 < 7 and y1 < 7:
                if board[y1 + 1][x1 - 1] == 0:
                    possible_moves[0] = x1 - 1
                    possible_moves[1] = y1 + 1
                if board[y1 + 1][x1 + 1] == 0:
                    possible_moves[2] = x1 + 1
                    possible_moves[3] = y1 + 1
            if x1 > 1 and x1 < 6 and y1 < 6:
                if board[y1 + 1][x1 - 1] == 2 and board[y1 + 2][x1 - 2] == 0:
                    possible_moves[0],possible_moves[1]= x1 - 2, y1 + 2
                if board[y1 + 1][x1 + 1] == 2 and board[y1 + 2][x1 + 2] == 0:
                    possible_moves[2],possible_moves[3] = x1 + 2, y1 + 2

            if x1 == 0 and y1 < 7:
                if board[y1 + 1][x1 + 1] == 0:
                    possible_moves[2] = x1 + 1
                    possible_moves[3] = y1 + 1
            if x1 < 2 and y1 < 6:
                if board[y1 + 1][x1 + 1] == 2 and board[y1 + 2][x1 + 2] == 0:
                    possible_moves[2],possible_moves[3] = x1 + 2, y1 + 2

            if x1 == 7 and y1 < 6:
                if board[y1 + 1][x1 - 1] == 0:
                    possible_moves[0] = x1 - 1
                    possible_moves[1] = y1 + 1
            if x1 > 5 and y1 < 6:
                if board[y1 + 1][x1 - 1] == 2 and board[y1 + 2][x1 - 2] == 0:
                     possible_moves[0],possible_moves[1]= x1 - 2, y1 + 2

    if board[y1][x1] == 3 or board[y1][x1] == 4:
        stopFlag = 0
        y_t = y1
        x_t = x1
        while y_t != 0 and x_t != 7:
            x_t += 1
            y_t -= 1
            if board[y_t][x_t] == 0:
                possible_moves[0], possible_moves[1] = x_t, y_t
            if turn == 1:

                if board[y_t][x_t] == 2 or board[y_t][x_t] == 4 :
                    stopFlag = 1

                if board[y_t][x_t] == 1 or board[y_t][x_t] == 3:
                    stopFlag = 1
                    if y_t > 0 and x_t < 7:
                        if board[y_t-1][x_t+1] == 0:
                            y_t -= 1
                            x_t += 1
                            possible_moves[0], possible_moves[1] = x_t, y_t
            else:
                if board[y_t][x_t] == 1 or board[y_t][x_t] == 3:
                    stopFlag = 1

                if board[y_t][x_t] == 2 or board[y_t][x_t] == 4:
                    stopFlag = 1
                    if y_t > 0 and x_t < 7:
                        if board[y_t-1][x_t+1] == 0:
                            y_t -= 1
                            x_t += 1
                            possible_moves[0], possible_moves[1] = x_t, y_t
            if stopFlag == 1:
                break

        stopFlag = 0
        y_t = y1
        x_t = x1
        while y_t != 7 and x_t != 7:
            x_t += 1
            y_t += 1
            if board[y_t][x_t] == 0:
                possible_moves[2], possible_moves[3] = x_t, y_t
            if turn == 1:

                if board[y_t][x_t] == 2 or board[y_t][x_t] == 4:
                    stopFlag = 1

                if board[y_t][x_t] == 1 or board[y_t][x_t] == 3:
                    stopFlag = 1
                    if y_t < 7 and x_t < 7:
                        if board[y_t + 1][x_t + 1] == 0:
                            y_t += 1
                            x_t += 1
                            possible_moves[2], possible_moves[3] = x_t, y_t
            else:
                if board[y_t][x_t] == 1 or board[y_t][x_t] == 3:
                    stopFlag = 1

                if board[y_t][x_t] == 2 or board[y_t][x_t] == 4:
                    stopFlag = 1
                    if y_t < 7 and x_t < 7:
                        if board[y_t + 1][x_t + 1] == 0:
                            y_t += 1
                            x_t += 1
                            possible_moves[2], possible_moves[3] = x_t, y_t
            if stopFlag == 1:
                break

        stopFlag = 0
        y_t = y1
        x_t = x1
        while y_t != 0 and x_t != 0:
            x_t -= 1
            y_t -= 1
            if board[y_t][x_t] == 0:
                possible_moves[4], possible_moves[5] = x_t, y_t
            if turn == 1:
                if board[y_t][x_t] == 2 or board[y_t][x_t] == 4:
                    stopFlag = 1

                if board[y_t][x_t] == 1 or board[y_t][x_t] == 3:
                    stopFlag = 1
                    if y_t > 0 and x_t > 0:
                        if board[y_t - 1][x_t - 1] == 0:
                            y_t -= 1
                            x_t -= 1
                            possible_moves[4], possible_moves[5] = x_t, y_t
            else:
                if board[y_t][x_t] == 1 or board[y_t][x_t] == 3:
                    stopFlag = 1

                if board[y_t][x_t] == 2 or board[y_t][x_t] == 4:
                    stopFlag = 1
                    if y_t > 0 and x_t > 0:
                        if board[y_t - 1][x_t - 1] == 0:
                            y_t -= 1
                            x_t -= 1
                            possible_moves[4], possible_moves[5] = x_t, y_t

            if stopFlag == 1:
                break

        stopFlag = 0
        y_t = y1
        x_t = x1
        while y_t != 7 and x_t != 0:
            x_t -= 1
            y_t += 1
            if board[y_t][x_t] == 0:
                possible_moves[6], possible_moves[7] = x_t, y_t
            if turn == 1:
                if board[y_t][x_t] == 2 or board[y_t][x_t] == 4:
                    stopFlag = 1

                if board[y_t][x_t] == 1 or board[y_t][x_t] == 3:
                    stopFlag = 1
                    if y_t < 7 and x_t > 0:
                        if board[y_t + 1][x_t - 1] == 0:
                            y_t += 1
                            x_t -= 1
                            possible_moves[6], possible_moves[7] = x_t, y_t
            else:
                if board[y_t][x_t] == 1 or board[y_t][x_t] == 3:
                    stopFlag = 1

                if board[y_t][x_t] == 2 or board[y_t][x_t] == 4:
                    stopFlag = 1
                    if y_t < 7 and x_t > 0:
                        if board[y_t + 1][x_t - 1] == 0:
                            y_t += 1
                            x_t -= 1
                            possible_moves[6], possible_moves[7] = x_t, y_t
            if stopFlag == 1:
                break

def click(event):
    global x2, y2, x1, y1, mFlag, m_move_flag, x_m, y_m, x_m2, y_m2

    x = event.x // 100
    y = event.y // 100

    if mFlag == -1:
        x1, y1 = x, y

    m_move(colorH, turn)

    if m_move_flag == 1:

        if (colorH == True and turn == 2) or (colorH == False and turn == 1):
            if x_m != -1 and board[x_m][y_m] != 4 and board[x_m][y_m] != 3:
                canvas.create_rectangle(y_m * 100, x_m * 100, y_m * 100 + 100,
                                        x_m * 100 + 100, outline="orange", width=5)
                canvas.create_rectangle((y_m + 2) * 100, (x_m + 2) * 100, (y_m + 2) * 100 + 100,
                                        (x_m + 2) * 100 + 100, outline="green", width=5)
                canvas.pack()

            if x_m2 != -1 and board[x_m][y_m] != 4 and board[x_m][y_m] != 3:
                canvas.create_rectangle(y_m2 * 100, x_m2 * 100, y_m2 * 100 + 100,
                                        x_m2 * 100 + 100, outline="orange", width=5)
                canvas.create_rectangle((y_m2 - 2) * 100, (x_m2 + 2) * 100, (y_m2 - 2) * 100 + 100,
                                        (x_m2 + 2) * 100 + 100, outline="green", width=5)
                canvas.pack()

            if x_m2 != -1 and (board[x_m][y_m] == 4 or board[x_m][y_m] == 3):

                canvas.create_rectangle(y_m2 * 100, x_m2 * 100, y_m2 * 100 + 100,
                                        x_m2 * 100 + 100, outline="orange", width=5)
                canvas.create_rectangle(y_m * 100, x_m * 100, y_m * 100 + 100,
                                        x_m * 100 + 100, outline="green", width=5)

                canvas.pack()

        else:
            if x_m != -1 and board[x_m][y_m] != 4 and board[x_m][y_m] != 3:
                canvas.create_rectangle(y_m * 100, x_m * 100, y_m * 100 + 100,
                                        x_m * 100 + 100, outline="orange", width=5)
                canvas.create_rectangle((y_m + 2) * 100, (x_m - 2) * 100, (y_m + 2) * 100 + 100,
                                        (x_m - 2) * 100 + 100, outline="green", width=5)
                canvas.pack()


            if x_m2 != -1 and board[x_m][y_m] != 4 and board[x_m][y_m] != 3:


                canvas.create_rectangle(y_m2 * 100, x_m2 * 100, y_m2 * 100 + 100,
                                        x_m2 * 100 + 100, outline="orange", width=5)
                canvas.create_rectangle((y_m2 - 2) * 100, (x_m2 - 2) * 100, (y_m2 - 2) * 100 + 100,
                                        (x_m2 - 2) * 100 + 100, outline="green", width=5)
                canvas.pack()

            if x_m != -1 and (board[x_m][y_m] == 4 or board[x_m][y_m] == 3):

                canvas.create_rectangle(y_m2 * 100, x_m2 * 100, y_m2 * 100 + 100,
                                        x_m2 * 100 + 100, outline="orange", width=5)
                canvas.create_rectangle(y_m * 100, x_m * 100, y_m * 100 + 100,
                                        x_m * 100 + 100, outline="green", width=5)
                canvas.pack()

    if m_move_flag == 1:
        if (colorH == True and turn == 2) or (colorH == False and turn == 1):
            if mFlag == -1:
                if board[x_m][y_m] == 3 or board[x_m][y_m] == 4:
                    if (y1 == x_m and x1 == y_m) and ((turn == 2 and board[y][x] == 4) or (turn == 1 and board[y][x] == 3)):
                        x1, y1 = x, y
                        mFlag = 1
                        canvas.create_rectangle(x1 * 100, y1 * 100, x1 * 100 + 100, y1 * 100 + 100, outline="red",
                                                    width=5)
                        canvas.pack()
                    else:
                        showinfo(title="Информация", message="Совершите обязательный ход")
                elif board[y][x] == 1 or board[y][x] == 2:
                    if ((y1 == x_m + 2 and x1 == y_m + 2) or (y1 == x_m2 + 2 and x1 == y_m2 - 2)) and ((turn == 2 and board[y][x] == 2) or (turn == 1 and board[y][x] == 1)):
                        x1, y1 = x, y
                        mFlag = 1
                        canvas.create_rectangle(x * 100, y * 100, x * 100 + 100, y * 100 + 100, outline="red",
                                        width=5)
                        canvas.pack()
                else:
                    showinfo(title="Информация", message="Совершите обязательный ход")
            else:
                if mFlag != -1:
                    x2, y2 = x, y
                    if (x2 == y_m and y2 == x_m and x1 != x2) or (x2 == y_m2 and y2 == x_m2 and x1 != x2):
                        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]
                        if x2 > x1 and y2 > y1:
                            board[y2 - 1][x2 - 1] = 0
                        if x2 > x1 and y2 < y1:
                            board[y2 + 1][x2 - 1] = 0
                        if x2 < x1 and y2 > y1:
                            board[y2 - 1][x2 + 1] = 0
                        if x2 < x1 and y2 < y1:
                            board[y2 + 1][x2 + 1] = 0
                        mFlag = -1
                        draw_game(board)
                        m_move_flag = 0
                        m_move(colorH, turn)
                        if m_move_flag == 0:
                            draw_game(board)
                            turn_switch(turn)
                        damka(board)
                        end_game(board)
                        draw_game(board)
                        if turn == ComputerCheckers:
                            computer_move(turn, board)


        else:
            if mFlag == -1:
                if board[x_m][y_m] == 4 or board[x_m][y_m] == 3:
                    if (y1 == x_m and x1 == y_m) and ((turn == 2 and board[y][x] == 4) or (turn == 1 and board[y][x] == 3)):
                        x1, y1 = x, y
                        mFlag = 1
                        canvas.create_rectangle(x * 100, y * 100, x * 100 + 100, y * 100 + 100, outline="red",
                                                width=5)
                        canvas.pack()
                    else:
                        showinfo(title="Информация", message="Совершите обязательный ход")
                elif board[y][x] == 1 or board[y][x] == 2:
                    if (y1 == x_m - 2 and x1 == y_m + 2) or (y1 == x_m2 - 2 and x1 == y_m2 - 2):
                        x1, y1 = x, y
                        mFlag = 1
                        canvas.create_rectangle(x * 100, y * 100, x * 100 + 100, y * 100 + 100, outline="red",
                                                width=5)
                        canvas.pack()
                else:
                    showinfo(title="Информация", message="Совершите обязательный ход")
            else:
                if mFlag != -1:
                    x2, y2 = x, y
                    if (x2 == y_m and y2 == x_m and x1 != x2) or (x2 == y_m2 and y2 == x_m2 and x1 != x2):
                        board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]
                        if x2 > x1:
                            board[y2 - 1][x2 - 1] = 0
                        else:
                            board[y2 - 1][x2 + 1] = 0
                        m_move_flag = 0
                        mFlag = -1
                        draw_game(board)
                        m_move(colorH, turn)
                        if m_move_flag == 0:
                            draw_game(board)
                            turn_switch(turn)
                        end_game(board)
                        damka(board)
                        draw_game(board)
                        if turn == ComputerCheckers:
                            computer_move(turn, board)

    if m_move_flag == 0:
        if board[y][x] == turn:
            draw_game(board)
            x1, y1 = x, y
            for i in range(8):
                possible_moves[i] = -1
            checking_moves(x1, y1, turn, colorH)

            mFlag = 1
            canvas.create_rectangle(x * 100, y * 100, x * 100 + 100, y * 100 + 100, outline="red", width=5)
            checking_moves(x1, y1, turn, colorH)
            canvas.create_rectangle(possible_moves[0] * 100, possible_moves[1] * 100, possible_moves[0] * 100 + 100,
                                    possible_moves[1] * 100 + 100, outline="blue", width=5)
            canvas.create_rectangle(possible_moves[2] * 100, possible_moves[3] * 100, possible_moves[2] * 100 + 100,
                                    possible_moves[3] * 100 + 100, outline="blue", width=5)
            canvas.pack()


        elif (board[y][x] == 3 and turn == 1) or (board[y][x] == 4 and turn == 2):

            draw_game(board)
            x1, y1 = x, y
            for i in range(8):
                possible_moves[i] = -1
            checking_moves(x1, y1, turn, colorH)

            canvas.create_rectangle(x * 100, y * 100, x * 100 + 100, y * 100 + 100, outline="red", width=5)
            canvas.pack()

            mFlag = 1
            if possible_moves[0] != -1:
                dop = -1
                for i in range(possible_moves[0] - x1):
                    dop += 1
                    if board[possible_moves[1] + dop][possible_moves[0] - dop] != turn and board[possible_moves[1] + dop][possible_moves[0] - dop] != turn + 2:
                        canvas.create_rectangle((possible_moves[0] - dop) * 100, (possible_moves[1] + dop) * 100,
                                                (possible_moves[0] - dop) * 100 + 100,
                                                (possible_moves[1] + dop) * 100 + 100, outline="blue", width=5)

            if possible_moves[2] != -1:
                dop = -1
                for j in range(possible_moves[2] - x1):
                    dop += 1

                    if board[possible_moves[3] - dop][possible_moves[2] - dop] != turn and board[possible_moves[3] - dop][possible_moves[2] - dop] != turn + 2:
                        canvas.create_rectangle((possible_moves[2] - dop) * 100, (possible_moves[3] - dop) * 100,
                                                (possible_moves[2] - dop) * 100 + 100,
                                                (possible_moves[3] - dop) * 100 + 100, outline="blue", width=5)


            if possible_moves[4] != -1:
                dop = -1
                for j in range(x1 - possible_moves[4]):
                    dop += 1

                    if board[possible_moves[5] + dop][possible_moves[4] + dop] != turn and board[possible_moves[5] + dop][possible_moves[4] + dop] != turn + 2:
                        canvas.create_rectangle((possible_moves[4] + dop) * 100, (possible_moves[5] + dop) * 100,
                                                (possible_moves[4] + dop) * 100 + 100,
                                                (possible_moves[5] + dop) * 100 + 100, outline="blue", width=5)
            if possible_moves[6] != -1:
                dop = -1
                for j in range(x1 - possible_moves[6]):
                    dop += 1

                    if board[possible_moves[7] - dop][possible_moves[6] + dop] != turn and board[possible_moves[7] - dop][possible_moves[6] + dop] != turn + 2:
                        canvas.create_rectangle((possible_moves[6] + dop) * 100, (possible_moves[7] - dop) * 100,
                                                (possible_moves[6] + dop) * 100 + 100,
                                                (possible_moves[7] - dop) * 100 + 100, outline="blue", width=5)
            canvas.pack()

        else:
            if mFlag != -1:
                x2, y2 = x, y
                if (x2 == possible_moves[0] and y2 == possible_moves[1] and board[y1][x1] != 3 and board[y1][x1] != 4) or (x2 == possible_moves[2] and y2 == possible_moves[3] and board[y1][x1] != 3 and board[y1][x1] != 4):
                    board[y1][x1], board[y2][x2] = board[y2][x2], board[y1][x1]
                    if abs(x2-x1) == 2:
                        if (colorH == True and turn == 2) or (colorH == False and turn == 1):
                            if x2 > x1:
                                board[y2 + 1][x2 - 1] = 0
                            else:
                                board[y2 + 1][x2 + 1] = 0
                            end_game(board)
                        else:
                            if x2 > x1:
                                board[y2 - 1][x2 - 1] = 0
                            else:
                                board[y2 - 1][x2 + 1] = 0
                            end_game(board)
                    draw_game(board)


                    turn_switch(turn)
                    damka(board)
                    mFlag = -1
                    draw_game(board)
                    if turn == ComputerCheckers:
                        computer_move(turn, board)
                    for i in range(8):
                        possible_moves[i] = -1

                if board[y1][x1] == 3 or board[y1][x1] == 4:
                    dop = -1
                    for i in range(possible_moves[0] - x1):
                        dop += 1
                        if (x2 == possible_moves[0] - dop and y2 == possible_moves[1] + dop and board[possible_moves[1]][possible_moves[0]] != turn
                                and board[possible_moves[1]][possible_moves[0]] != turn +2):
                            board[y1][x1], board[possible_moves[1] + dop][possible_moves[0] - dop] = \
                            board[possible_moves[1] + dop][possible_moves[0] - dop], board[y1][x1]
                            if x2 > x1 and y2 > y1:
                                board[possible_moves[1] + dop - 1][possible_moves[0] - dop - 1] = 0
                            if x2 > x1 and y2 < y1:
                                board[possible_moves[1] + dop + 1][possible_moves[0] - dop - 1] = 0
                            if x2 < x1 and y2 > y1:
                                board[possible_moves[1] + dop - 1][possible_moves[0] - dop + 1] = 0
                            if x2 < x1 and y2 < y1:
                                board[possible_moves[1] + dop + 1][possible_moves[0] - dop + 1] = 0
                            damka(board)
                            mFlag = -1
                            draw_game(board)
                            turn_switch(turn)
                            if turn == ComputerCheckers:
                                computer_move(turn, board)
                            break
                    dop = -1
                    for i in range(possible_moves[2] - x1):
                        dop += 1
                        if (x2 == possible_moves[2] - dop and y2 == possible_moves[3] - dop and board[possible_moves[3] - dop][possible_moves[2] - dop] != turn
                                and board[possible_moves[3] - dop][possible_moves[2] - dop] != turn +2):
                            board[y1][x1], board[possible_moves[3] - dop][possible_moves[2] - dop] = \
                            board[possible_moves[3] - dop][possible_moves[2] - dop], board[y1][x1]
                            if x2 > x1 and y2 > y1:
                                board[possible_moves[3] - dop - 1][possible_moves[2] - dop - 1] = 0
                            if x2 > x1 and y2 < y1:
                                board[possible_moves[3] - dop + 1][possible_moves[2] - dop - 1] = 0
                            if x2 < x1 and y2 > y1:
                                board[possible_moves[3] - dop - 1][possible_moves[2] - dop + 1] = 0
                            if x2 < x1 and y2 < y1:
                                board[possible_moves[3] - dop + 1][possible_moves[2] - dop + 1] = 0
                            damka(board)
                            mFlag = -1
                            draw_game(board)
                            turn_switch(turn)
                            if turn == ComputerCheckers:
                                computer_move(turn, board)
                            break
                    dop = -1
                    for i in range(x1 - possible_moves[4]):
                        dop += 1
                        if (x2 == possible_moves[4] + dop and y2 == possible_moves[5] + dop and board[possible_moves[5] + dop][possible_moves[4] + dop] != turn
                                and board[possible_moves[5] + dop][possible_moves[4] + dop] != turn +2):
                            board[y1][x1], board[possible_moves[5] + dop][possible_moves[4] + dop] = \
                            board[possible_moves[5] + dop][possible_moves[4] + dop], board[y1][x1]
                            if x2 > x1 and y2 > y1:
                                board[possible_moves[5] + dop - 1][possible_moves[4] + dop - 1] = 0
                            if x2 > x1 and y2 < y1:
                                board[possible_moves[5] + dop + 1][possible_moves[4] + dop - 1] = 0
                            if x2 < x1 and y2 > y1:
                                board[possible_moves[5] + dop - 1][possible_moves[4] + dop + 1] = 0
                            if x2 < x1 and y2 < y1:
                                board[possible_moves[5] + dop + 1][possible_moves[4] + dop + 1] = 0
                            damka(board)
                            mFlag = -1
                            draw_game(board)
                            turn_switch(turn)
                            if turn == ComputerCheckers:
                                computer_move(turn, board)
                            break
                    dop = -1
                    for i in range(x1 - possible_moves[6]):
                        dop += 1
                        if (x2 == possible_moves[6] + dop and y2 == possible_moves[7] - dop and board[possible_moves[7] - dop][possible_moves[6] + dop] != turn
                                and board[possible_moves[7] - dop][possible_moves[6] + dop] != turn +2):
                            board[y1][x1], board[possible_moves[7] - dop][possible_moves[6] + dop] = \
                            board[possible_moves[7] - dop][possible_moves[6] + dop], board[y1][x1]
                            if x2 > x1 and y2 > y1:
                                board[possible_moves[7] - dop - 1][possible_moves[6] + dop - 1] = 0
                            if x2 > x1 and y2 < y1:
                                board[possible_moves[7] - dop + 1][possible_moves[6] + dop - 1] = 0
                            if x2 < x1 and y2 > y1:
                                board[possible_moves[7] - dop - 1][possible_moves[6] + dop + 1] = 0
                            if x2 < x1 and y2 < y1:
                                board[possible_moves[7] - dop + 1][possible_moves[6] + dop + 1] = 0
                            damka(board)
                            mFlag = -1
                            draw_game(board)
                            turn_switch(turn)
                            if turn == ComputerCheckers:
                                computer_move(turn, board)
                            break

            for i in range(8):
                possible_moves[i] = -1

def rungame():
    global  colorH, board, ComputerCheckers
    board, colorH = new_game()
    if colorH == False:
        ComputerCheckers = 2
        computer_move(turn, board)
    else:
       ComputerCheckers = 1

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

ui.pushButtonRegistration.clicked.connect(click_reg)
ui.pushButtonLogin.clicked.connect(click_auth)

window = Tk()
window.title("Шашки-Самоеды")
window.geometry('800x800')
canvas = Canvas(window, width=800,height=800)
window.iconify()

turn = 2
ComputerCheckers = -1
m_move_flag = 0
mFlag = -1
x_m = -1
y_m = -1
x_m2 = -1
y_m2 = -1
possible_moves = [-1, -1, -1, -1, -1, -1, -1, -1]

canvas.bind("<Button-1>", click)
window.mainloop()

sys.exit(app.exec())