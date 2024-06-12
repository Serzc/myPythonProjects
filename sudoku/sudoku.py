#Horas dedicadas:
#Analisis de requerimientos:    -2
#Diseño de la aplicacion:       -
#Investigacion de funciones:    -1
#Programacion:                  -
#Pruebas:                       -
#Elaboracion del doc:           -
#TOTAL:                         -
from tkinter import *
import time
import copy
import random
####################################################################################
#COMMONS
#esEntero evalúa si un valor se puede convertir en entero
def esEntero(value):
    try:
        entero=int(value)
        if type(entero) == int:
            return True
        return False
    except:
        return False
#given a list, returns its second element or [] if there's none
def getSecondElem(list):
    try:
        return list[1]
    except:
        return []
#I: path with filename, string to write
#O: none
def writeIntoFile (path, string):
               fo = open(path, "w")
               fo.write(string)
               fo.close()   
#I: path with filename
#O: string with whole file content
def readFile(path):
               fo = open(path, "r")
               res = fo.read()
               fo.close()
               return res

####################################################################################
posicion={
      1:(0,0),2:(0,1),3:(0,2),
      4:(1,0),5:(1,1),6:(1,2),
      7:(2,0),8:(2,1),9:(2,2),
}

#verifica si colocar un número en un row y col es válido
#E:matriz,int,int,int
#S:bool
def is_safe(board, row, col, num):
    # Verificar si el número ya está en la fila
    for x in range(9):
        if board[row][x] == num:
            return False

    # Verificar si el número ya está en la columna
    for x in range(9):
        if board[x][col] == num:
            return False

    # Verificar si el número ya está en la subcuadrícula 3x3
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

#resuelve el sudoku
#E:matriz
#S:bool y cambia la matriz
def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True  # No hay más ubicaciones vacías, se resolvió el Sudoku
    row, col = empty

    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # Deshacer el cambio (backtrack)

    return False

#encuentra el primer lugar vacío
#E:matriz
#S:tuple i,j o None
def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j) 
    return None
#prints a board into console
def print_board(board):
    for row in board:
        print(" ".join(str(num) for num in row))
#Dado un frame y un board, genera una serie de botones dentro del frame
#Devuelve una matriz con los botones
def generateButtons(frame,board):
    buttons=[]
    
    for i in range(len(board)):
        row=[]
        for j in range(len(board[0])):
            if board[i][j]!=0:
                btnText=board[i][j]
            else:
                btnText=""
            button = Button(
                frame,
                text=f"{btnText}",bg="white",
                width=4 ,
                height=2 ,
                command=lambda i=i, j=j: buttonClick(i, j)
            )
            row+=[button]
            button.grid(row=i, column=j, sticky="nsew")# Elimina el espacio entre los botones
        buttons+=[copy.copy(row)]
    return buttons

def generateKeyPad(frame,keyPadList,activeNum):
     for num in range(1,10):
        button = Button(
                    frame,
                    text=f"{num}",bg="gray",
                    width=5 ,
                    height=3 ,
                    command=lambda num=num, activeNum=activeNum: keyPadClick(num,activeNum)
                )
        button.grid(row=posicion[num][0],column=posicion[num][1])
        keyPadList+=[button]

def setAllButtonsColor(board,color):
    for row in board:
        for button in row:
            button.configure(bg=color)

def setRowColAndSimilarColor(buttonBoard,i,j):
     num=board[i][j]
     start_row = i - i % 3
     start_col = j - j % 3
     
     for row in range(3):
        for col in range(3):
            buttonBoard[row + start_row][col + start_col].configure(bg="light cyan")
     for row in range(len(buttonBoard)):
          for col in range(len(buttonBoard[0])):
                if row==i or col==j:
                    buttonBoard[row][col].configure(bg="light cyan")
                if board[row][col]==num and num!=0:
                    buttonBoard[row][col].configure(bg="sky blue")
 
def keyPadClick(num,activeNum):
     for i in range(len(activeNum)):
          activeNum[i]=False 
     activeNum[num-1]=num
     setAllButtonsColor([keyPadList],"gray")
     keyPadList[num-1].configure(bg="mint cream")
     return

def buttonClick(i,j):
     setAllButtonsColor(gameButtons,"white")
     setRowColAndSimilarColor(gameButtons,i,j)
     gameButtons[i][j].configure(bg="SteelBlue2")
     
     return

def placeButtonClick(activeNum):
     for i in activeNum:
          if i:
               print("placed",i)

def notesButtonClick(activeNum):
     for i in activeNum:
          if i:
               print("noted",i)

def updateTimer(initialTime,root,lblTiempo): 
    global strTimePassed, elapsedTime
    if not gameOver:
        elapsedTime = time.time() - initialTime 
        minutes=int(elapsedTime)//60
        seconds=int(elapsedTime)%60
        strTimePassed=f"{minutes}:{str((seconds<10)*'0')+str(seconds)}"
        lblTiempo.config(text= strTimePassed)       
        root.after(1000, lambda initialTime=initialTime,root=root,lblTiempo=lblTiempo:updateTimer(initialTime,root,lblTiempo))
####################################################################################
#Ventanas
def gameWindow(board):
    global gameButtons, keyPadList,gameOver
    game=Tk()
    gameOver=False
    initialTime=time.time()
    gameArea=Frame(game)                            #Area Sudoku
    gameArea.grid(row=1,column=0,rowspan=2)
    gameButtons=generateButtons(gameArea,board)
    Label(game,width=5).grid(column=1)              #Espacio

    sideButtonBar=Frame(game)                       #Barra con botones para juego
    sideButtonBar.grid(row=2,column=2)

    topToolBar=Frame(game)
    topToolBar.grid(row=0,column=0)

    keyPad=Frame(game)                              #Keypad
    keyPad.grid(row=1,column=2)
    keyPadList=[]
    activeNum=[False for i in range(9)]
    generateKeyPad(keyPad,keyPadList,activeNum)

    placeButton=Button(sideButtonBar,               #PlaceButton
                       text="Place Number", 
                       command=lambda activeNum=activeNum:placeButtonClick(activeNum))
    placeButton.grid(row=1,column=0)

    notesButton=Button(sideButtonBar,               #NotesButton
                       text="Note",
                        command=lambda activeNum=activeNum:notesButtonClick(activeNum))
    notesButton.grid(row=1,column=1)

    lblTiempo=Label(topToolBar,text="jiji",fg="black",font=('Comic Sans MS', 10))
    lblTiempo.grid(row=0,column=1)
    updateTimer(initialTime,game,lblTiempo)
    
    game.mainloop()

def main():
    # Ejemplo de un Sudoku parcialmente completado
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
"""
    if solve_sudoku(board):
        print_board(board)
    else:
        print("No solution exists")
"""
"""
if __name__ == "__main__":
    main()
"""
board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
gameWindow(board)