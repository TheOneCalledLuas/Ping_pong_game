#Implemento las librerías.
from random import randint
import os
from time import time as time_screenshot
from time import sleep
from pygame import *


#Líneas básicas para el uso de pygame.
init()
mixer.init()
os.system('cls')
mwin = display.set_mode((700, 500))
display.set_caption('Ping-Pong game')
background = transform.scale(image.load('background.png'), (700,500))

#Clase que controla la parte sonora del programa.
class Music_manager():
    def __init__(self):
        self.soundtrack = None
        self.sound = None
        
    
    def play_soundtrack(self, music=None):
        if music != None:
            self.soundtrack = music
        mixer.music.load(music)
        mixer.music.play()
    
    def stop_soundtrack(self):
        mixer.music.pause()
    
    def continue_soundtrack(self):
        mixer.music.unpause()
    
    def play_sound(self, sound=None):
        if sound != None:
            self.sound = sound
        one_sound = mixer.Sound(sound)
        one_sound.set_volume(0.5)
        one_sound.play()
    
mp3 = Music_manager()

#Clase de entidad general de la que pueden derivar los distintos elementos interactuables mostrados en la pantalla.
class entity():
    def __init__(self, xpos, ypos, width, lenght, image =None):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.lenght = lenght
        self.object = None
        self.collide_area = draw.rect(mwin, (0, 150, 0), Rect(self.xpos, self.ypos, self.width, self.lenght))
        self.image = image

    #Método que crea el objeto con su imágen.
    def initialise(self):
        if self.image != None:
            self.object = transform.scale(image.load(self.image), (self.width, self.lenght))
        else:
            raise SyntaxWarning('Se intentó crear un objeto sin imágen.')
    # Método que crea la caja de colisión.
    def create_collide_area(self):
        self.collide_area = draw.rect(mwin, (0, 150, 0), Rect(self.xpos, self.ypos, self.width, self.lenght))
    # Método que muestra el objeto en pantalla.
    def show(self):
        if self.object != None:
            mwin.blit(self.object, (self.xpos, self.ypos))   
        else:
            raise SyntaxWarning('Se intentó mostrar un objeto sin inicializarlo antes.')

# Clase que puede moverse y hereda de la entidad común.
class cinetic_entity(entity):
    def __init__(self, xpos, ypos, width, lenght, speed, image=None):
        self.speed = speed
        super().__init__(xpos, ypos, width, lenght, image)
    
    # Métodos que mueven al personaje de forma intuitiva.
    def horizontal_step(self):
        self.xpos += self.speed
    def vertical_step(self):
        self.ypos += self.speed
    def left_step(self):
        self.xpos -= self.speed
    def right_step(self):
        self.xpos += self.speed
    def up_step(self):
        self.ypos -= self.speed
    def down_step(self):
        self.ypos += self.speed

#Clase de la pelota.
class ball(cinetic_entity):
    def __init__(self, xpos, ypos, width, lenght, speed, image=None):
        super().__init__(xpos, ypos, width, lenght, speed, image)
        self.yspeed = speed
        self.xspeed = speed
    
    # Métodos que mueven la bola de forma que diferencia la velocidad y de la x.
    def horizontal_step(self):
        self.xpos += self.xspeed
    def vertical_step(self):
        self.ypos += self.yspeed



#Objetos que voy a usar.
platform1 = cinetic_entity(25, 200, 25, 100, 2, image='platform_2.png')
platform1.initialise()
platform1.show()
platform2 = cinetic_entity(650, 200, 25, 100, 2, image='platform_2.png')
platform2.initialise()
platform2.show()
ball1 = ball(300, 225, 50, 50, 4, image='ball.png')
ball1.initialise()
ball1.show()

#Variables que condicional el programa y serán usadas posteriormente.
end_condition = False
timer = time.Clock()
is_point = False

def update_screen():
    platform1.create_collide_area()
    platform2.create_collide_area()
    ball1.create_collide_area()
    mwin.blit(background, (0,0))
    platform1.show()
    platform2.show()
    ball1.show()

#Decido la velocidad inicial de la pelota.
if randint(0,1) == 1:
    ball1.xspeed = -4

if randint(0,1) == 1:
    ball1.yspeed = -4

#Bucle del juego
while not end_condition:

    timer.tick(60)
    update_screen()
    display.update()

    #control de salida
    for e in event.get():
        if e.type == QUIT:
            end_condition = True
    
    keys_down = key.get_pressed()
    if keys_down[K_ESCAPE]:
        end_condition = True
    if keys_down[K_w] and platform1.ypos > 0:
        platform1.up_step()
    if keys_down[K_s] and platform1.ypos < 400:
        platform1.down_step()
    if keys_down[K_UP] and platform2.ypos > 0:
        platform2.up_step()
    if keys_down[K_DOWN] and platform2.ypos < 400:
        platform2.down_step()
    
    #Movimiento de la bola.
    if ball1.xpos > 0 and ball1.xpos < 650:
        ball1.horizontal_step()
    else:
        is_point = True
        ball1.xspeed *= -1
    if ball1.ypos > 0 and ball1.ypos < 450:
        ball1.vertical_step()
    else:
        ball1.yspeed *= -1