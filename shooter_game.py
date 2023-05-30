# ¡Crea tu propio juego de disparos!
from random import randint
import os
from time import time as time_screenshot
from time import sleep
from pygame import *

init()
mixer.init()
os.system('cls')
mwin = display.set_mode((700, 500))
display.set_caption('Tirador')
background = transform.scale(image.load('galaxy.jpg'), (700,500))
if False:
    # clase padre para otros objetos
    class GameSprite(sprite.Sprite):
        # constructor de clase
        def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
            # llamamos al constructor de la clase (Sprite):
            sprite.Sprite.__init__(self)

            # cada objeto debe almacenar una propiedad image
            self.image = transform.scale(image.load(player_image), (size_x, size_y))
            self.speed = player_speed

            # cada objeto debe almacenar la propiedad rect en la cual está inscrito
            self.rect = self.image.get_rect()
            self.rect.x = player_x
            self.rect.y = player_y

        # método que dibuja al personaje en la ventana
        def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))


    # clase del jugador principal
    class Player(GameSprite):
        pass

enemies_list = list()
bullet_list = list()
asteroid_list = list()
points_counter = 0
doshow_explosion = False

# Clase reproductora de música.
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

# Clase del tipo jugador, que puede disparar.
class Player(cinetic_entity):
    def __init__(self, xpos, ypos, width, lenght, speed, image=None):
        super().__init__(xpos, ypos, width, lenght, speed, image)
        self.shoot_timer = time_screenshot()
        self.lifes = 3
        self.super_ready = False
        self.super_timer = time_screenshot() - 5
        self.explosion = None
        self.is_recharging = False
        self.recharging_time = 0
        self.bullets_left = 10


    def create_explosion(self, x, y):
        self.explosion = entity(x, y, 100, 100, image='explosion.png')
        self.explosion.initialise()

    def check_super_ready(self):
        current_time = time_screenshot()
        if (current_time - self.super_timer) >= 5:
            self.super_ready = True
            return True
        else:
            self.super_ready = False
            return False


    def super_ability(self):
        global points_counter
        self.check_super_ready()
        if self.super_ready:
            self.super_timer = time_screenshot()
            position = mouse.get_pos()
            expl_x = position[0] - 50
            expl_y = position[1] - 50
            self.create_explosion(expl_x, expl_y)
            self.explosion.create_collide_area()
            for e in enemies_list:
                if e.collide_area.colliderect(self.explosion.collide_area):
                    enemies_list.remove(e)
                    del e
                    points_counter += 5

    def check_recharging(self):
        actual_time = time_screenshot()
        if (actual_time - self.recharging_time) >= 1.5:
            self.is_recharging = False
            return False
        else:
            return True    
        
    def shoot(self):
        global points_counter
        act_time = time_screenshot()
        if (actual_time - self.recharging_time) >= 1.5:
            self.is_recharging = False
        if len(bullet_list) <= 9 and act_time - self.shoot_timer > 0.25 and not self.is_recharging:
            mp3.play_sound('fire.ogg')
            self.shoot_timer = act_time
            bullet_name = 'bullet_' + str(len(bullet_list) + 1)
            bullet_creation = f' = cinetic_entity({self.xpos + (self.width / 2) - 10}, {self.ypos - (self.lenght)}, 20, 50, 3, image= "bullet.png")'
            bullet_creation_line = bullet_name + bullet_creation
            exec(bullet_creation_line)
            exec(f'{bullet_name}.initialise()')
            exec(f'bullet_list.append({bullet_name})')
            points_counter -= 1
            self.bullets_left -= 1
            if self.bullets_left == 0:
                self.is_recharging = True
                self.recharging_time = time_screenshot()
                self.bullets_left = 10
    
    

    

def refresh_screen():
    pos = mouse.get_pos()
    mouse_target = entity(pos[0] - 25, pos[1] - 25, 50, 50, image = 'red_target_1-removebg-preview.png')
    mouse_target.initialise()
    mouse_target.show()
    player.create_collide_area()
    for b in bullet_list:
        b.create_collide_area()
    for e in enemies_list:
        e.create_collide_area()
    for a in asteroid_list:
        a.create_collide_area()
    mwin.blit(background, (0,0))
    
    lifes_stats = player_lifes.render(f'Vidas restantes: {player.lifes}', True, (255,255,255))
    point_text = point_stats.render(f'Puntuación: {points_counter}', True, (255,255,255))
    bullets_left = player_lifes.render(f'Balas restantes: {player.bullets_left}', True, (255,255,255))
    if player.check_super_ready():
        ultimate_text = player_lifes.render(f'Habilidad lista en: YA', True, (255,255,255))
    else:
        time_now = time_screenshot()
        ultimate_text = player_lifes.render(f'(Click izq) Habilidad lista en: {int(5 - ((player.super_timer - time_now)*-1))}', True, (255,255,255))


    for e in enemies_list:
        e.show()
    
    for a in asteroid_list:
        a.show()

    player.show()
    for b in bullet_list:
        b.show()
    mwin.blit(lifes_stats, (0, 0))
    mwin.blit(point_text, (0, 15))
    mwin.blit(bullets_left, (0,30))
    mwin.blit(ultimate_text, (0, 45))
    if doshow_explosion:
        player.explosion.show()
    if player.is_recharging:
        recharging_text = instructions.render('Recargando', True, (255,255,255))
        mwin.blit(recharging_text, (300, 450))
    mouse_target.show()
    display.update()


