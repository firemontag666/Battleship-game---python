#  se importan las librerias necesarias
import pygame
from pygame.locals import *
import random
import os

#  se inicia el juego y se inicia la fuente
pygame.init()
pygame.font.init()

FPS = pygame.time.Clock()
FPS.tick(30) 


#se cargan las imagenes, botones, sprites y se les da un tamaño de ser necesario
background=pygame.image.load('img/main_screen.png')
background=pygame.transform.scale(background, ((1100, 750)))

start_buttonimg=pygame.image.load('buttons/start_button.png')
menu_buttonimg=pygame.image.load('buttons/menu_button.png')
menu_buttonimg=pygame.transform.scale(menu_buttonimg, ((100, 50)))
next_button=pygame.image.load('buttons/next_button.png')


shipdeck=pygame.image.load('img/shipdeck.png')
shipdeck=pygame.transform.rotate(shipdeck, -90)
shipdeck=pygame.transform.scale(shipdeck, ((550, 290)))

s1 = pygame.Surface((400,400), pygame.SRCALPHA)   
s2 = pygame.Surface((400,400), pygame.SRCALPHA)
s1.fill((255,255,255,128))     
s2.fill((255,255,255,128)) 

hit=pygame.image.load('ships/ShipHit.png')
hit=pygame.transform.scale(hit, ((40, 40)))
hit_rect=hit.get_rect()

not_hit=pygame.image.load('ships/ShipMiss.png')
not_hit=pygame.transform.scale(not_hit, ((40, 40)))
not_hit_rect=not_hit.get_rect()

game=None
#se crean las clases necesarias para el juego
class Button: #Se crea la clase Button para poder crear los botones
    def __init__(self,x,y,image,name): #Se le da una posicion y una imagen
        self.name=name
        self.image=image
        self.imageLarger=self.image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.active=False

    def pressaction(self): #accion que se realiza al presionar el boton
        if self.name=='gamestart':
            self.action()
        elif self.name=='quit':
            quit()
            
    def action(self):
        pass
        #if gamestate==True:
         #   for ship in pFleet:
          #      ship.setmove(False)  
    def quit(self):
        pass
    def draw(self,window): #Se crea la funcion draw para poder dibujar el boton
        window.blit(self.image,self.rect)
        act=False
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse): #Se crea la funcion collidepoint para que el boton pueda ser clickeado
            if click[0]==1 and self.active==False:
                self.active=True
                act=True
                
        if click[0]==0: #Se crea la funcion click para que el boton pueda ser clickeado
            self.active=False
            
        GAMESCREEN.blit(self.image,(self.rect.x,self.rect.y)) #Se dibuja el boton

        return act #Se retorna la accion del boton
    
