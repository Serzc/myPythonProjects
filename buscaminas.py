#Horas dedicadas:
#Analisis de requerimientos:    -2
#Diseño de la aplicacion:       -4
#Investigacion de funciones:    -1,5
#Programacion:                  -17
#Pruebas:                       -5
#Elaboracion del doc:           -0
#TOTAL:                         -
from tkinter import *
from tkinter import font
import random as rand
import time 
tablero=[]
tableroShown=[]
rows=""
columns=""
mines=""
lblDimensionError=""
lblMinesError=""
lblWonOrLost=""
txtWonOrLost=""
recommendedMines=""
minesLeft=""
firstTime=True
toggle=False
totalMarked=0
bestTimes=[]
gameEnded=False
path="leaderboard.txt"
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
# cargar estudiantes 
def loadLeaderboard():
    global bestTimes
    try:
        bestTimes = eval(readFile(path))
    except:
        bestTimes=[]
def saveLeaderboard():
               global bestTimes
               writeIntoFile(path, str(bestTimes))
####################################################################################
#Funcion que genera el tablero de juego dado las columnas y filas
def generateGrid(columnas,filas):
    global tablero
    global tableroShown
    row= [ 0 for i in range(columnas)]
    tablero=[ row+[] for i in range(filas)]
    tableroShown=[ row+[] for i in range(filas)]

#Función que coloca las minas al azar en el tablero
def colocarMinas(minas,columnas,filas):
    global tablero
    for i in range(minas):
        x=rand.randint(0,columnas-1)
        y=rand.randint(0,filas-1)
        while tablero[y][x]==-1:
            x=rand.randint(0,columnas-1)
            y=rand.randint(0,filas-1)
        tablero[y][x]=-1
    setHowManyAdjMines(columnas,filas)

#Cambia el número de una casilla al correspondiente según cantidad de minas adyacentes
def setHowManyAdjMines(columnas,filas):
    global tablero
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j]!=-1:
                minasAdyacentes=0
                for k in getAdjacentValues(i,j,filas,columnas):
                    if k==-1:
                        minasAdyacentes+=1
                tablero[i][j]=minasAdyacentes

#devuelve la cantidad de minas adyacentes a una casilla
def getAdjacentValues(i,j,iMax,jMax):
    adjacentPlaces=[(i-1,j-1),(i,j-1),(i+1,j-1),
                    (i-1,j),          (i+1,j),
                    (i-1,j+1),(i,j+1),(i+1,j+1)]
    resultList=[]
    #i es columna j es fila
    for place in adjacentPlaces:
        if not(place[0]==-1 or place[0]==iMax):
            if not(place[1]==-1 or place[1]==jMax):
                resultList+= [tablero[place[0]][place[1]]]
    return resultList

#realiza un click a todas las casillas adyacentes
def clickAdjacentTiles(i,j,iMax,jMax):
    adjacentPlaces=[(i-1,j-1),(i,j-1),(i+1,j-1),
                    (i-1,j),          (i+1,j),
                    (i-1,j+1),(i,j+1),(i+1,j+1)]
    for place in adjacentPlaces:
        if not(place[0]==-1 or place[0]==iMax):   
            if not(place[1]==-1 or place[1]==jMax):
                if not tableroShown[place[0]][place[1]][1]: #if not revealed
                    buttonClick(place[0],place[1])

#Toma las entradas de la ventana de menu y genera la matriz correspondiente
def validateGame():
    global validGame
    global lblWonOrLost
    columnas=str(columns.get())
    filas=str(rows.get())
    minas=str(mines.get())
    if esEntero(columnas) and esEntero(filas):
        lblDimensionError.set("")
        validGame=True
        recommendedMines.set(f"recomendado: {max([int(int(columnas)*int(filas)/5),1])}")
        generateGrid(int(columnas),int(filas))
    else:
        lblDimensionError.set("Valores de dimensiones no apropiados")
        recommendedMines.set("")
        validGame=False
    if esEntero(minas) and validGame:
        if int(minas)<int(columnas)*int(filas):
            validGame=True
            lblMinesError.set("")
            colocarMinas(int(minas),int(columnas),int(filas))
        else:
            validGame=False
            lblMinesError.set("Valor de minas no apropiado")
    else:
        validGame=False
        lblMinesError.set("Valor de minas no apropiado")
    if validateGame:
        lblWonOrLost.set("Juego listo")

