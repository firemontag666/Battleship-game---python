#se importan las librerias necesarias
import pygame
from pygame.locals import *
import sys
import time
import pyfiglet



#se inica pygame y se inicia la fuente
pygame.init()
pygame.font.init()

#se crea la barra de carga y se imprime el titulo con texto ascii
bar_len=24
elements=['-','\\','l','/']
print(pyfiglet.figlet_format('Battleship', font = "slant"))
#se crea la barra de carga gracias a un loop y se le da un tiempo de espera para que se repita
for i in range(bar_len+1):
    frame=i%len(elements)
    print(f'\r[{elements[frame]*i:=<{bar_len}}]',end='')
    time.sleep(0.09)


#se crea la pantalla y sus dimensiones y se le da un titulo e icono
DISPLAYSURF = pygame.display.set_mode((1100,750))
DISPLAYSURF.fill((255,255,255))
pygame.display.set_caption('Battlefield')
pygame.display.set_icon(pygame.image.load('img/icon.png'))

#Se asignan los FPS del juego
FPS = pygame.time.Clock()
FPS.tick(30) 

#En este apartado se cargan todas las imagenes, botones, sprites y se les da un tamaño de ser necesario


background=pygame.image.load('img/main_screen.png')
background=pygame.transform.scale(background, ((1100, 750)))

start_button=pygame.image.load('buttons/start_button.png')
quit_button=pygame.image.load('buttons/quit_button.png')
settings_button=pygame.image.load('buttons/settings_button.png')
next_button=pygame.image.load('buttons/next_button.png')

title=pygame.image.load('logos/title_logo.png')
s_title=pygame.image.load('logos/Settings_logo.png')
plan_logo=pygame.image.load('logos/Plan_strategy_logo.png')
instructions=pygame.image.load('logos/instructions_logo.png')
inst1=pygame.image.load('logos/inst.png')
inst2=pygame.image.load('logos/inst2.png')



#Se obtienen los rectangulos de las imagenes para poder usarlos en los botones,sprites y titulos

rt=title.get_rect()
rts=s_title.get_rect()
rti=instructions.get_rect()
inst1r=inst1.get_rect()
inst2r=inst2.get_rect()

rq=quit_button.get_rect()
rss=settings_button.get_rect()
rs=start_button.get_rect()
rn=next_button.get_rect()

rpl=plan_logo.get_rect()



#Se carga la musica del juego y se le da un loop infinito
music=pygame.mixer.music.load('misc/music.wav')
pygame.mixer.music.play(-1)

#Se crean las fuentes para los titulos y textos
fonttitle=pygame.font.SysFont('PIXEL-LI.TTF', 100)


    
#Se crean las variables globales para el juego
game_state = "start_menu" 
cellsizestrat=50
cellsizemain=40
filas=10
columnas=10


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////Empieza codigo de juego////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#Se crea la clase boton para poder usarla en el juego
class Button:
    def __init__(self,x,y,image): #Se le da una posicion y una imagen
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False

    def draw(self): #Se crea la funcion draw para poder dibujar el boton
        act=False
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse): #Se crea la funcion collidepoint para que el boton pueda ser clickeado
            if click[0]==1 and self.clicked==False:
                self.clicked=True
                act=True
                
        if click[0]==0: #Se crea la funcion click para que el boton pueda ser clickeado
            self.clicked=False
            
        DISPLAYSURF.blit(self.image,(self.rect.x,self.rect.y)) #Se dibuja el boton

        return act #Se retorna la accion del boton


#Se crean los botones para el juego
startbtn=Button(1100//2-rs.width//2,370,start_button) 
settingsbtn=Button(1100//2-rss.width//2,470,settings_button)
quitbtn=Button(1100//2-rq.width//2,570,quit_button)
nextbtn=Button((1100//2+500//2)-rn.width-10,690,next_button)


def dmenu(): #Se crea la funcion dmenu para poder crear la pantalla de inicio
    global game_state
    DISPLAYSURF.blit(background, (0,0))
    DISPLAYSURF.blit(title,(1100//2-rt.width//2,190))
    
    if startbtn.draw()==True:
        pygame.display.update()
        game_state= 'gamestart'
    elif settingsbtn.draw()==True:
        pygame.display.update()
        game_state= 'settings'     
    elif quitbtn.draw()==True:
        pygame.display.update()
        game_state= 'quit'
    pygame.display.update()
#Menus del juego
def settings(): #Se crea la funcion settings para poder crear la pantalla de configuracion
    global game_state
    quitbtn=Button(1100//2-rq.width//2,670,quit_button)
    DISPLAYSURF.fill((255,255,255))
    DISPLAYSURF.blit(background, (0,0))
    DISPLAYSURF.blit(instructions,(1100//2-rti.width//2,150))
    DISPLAYSURF.blit(inst1,(1100//2-inst1r.width//2,300))
    DISPLAYSURF.blit(inst2,(1100//2-inst2r.width//2,470))
    if quitbtn.draw()==True:
        pygame.display.update()
        game_state= 'start_menu'
    pygame.display.update()

def quitgame(): #Se crea la funcion quitgame para poder salir del juego
    pygame.quit()
    sys.exit()

while True:	 #Se crea el loop principal del juego
    for event in pygame.event.get(): #Se crea el loop de eventos del juego
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    if game_state=='start_menu': #revisa el estado del juego para asignar la pantalla correspondiente
        dmenu()
    elif game_state=='quit':
        quitgame()
    elif game_state=='settings':
        settings()
    elif game_state=='gamestart':
      with open('Battleship_main2.py') as f:
          exec(f.read())  #se llama al programa del juego

    pygame.display.update() #Se actualiza la pantalla

    