player = Player(325, 450, 50, 50, 5, image='rocket.png')
player.initialise()
mouse.set_visible(False)

#explosion = entity(100, 100, 150, 150, image='explosion.png')
#explosion.initialise()
doshow_explosion = False
instructions = font.SysFont('Arial', 25)
game_condition = True
enemy_number = 0
asteroid_number = 0
timer = time.Clock()
last_enemy_kill = 0
last_enemy_generation = 0
player_lifes = font.SysFont('Arial', 25)
points_counter = 0
point_stats = font.SysFont('Arial', 25)
title = font.SysFont('Arial', 25)
mwin.blit(background, (0,0))
text1 = instructions.render('Mueve el ratón fuera de esta pantalla si no va a ser usado para moverse', True, (255, 255, 255))
mwin.blit(text1, (0, 0))
display.update()
while game_condition:
    timer.tick(60)

    refresh_screen()

    for e in event.get():
        if e.type == QUIT:
            game_condition = False
        if e.type == MOUSEBUTTONDOWN:
            player.super_ability()
        if e.type == MOUSEMOTION:
            pos = mouse.get_pos()
            mouse_target = entity(pos[0] - 25, pos[1] - 25, 50, 50, image = 'red_target_1-removebg-preview.png')
            mouse_target.initialise()
            mouse_target.show()
        
    keys_down = key.get_pressed()

    if keys_down[K_ESCAPE]:
        game_condition = False
    if keys_down[K_a] and player.xpos > 0:
        player.left_step()
    if keys_down[K_d] and player.xpos < 650:
        player.right_step()
    if keys_down[K_SPACE]:
        player.shoot()
    
    player.check_recharging()

    for b in bullet_list:
        if b.ypos > 0:
            b.up_step()
        else:
            bullet_list.remove(b)
            del b
    
    for a in asteroid_list:
        if a.ypos < 450:
            a.down_step()
        else:
            asteroid_list.remove(a)
            del a
    
    for e in enemies_list:
        do_bucle = True
        e.down_step()
        for b in bullet_list:
            if do_bucle and e.collide_area.colliderect(b.collide_area):
                bullet_list.remove(b)
                del b
                enemies_list.remove(e)
                del e
                points_counter += 5
                do_bucle = False
    for a in asteroid_list:
        del_condition = False
        current_asteroid = a
        if player.collide_area.colliderect(a.collide_area):
            del_condition = True
            asteroid_list.remove(a)
            player.lifes -= 1
            points_counter -= 20
            pass
        for b in bullet_list:
            if b.collide_area.colliderect(current_asteroid.collide_area):
                bullet_list.remove(b)
                del b

        if a.ypos >= 450:
            asteroid_list.remove(a)
        if del_condition:
            del a
            
    
    for e in enemies_list:
        del_condition = False
        if player.collide_area.colliderect(e.collide_area):
            del_condition = True
            enemies_list.remove(e)
            player.lifes -= 1
            pass
        if e.ypos >= 450:
            enemies_list.remove(e)
            player.lifes -= 1
        if del_condition:
            del e
            points_counter -= 20
    
    y_mouse_pos = 0
    actual_time = time_screenshot()
    if actual_time - last_enemy_kill > 1.75 and actual_time - last_enemy_generation > 1.25 and len(enemies_list) <= 5:
        enemy_number += 1
        last_enemy_generation = actual_time
        initial_pos = randint(0, 650)
        enemy_name = 'enemy_' + str(len(enemies_list) + 1)
        velocity = randint(1,3)
        exec(f'{enemy_name} = cinetic_entity({initial_pos}, 0, 50, 50, {velocity}, image="ufo.png")')
        exec(f'enemies_list.append({enemy_name})')
        exec(f'{enemy_name}.initialise()')
    asteroid_chance = randint(0,100)
    if asteroid_chance == 1:
        asteroid_number += 1
        initial_pos = randint(0, 650)
        asteroid_name = 'asteroid_' + str(len(asteroid_list) + 1)
        velocity = randint(1,3)
        exec(f'{asteroid_name} = cinetic_entity({initial_pos}, 0, 50, 50, {velocity}, image="asteroide_1-removebg-preview.png")')
        exec(f'asteroid_list.append({asteroid_name})')
        exec(f'{asteroid_name}.initialise()')
    
    if player.lifes <= 0:
        text = title.render('Game over', True, (255,0,0))
        mwin.blit(text, (250, 250))
        display.update()
        game_condition = False
        sleep(3)
    
    time_now = time_screenshot()
    if (time_now - player.super_timer) <= 1.5:
        doshow_explosion = True
    else:
        doshow_explosion = False