class Ship: #Se crea la clase Ship para poder crear los barcos
    def __init__(self, name, img, pos, size,move=True): #Se le da un nombre, una imagen, una posicion y un tamaño
        self.name = name
        self.pos = pos
        #  Load the Vertical image
        self.vImage = loadImage(img, size)
        self.vImageWidth = self.vImage.get_width()
        self.vImageHeight = self.vImage.get_height()
        self.vImageRect = self.vImage.get_rect()
        self.vImageRect.topleft = pos
        #  Load the Horizontal image
        self.hImage = pygame.transform.rotate(self.vImage, -90)
        self.hImageWidth = self.hImage.get_width()
        self.hImageHeight = self.hImage.get_height()
        self.hImageRect = self.hImage.get_rect()
        self.hImageRect.topleft = pos
        #  Image and Rectangle
        self.image = self.vImage
        self.rect = self.vImageRect
        self.rotation = False
        #  Ship is current selection
        self.active = False
        self.move=move

    def setmove(self,move): #Se crea la funcion setmove para poder mover los barcos
        self.move=move   
        
    def selectShipAndMove(self): #Se crea la funcion selectShipAndMove para poder seleccionar el barco y moverlo
        while self.active == True and self.move==True:
            self.rect.center = pygame.mouse.get_pos()
            updateGameScreen(GAMESCREEN)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.checkForCollisions(pFleet):
                        if event.button == 1:
                            self.hImageRect.center = self.vImageRect.center = self.rect.center
                            self.active = False

                    if event.button == 3:
                        self.rotateShip()
            
            


    def rotateShip(self, doRotation=False): #Se crea la funcion rotateShip para poder rotar los barcos
        if self.active or doRotation == True:
            if self.rotation == False:
                self.rotation = True
            else:
                self.rotation = False
            self.switchImageAndRect()


    def switchImageAndRect(self): #Se crea la funcion switchImageAndRect para poder cambiar la imagen y el rectangulo
        if self.rotation == True:
            self.image = self.hImage
            self.rect = self.hImageRect
        else:
            self.image = self.vImage
            self.rect = self.vImageRect
        self.hImageRect.center = self.vImageRect.center = self.rect.center


    def checkForCollisions(self, shiplist): #Se crea la funcion checkForCollisions para poder verificar si hay colisiones
        slist = shiplist.copy()
        slist.remove(self)
        for item in slist:
            if self.rect.colliderect(item.rect):
                return True
        return False


    def checkForRotateCollisions(self, shiplist): #Se crea la funcion checkForRotateCollisions para poder verificar si hay colisiones al rotar
        slist = shiplist.copy()
        slist.remove(self)
        for ship in slist:
            if self.rotation == True:
                if self.vImageRect.colliderect(ship.rect):
                    return True
            else:
                if self.hImageRect.colliderect(ship.rect):
                    return True
        return False


    def returnToDefaultPosition(self): #Se crea la funcion returnToDefaultPosition para poder regresar a la posicion inicial
        if self.rotation == True:
            self.rotateShip(True)

        self.rect.topleft = self.pos
        self.hImageRect.center = self.vImageRect.center = self.rect.center


    def snapToGridEdge(self, gridCoords): #Se crea la funcion snapToGridEdge para que el barco no pueda salirse del tablero
        if self.rect.topleft != self.pos:
            if self.rect.left > gridCoords[0][-1][0] + 40 or \
                    self.rect.right < gridCoords[0][0][0] or \
                    self.rect.top > gridCoords[-1][0][1] + 40 or \
                    self.rect.bottom < gridCoords[0][0][1]:
                self.returnToDefaultPosition()

            elif self.rect.right > gridCoords[0][-1][0] + 40:
                self.rect.right = gridCoords[0][-1][0] + 40
            elif self.rect.left < gridCoords[0][0][0]:
                self.rect.left = gridCoords[0][0][0]
            elif self.rect.top < gridCoords[0][0][1]:
                self.rect.top = gridCoords[0][0][1]
            elif self.rect.bottom > gridCoords[-1][0][1] + 40:
                self.rect.bottom = gridCoords[-1][0][1] + 40
            self.vImageRect.center = self.hImageRect.center = self.rect.center


    def snapToGrid(self, gridCoords): #Se crea la funcion snapToGrid para que el barco se pueda posicionar en el tablero
        for rowX in gridCoords:
            for cell in rowX:
                if self.rect.left >= cell[0] and self.rect.left < cell[0] + CELLSIZE \
                        and self.rect.top >= cell[1] and self.rect.top < cell[1] + CELLSIZE:
                    if self.rotation == False:
                        self.rect.topleft = (cell[0] + (CELLSIZE - self.image.get_width()) // 2, cell[1])
                    else:
                        self.rect.topleft = (cell[0], cell[1] + (CELLSIZE - self.image.get_height()) // 2)

        self.hImageRect.center = self.vImageRect.center = self.rect.center


    def draw(self, window): #Se crea la funcion draw para poder dibujar el barco
        window.blit(self.image, self.rect)
       
class player: #Se crea la clase player para poder crear al jugador
    def __init__(self): #Se le da un turno
        self.turn=True

    def attack(self,grid,logicgrid): #Se crea la funcion attack para poder atacar
        
        x,y=pygame.mouse.get_pos()
        if x>=grid[0][0][0] and x<=grid[0][-1][0]+40 and y>=grid[0][0][1] and y<=grid[-1][0][1]+40:
            for i,filax in enumerate(grid):
                for j,colx in enumerate(filax):
                    if x>=colx[0] and x<colx[0]+40 and y>=colx[1] and y>=colx[1] and y<=colx[1]+40:
                        if logicgrid[i][j]!=' ':
                            if logicgrid[i][j]=='0':
                                print('jugador:hit')
                                MARKER.append(marker(hit,grid[i][j],'hit'))
                                logicgrid[i][j]='T'
                                
                                self.turn=False
                        else:
                            logicgrid[i][j]='X'
                            print('jugador: miss')
                            
                            MARKER.append(marker(not_hit,grid[i][j],'no hit'))
                            self.turn=False

class bot:
    def __init__(self): #Se le da un turno y un status
        self.turn=False
        self.status=self.puterstatus('processing')
        self.name='puter'

    def puterstatus(self,msg): #Se crea la funcion puterstatus para poder mostrar el status del bot
        image=pygame.font.Font('misc/pixel-li.ttf',30)
        mensaje=image.render(msg,1,(255,255,255))
        return mensaje

    def shoot(self,logicgrid): #Se crea la funcion shoot para poder disparar
        vchoice=False
        while not vchoice:
            filax=random.randint(0,9)
            colx=random.randint(0,9)

            if logicgrid[filax][colx]==' ' or logicgrid[filax][colx]=='0':
                vchoice=True
        if logicgrid[filax][colx]=='0':
            print('puter:hit')
            MARKER.append(marker(hit,pGameGrid[filax][colx],'hit'))
            logicgrid[filax][colx]='T'
            self.turn=False
        else:
            logicgrid[filax][colx]='X'
            print('puter:miss')
            MARKER.append(marker(not_hit,pGameGrid[filax][colx],'no hit'))
            self.turn=False
        return self.turn
    
    def draw(self,window): #Se crea la funcion draw para poder dibujar el status del bot
        if self.turn==True:
            window.blit(self.status,(cGameGrid[0][0][0]-CELLSIZE,cGameGrid[-1][-1][-1]+CELLSIZE))
        
class marker: #Se crea la clase marker para poder crear los marcadores de los disparos
    def __init__(self,image,pos,action): #Se le da una imagen, una posicion y una accion
        self.image=image
        self.rect=self.image.get_rect()
        self.pos=pos
        self.rect.topleft=self.pos
        self.action=action
        self.timer=pygame.time.get_ticks()
    def draw(self,window): #Se crea la funcion draw para poder dibujar el marcador
        window.blit(self.image,self.rect)
        
# se crean las funciones para el tablero del juego
      
def createGameGrid(rows, cols, cellsize, pos): #hace un tablero con las coordenadas de cada celda
    startX = pos[0]
    startY = pos[1]
    coordGrid = []
    for row in range(rows):
        rowX = []
        for col in range(cols):
            rowX.append((startX, startY))
            startX += cellsize
        coordGrid.append(rowX)
        startX = pos[0]
        startY += cellsize
    return coordGrid

def createGameLogic(rows, cols): #crea el tablero logico en la consola con espacios vacios
    gamelogic = []
    for row in range(rows):
        rowX = []
        for col in range(cols):
            rowX.append(' ')
        gamelogic.append(rowX)
    return gamelogic

def updateGameLogic(coorGrid,shiplist,gamelogic): #actualiza el tablero logico con los barcos, tiros fallidos y tiros acertados
    for i,rowX in enumerate(coorGrid):
        for j,colX in enumerate(rowX):
            if gamelogic[i][j]=='T' or gamelogic[i][j]=='X':
                continue
            else:
                gamelogic[i][j]=' '
                for ship in shiplist:
                    if pygame.rect.Rect(colX[0],colX[1],40,40).colliderect(ship.rect):
                        gamelogic[i][j]='0'
                        
def showGridOnScreen(window, cellsize, playerGrid, computerGrid): #dibuja el tablero en la pantalla de ambos jugadores
    gamegrids = [playerGrid, computerGrid]
    for grid in gamegrids:
        for row in grid:
            for col in row:
                pygame.draw.rect(window, (0, 0, 0), (col[0], col[1], cellsize, cellsize), 1)

def printGameLogic(): #imprime el tablero logico en la consola
    print('Player Grid'.center(50, '#'))
    for _ in pGameLogic:
        print(_)
    print('Computer Grid'.center(50, '#'))
    for _ in cGameLogic:
        print(_)

def loadImage(path, size, rotate=False): #carga las imagenes de los barcos
    
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    if rotate == True:
        img = pygame.transform.rotate(img, -90)
    return img

def createFleet():#crea la flota de barcos
    fleet = []
    for name in FLEET.keys():
        fleet.append(
            Ship(name,
                 FLEET[name][1],
                 FLEET[name][2],
                 FLEET[name][3])
        )
    return fleet

def sortFleet(ship, shiplist): #organiza la lista de barcos
    
    shiplist.remove(ship)
    shiplist.append(ship)

def randomize_position(shipdic,grid): #Se crea la funcion randomize position para poder posicionar los barcos de manera aleatoria
    placeships=[]
    for i,ship in enumerate(shipdic):
        validpos=False
        while validpos==False:
            ship.returnToDefaultPosition()
            rotation=random.choice([True,False])
            if rotation==True:
                yaxis=random.randint(0,9)
                xaxis=random.randint(0,9-(ship.hImage.get_width()//40))
                ship.rotateShip(True)
                ship.rect.topleft=grid[yaxis][xaxis]
            else:
                yaxis=random.randint(0,9-(ship.vImage.get_height()//40))
                xaxis=random.randint(0,9)
                ship.rect.topleft=grid[yaxis][xaxis]
            if len(placeships)>0:
                for item in placeships:
                    if ship.rect.colliderect(item.rect):
                        validpos=False
                        break
                    else:
                        validpos=True
            else:
                validpos=True
        placeships.append(ship)
        updateGameLogic

def action(gamestate): #Se crea la funcion action para poder iniciar el juego
    if gamestate==True:
        return False
    else:
        return True

def turnos(user,pc): #Se crea la funcion turnos para poder alternar los turnos entre el jugador y el bot
    if user.turn==True:
        pc.turn=False
    else:
        pc.turn=True
        if not pc.shoot(pGameLogic):
            user.turn=True

def quit(): #Se crea la funcion quit para poder cerrar el juego y llevar al menu principal
    
    os.system('python Battleship_main.py')
    os.system('taskkill /f /im python.exe')


def updateGameScreen(window): #Se crea la funcion updateGameScreen para poder actualizar la pantalla del juego
    global status
    window.fill((0, 0, 0))
    window.blit(background,(0,0))
    window.blit(shipdeck,((30,455)))
    window.blit(s1,(40,50))
    window.blit(s2,(SCREENWIDTH - (ROWS * CELLSIZE)-40, 50))
    showGridOnScreen(window, CELLSIZE, pGameGrid, cGameGrid)
    #randomize_hit(cGameGrid,window,True)
    
    for ship in pFleet:
        ship.draw(window)
        ship.snapToGridEdge(pGameGrid)
        ship.snapToGrid(pGameGrid)
    
    for ship in cFleet:
        #ship.draw(window)
        ship.snapToGridEdge(cGameGrid)
        ship.snapToGrid(cGameGrid)
    
    for Button in BUTTONS:
        Button.draw(window)

    for item in MARKER:
        item.draw(window)
    puter.draw(window)
    updateGameLogic(pGameGrid,pFleet,pGameLogic)
    updateGameLogic(cGameGrid,cFleet,cGameLogic)
    pygame.display.update()


#variables globales del juego
SCREENWIDTH = 1100
SCREENHEIGHT = 750
ROWS = 10
COLS = 10
CELLSIZE = 40
gamestart=True

# inicializacion de pygame
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Battleship')
pygame.display.set_icon(pygame.image.load('img/icon.png'))

#carga musica
music=pygame.mixer.music.load('misc/music.wav')
pygame.mixer.music.play(-1)
#pygame.mixer.music.set_volume(0.01)

#crea diccionario de flotilla para crearla mas adelante
FLEET = {
    'battleship': ['battleship', 'ships/ShipBattleshipHull.png', (125, 485), (30, 185)],
    'cruiser': ['cruiser', 'ships/ShipCruiserHull.png', (200,  485), (30, 185)],
    'destroyer': ['destroyer', 'ships/ShipDestroyerHull.png', (275,  485), (20, 135)],
    'patrol boat': ['patrol boat', 'ships/ShipPatrolHull.png', (425,  485), (10, 85)],
    'submarine': ['submarine', 'ships/ShipSubMarineHull.png', (350,  485), (20, 135)],
    'carrier': ['carrier', 'ships/ShipCarrierHull.png', (50,  470), (35, 225)],
    'rescue ship': ['rescue ship', 'ships/ShipRescue.png', (500,  485), (10, 85)]
}

#crea la lista de botones
BUTTONS=[
    Button(760,570,start_buttonimg,'gamestart'),
    Button(810,650,menu_buttonimg,'quit')
]

# crea variables de tablero, flota y marcadores
pGameGrid = createGameGrid(ROWS, COLS, CELLSIZE, (40, 50))
pGameLogic = createGameLogic(ROWS, COLS)
pFleet = createFleet()

cGameGrid = createGameGrid(ROWS, COLS, CELLSIZE, (SCREENWIDTH - (ROWS * CELLSIZE)-40, 50))
cGameLogic = createGameLogic(ROWS, COLS)
cFleet = createFleet()
randomize_position(cFleet,cGameGrid)

MARKER=[]

printGameLogic()



#  crea a los jugadores
player1=player()
puter=bot()

#  loop principal del juego
RUNGAME = True
while RUNGAME:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNGAME = False 
        elif event.type == pygame.MOUSEBUTTONDOWN: #Se crea la funcion MOUSEBUTTONDOWN para poder usar el mouse
            if event.button == 1:
                if gamestart==True:
                    for ship in pFleet:
                        if ship.rect.collidepoint(pygame.mouse.get_pos()):
                            ship.active = True
                            sortFleet(ship, pFleet)
                            ship.selectShipAndMove()
                else:
                    if player1.turn==True:
                        player1.attack(cGameGrid,cGameLogic)
                    
                for Button in BUTTONS: #Se crea la funcion BUTTONS para poder usar los botones
                    if Button.rect.collidepoint(pygame.mouse.get_pos()):
                        Button.pressaction()
                        if Button.name=='gamestart':
                            status=action(gamestart)
                            gamestart=status
                        elif Button.name=='quit':
                            quit()

            elif event.button == 2: #si se presiona el boton de en medio se imprimira el tablero logico en la consola
                printGameLogic()

            elif event.button == 3: #si se presiona el boton derecho del mouse se rotara el barco
                if gamestart==True:
                    for ship in pFleet:
                        if ship.rect.collidepoint(pygame.mouse.get_pos()) and not ship.checkForRotateCollisions(pFleet):
                            ship.rotateShip(True)
        
        
    updateGameScreen(GAMESCREEN)
    turnos(player1,puter)  #Se crea la funcion turnos para poder alternar los turnos entre el jugador y el bot


pygame.quit() #Se cierra el juego