#función que cierra la ventana del menú y abre el juego con la info del menú
def startGame():
    global initialTime, gameEnded, totalMarked
    totalMarked=0
    gameEnded=False
    if validGame:
        initialTime=int(time.time())
        [print(i)for i in tablero]
        startMenu.destroy()
        gameWindowFunc()

#función que termina el juego y abre el menu inicial de nuevo, recibe bool que indica si gana o pierde
def endGame(won):
    game.destroy()
    startMenuFunc(won)     
    return

#activa o desactiva la acción de colocar banderas
def toggleMark():
    global toggle
    toggle=not toggle
    if toggle:
        btnToggleMark.config(bg="green")
        print("MARCANDO")
    else:
        btnToggleMark.config(bg="white")
        print("Revelando")
    return

#dada una coordenada, realiza la lógica de clickear una casilla
def buttonClick(i,j):       #cada entrada de tableroShown: #[botón, locked, marked,revealed]
    global totalMarked
    global minesLeft, gameEnded, bestTimes,lblWonOrLost,saved
    print(f"clicked {i},{j}")
    print(f"Adyacentes: {getAdjacentValues(i,j,int(rows.get()),int(columns.get()))}")
    print(tablero[i][j])
    minasRestantes=int(mines.get())-totalMarked
    columnas=int(columns.get())
    filas=int(rows.get())
    gameEnded=False
    won=False
    saved =False
    if toggle:
        if not tableroShown[i][j][1]:
            if minasRestantes>=0 or tableroShown[i][j][2]:
                if not tableroShown[i][j][2]:
                    tableroShown[i][j][0].config(fg="red",text="|◤",bg="white")
                    totalMarked+=1
                else:
                    tableroShown[i][j][0].config(fg="black",text=" ",bg="gray")
                    totalMarked-=1
                minasRestantes=int(mines.get())-totalMarked
                tableroShown[i][j][2]=not tableroShown[i][j][2]
                minesLeft.set(f"Minas faltantes: {minasRestantes}")
        print("MINAS RESTANTES",minasRestantes)
    else:
        if not tableroShown[i][j][2] and not tableroShown[i][j][1]: #si no está marcada ni locked
            if tablero[i][j]==-1:
                print("KABOOOM")
                tableroShown[i][j][0].config(fg="black",text="X",bg="red")
                tableroShown[i][j][1]=True
                tableroShown[i][j][2]=True
                mineRevealer()
                gameEnded=True
                won=False
                #endGame(False)
                
            else:
                print("save")
                if tablero[i][j]==0:
                    tableroShown[i][j][0].config(bg="green",text="")
                    tableroShown[i][j][1]=True
                    clickAdjacentTiles(i,j,int(rows.get()),int(columns.get()))
                else:
                    tableroShown[i][j][1]=True
                    tableroShown[i][j][0].config(text=f"{tablero[i][j]}",fg="black",bg="white")
                tableroShown[i][j][1]=True
   
    if minasRestantes<1 and not won and not gameEnded:
        print("GOT HERE")
        gameEnded=True
        won=True
        for row in range(filas):
            for column in range (columnas):
                if tableroShown [row][column][2]: #si está marcado
                    if tablero[row][column]!=-1:  #si no tiene mina
                        print(f"BRUH, {row} {column}; {tablero[row][column]};{tableroShown [row][column][2]}")
                        gameEnded=False
                        won=False
                        
    if gameEnded:
        if won:
            lblWonOrLost.set("Ganaste!")
            if not saved:
                bestTimes+=[[strTimePassed,elapsedTime,columnas*filas,int(mines.get())]]
                bestTimes.sort(key=getSecondElem)
                saveLeaderboard()
                print(f"added {[[strTimePassed,elapsedTime,columnas*filas,int(mines.get())]]} to {bestTimes}")
                saved=True
            print("Yipeee")
            
        else:
            lblWonOrLost.set("Perdiste...")
            print("BOOO")
    return

