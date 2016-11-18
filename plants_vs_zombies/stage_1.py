import random
import json
import os
import time

from pico2d import *

import game_framework
import title_state
import stage_2
import stage_3
from plants import *
from zombies import *

name = "Stage_1"

#객체
back = None
font = None
plants = None
flowers = None
walnuts = None
zombies = None
attacks = None
suns = None

mousex, mousey = 0, 0
selete_plant = 0
space = [[0 for col in range(20)] for row in range(20)]
zombie_cnt ,random_cnt = 0, 10
sunpoint = 1000

class Background:
    def __init__(self):
        self.image = load_image('background.png')
        self.selete = load_image('selete_plant.png')
        self.gamestart = True

    def draw(self):
        self.image.draw(700, 300)
        self.selete.clip_draw((selete_plant - 1) * 100 + 10, 0, 100, 100, 1350, 545)

def enter():
    global back, font
    global plants, flowers, walnuts, zombies, attacks, suns
    back = Background()
    font = load_font('ConsolaMalgun.ttf', 17)
    plants = []
    flowers = []
    walnuts = []
    zombies = []
    attacks = []
    suns = []

def exit():
    global back, font
    global plants, flowers, walnuts, zombies, attacks, suns
    global mousex, mousey
    global selete_plant, space
    global zombie_cnt, random_cnt
    global sunpoint
    del(back)
    del(plants)
    del(flowers)
    del(walnuts)
    del(zombies)
    del(attacks)
    del(suns)
    mousex, mousey = 0, 0
    selete_plant = 1000
    zombie_cnt, random_cnt = 0, 10
    sunpoint = 0
    for i in range(20):
        for j in range(20):
            space[i][j] = 0

def pause():
    pass

def resume():
    pass

def selete_space():
    global mousex, mousey, selete_plant
    space[int(mousex / 100)][int(mousey / 100)] = 1
    selete_plant = 0

def set_object():
    global plants, flowers, walnuts, suns
    global mousex, mousey
    global selete_plant, space
    global sunpoint

    if 260 < mousex < 980 and 90 < mousey < 600: # 땅
        if space[int(mousex / 100)][int(mousey / 100)] == 0:
            if selete_plant == 1 and sunpoint - 100 >= 0:
                sunpoint -= 100
                new_plant = Plant()
                new_plant.creat(mousex, 599 - mousey)
                plants.append(new_plant)
                selete_space()

            elif selete_plant == 2 and sunpoint - 50 >= 0:
                sunpoint -= 50
                new_flower = Flower()
                new_flower.creat(mousex, 599 - mousey)
                flowers.append(new_flower)
                selete_space()

            elif selete_plant == 3 and sunpoint - 50 >= 0:
                sunpoint -= 50
                new_walnut = Walnut()
                new_walnut.creat(mousex, 599 - mousey)
                walnuts.append(new_walnut)
                selete_space()

    elif 100 < mousex < 580 and 0 < mousey < 80: # 식물
        if 100 < mousex < 155:
            selete_plant = 1
        elif 160 < mousex < 210:
            selete_plant = 2
        elif 215 < mousex < 260:
            selete_plant = 3
        elif 500 < mousex < 575: # 삽
            selete_plant = 0

    elif 25 < mousex < 75 and 20 < mousey < 65: # 해
        suncount = len(suns)
        if suncount != 0:
            sunpoint += suncount * 15
            suns.clear()


def creat():
    global plants, zombies, attacks, suns, flowers
    global zombie_cnt, random_cnt

    zombie_cnt += 1
    if zombie_cnt == random_cnt:
        new_zombie = Zombie()
        zombies.append(new_zombie)
        random_cnt = random.randint(150, 200)
        zombie_cnt = 0

    for plant in plants:
        if plant.attackcnt == 200:
            new_attack = Attack()
            new_attack.creat(plant.x, plant.y)
            attacks.append(new_attack)
            plant.attackcnt = 0

    for flower in flowers:
        if flower.suncnt == 300:
            new_sun = Sun()
            suns.append(new_sun)
            flower.suncnt = 0

def remove():
    global attacks, zombies
    for zombie in zombies:
        if zombie.x < 0:
            zombies.remove(zombie)
        if zombie.state == zombie.END:
            zombies.remove(zombie)

    for attack in attacks:
        if attack.x > 1400:
            attacks.remove(attack)

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False

    return True

def collide_check():
    global plants, flowers, walnuts, zombies, attacks

    for zombie in zombies:
        for plant in plants:
            if collide(zombie, plant):
                plants.remove(plant)
                zombie.state = zombie.ATTACK
        for flower in flowers:
            if collide(zombie, flower):
                flowers.remove(flower)
                zombie.state = zombie.ATTACK
        for walnut in walnuts:
            if collide(zombie, walnut):
                if zombie.state == zombie.WALK:
                    if walnut.life > 0:
                        walnut.life -= 1
                    else:
                        walnuts.remove(walnut)
                zombie.state = zombie.DIE
        for attack in attacks:
            if collide(attack, zombie):
                zombie.state = zombie.DIE
                attacks.remove(attack)

def handle_events(frame_time):
    global mousex, mousey

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            back.gamestart = False
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            back.gamestart = False
            game_framework.change_state(stage_2)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            back.gamestart = False
            game_framework.change_state(stage_3)
        elif event.type == SDL_MOUSEMOTION:
            mousex, mousey = event.x, event.y
        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            set_object()

def update(frame_time):
    global plants, flowers, walnuts, zombies, attacks, suns

    if back.gamestart == True:
        for plant in plants:
            plant.update(frame_time)
        for attack in attacks:
            attack.update(frame_time)
        for flower in flowers:
            flower.update(frame_time)
        for sun in suns:
            sun.update(frame_time)
        for walnut in walnuts:
            walnut.update(frame_time)
        for zombie in zombies:
            zombie.update(frame_time)

    creat()
    remove()
    collide_check() # 충돌체크

def draw(frame_time):
    global back, font
    global plants, flowers, walnuts, zombies, attacks, suns
    global sunpoint
    clear_canvas()
    if back.gamestart == True:
        back.draw()
        font.draw(20, 504, '%d' % sunpoint)
        for plant in plants:
            plant.draw(frame_time)
        for flower in flowers:
            flower.draw(frame_time)
        for walnut in walnuts:
            walnut.draw(frame_time)
        for zombie in zombies:
            zombie.draw(frame_time)
        for attack in attacks:
            attack.draw(frame_time)
        for sun in suns:
            sun.draw(frame_time)
    update_canvas()