#función recursiva que administra el temporizador
def updateTimer(): 
    global lblTiempo, strTimePassed, elapsedTime
    if not gameEnded:
        elapsedTime = time.time() - initialTime 
        minutes=int(elapsedTime)//60
        seconds=int(elapsedTime)%60
        strTimePassed=f"{minutes}:{str((seconds<10)*'0')+str(seconds)}"
        lblTiempo.config(text= strTimePassed)       
        game.after(1000,updateTimer)

#pone todas las minas en X al perder
def mineRevealer():
    for i in range(int(rows.get())):
        for j in range (int(columns.get())):
            tableroShown[i][j][1]=True
            if tablero[i][j]==-1:
                tableroShown[i][j][0].config(fg="black",text="X",bg="red")

def resetGame():
    validateGame()
    global initialTime, gameEnded, totalMarked,toggle,saved
    totalMarked=0
    gameEnded=False
    toggle=False
    saved=False
    if validGame:
        initialTime=int(time.time())
        [print(i)for i in tablero]
        game.destroy()
        gameWindowFunc()
def mainMenu():
    global firstTime
    firstTime=True
    endGame(False)
    return            
                
#========================================================================
#abre la ventana del menu principal
def startMenuFunc(won):
    global startMenu,rows,columns, mines,lblDimensionError,lblMinesError,recommendedMines,validGame,lblWonOrLost,firstTime
    startMenu=Tk()
    startMenu.title("Menu Principal")
    validGame=False
    rows=StringVar()
    columns=StringVar()
    mines=StringVar()
    lblDimensionError=StringVar()
    lblMinesError=StringVar()
    recommendedMines=StringVar()
    lblWonOrLost=StringVar()
    if not firstTime:
        if won:
            lblWonOrLost.set("Ganaste!")
            print("YOU WON")
        else:
            lblWonOrLost.set("Perdiste...")
            print("YOU LOST")
    Label(startMenu,text="BIENVENIDO A BUSCAMINAS",fg="blue",font=('Comic Sans MS', 13)).grid(row=0,column=0)
    entryRow=Entry(startMenu,textvariable=rows,fg="black",font=('Comic Sans MS', 10),width=7)
    entryColumn=Entry(startMenu,textvariable=columns,fg="black",font=('Comic Sans MS', 10),width=7)
    Label(startMenu,text=" Ingrese las dimensiones del tablero:",fg="blue",font=('Comic Sans MS', 12)).grid(row=2,column=0)
    entryRow.grid(row=2,column=3)
    Label(startMenu,text="x",font=('Comic Sans MS', 10)).grid(row=2,column=2)
    entryColumn.grid(row=2,column=1)
    Label(startMenu, text="", textvariable=lblDimensionError, fg='red',font=('Comic Sans MS', 12)).grid(row=3, column=0)
    Label(startMenu,text="Ingrese las cantidad de minas:       ",fg="blue",font=('Comic Sans MS', 12)).grid(row=4,column=0)
    entryMines=Entry(startMenu,textvariable=mines,fg="black",font=('Comic Sans MS', 10),width=7).grid(row=4,column=1)
    Label(startMenu, text="", textvariable=lblMinesError, fg='red',font=('Comic Sans MS', 12)).grid(row=5, column=0)
    Label(startMenu,text="",textvariable=recommendedMines, fg="black",font=('Comic Sans MS', 8)).grid(row=5,column=1)
    Label(startMenu,text="",textvariable=lblWonOrLost,font=('Comic Sans MS', 12),fg="blue").grid(row=10,column=9)
    btnGenerateGrid = Button(startMenu, text='Generar Partida', command=validateGame, font=('Comic Sans MS', 11), width= 12, height = 1)
    btnGenerateGrid.grid(row=10,column=0)
    btnStartGame = Button(startMenu, text='Empezar', command=startGame, font=('Comic Sans MS', 11), width= 12, height = 1)
    btnStartGame.grid(row=11,column=10)
    Button(startMenu, text='Mejores Tiempos', command=scoresWindow, font=('Comic Sans MS', 10), width= 12, height = 1).grid(row=10,column=10)
    firstTime=False
    startMenu.mainloop()

#abre la ventana del juego usando los datos del menú principal
def gameWindowFunc():
    global game,minesLeft,btnToggleMark,lblTiempo,lblWonOrLost
    buttonSize=3
    game=Tk()
    gameArea=Frame(game)
    toolBar=Frame(game)
    botToolBar=Frame(game)
    minesLeft=StringVar()
    currentTime=StringVar()
    lblWonOrLost=StringVar()
    minesLeft.set(f"Minas faltantes: {int(mines.get())-totalMarked}")
    strTimePassed=f"{int((time.time())-initialTime)//60}:{int((time.time())-initialTime)%60}"
    currentTime.set(strTimePassed)
    columnas=int(str(columns.get()))
    filas=int(str(rows.get()))
    game.title("Buscaminas")
    btnToggleMark=Button(toolBar,text="|◤",command=toggleMark,font=("Castellar",10),width=buttonSize,height=buttonSize-5)
    btnToggleMark.grid(column=0,row=0)
    Label(toolBar,text="",textvariable=lblWonOrLost,font=('Comic Sans MS', 12),fg="blue").grid(row=0,column=5)
    lblMinasLeft=Label(toolBar,text="",textvariable=minesLeft,fg="black",font=('Comic Sans MS', 10))
    lblTiempo=Label(botToolBar,text="",fg="black",font=('Comic Sans MS', 10))
    Button(botToolBar,text="Reset",command=resetGame,fg="black",font=('Comic Sans MS', 10)).grid(column=1,row=0)
    Button(botToolBar,text="Main Menu",command=mainMenu,fg="black",font=('Comic Sans MS', 10)).grid(column=2,row=0)
    lblTiempo.grid(column=0,row=0)
    lblMinasLeft.grid(column=1,row=0)
    toolBar.grid(row=0,column=0)
    gameArea.grid(row=1,column=0)
    botToolBar.grid(column=0,row=3)
    for i in range(filas):
        for j in range(columnas):
            button = Button(
                gameArea,
                text=f" ",bg="gray",
                width=buttonSize ,
                height=buttonSize -5,
                command=lambda i=i, j=j: buttonClick(i, j)
            )
            button.grid(row=i, column=j, sticky="nsew")  # Elimina el espacio entre los botones
            tableroShown[i][j] = [button,False,False,False] #[botón, locked, marked,revealed]
    updateTimer()
    game.mainloop()

#abre la ventana con el leaderboard
def scoresWindow():
    scoreWind=Tk()
    print(bestTimes)
    Label(scoreWind,text="Mejores tiempos",fg="blue",font=('Comic Sans MS', 14)).grid(row=0)
    i=1
    for score in bestTimes:
        Label(scoreWind,text=f"{score[0]} Área: {score[2]}, minas {score[3]}",fg="black",font=('Comic Sans MS', 10)).grid(row=i)
        i+=1

#Esta función se obtuvo de internet, no tiene efectos en el programa, es solo una manera de ver los fonts en Tkinter
def fontShower():
    root = Tk()
    root.title('Font Families')
    fonts=list(font.families())
    fonts.sort()

    def populate(frame):
        '''Put in the fonts'''
        listnumber = 1
        for item in fonts:
            label = "listlabel" + str(listnumber)
            label = Label(frame,text=item,font=(item, 16)).pack()
            listnumber += 1

    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas = Canvas(root, borderwidth=0, background="#ffffff")
    frame = Frame(canvas, background="#ffffff")
    vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    populate(frame)


loadLeaderboard()
startMenuFunc(False)