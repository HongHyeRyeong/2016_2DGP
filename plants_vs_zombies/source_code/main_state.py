import random
import json
import os
import time

from pico2d import *

import game_framework
import title_state
from plants import *
from zombies import *

name = "MainState"

#객체
back = None
plants = None
flowers = None
walnuts = None
bombs = None
zombies = None
attacks = None

mousex, mousey = 0, 0
selete_plant = 0
space = [[0 for col in range(20)] for row in range(20)]
zombie_cnt ,random_cnt = 0, 10

class Background:
    def __init__(self):
        self.image = load_image('background.png')
        self.selete = load_image('selete_plant.png')
        self.gamestart = True

    def draw(self):
        self.image.draw(700, 300)
        self.selete.clip_draw((selete_plant - 1) * 100, 0, 100, 100, 1350, 545)

def enter():
    global back, plants, flowers, walnuts, bombs, zombies, attacks
    back = Background()
    plants = []
    flowers = []
    walnuts = []
    bombs = []
    zombies = []
    attacks = []

def exit():
    global back, plants, flowers, walnuts, bombs, zombies, attacks
    global mousex, mousey
    global selete_plant, space
    global zombie_cnt, random_cnt
    del(back)
    del(plants)
    del(flowers)
    del(walnuts)
    del(bombs)
    del(zombies)
    del(attacks)
    mousex, mousey = 0, 0
    selete_plant = 0
    zombie_cnt, random_cnt = 0, 10
    for i in range(20):
        for j in range(20):
            space[i][j] = 0

def pause():
    pass

def resume():
    pass

def set_object():
    global plants, flowers, walnuts, bombs
    global mousex, mousey
    global selete_plant, space

    if 260 < mousex < 980 and 90 < mousey < 600: # 땅
        if space[int(mousex / 100)][int(mousey / 100)] == 0:
            if selete_plant == 1:
                new_plant = Plant()
                new_plant.creat(mousex, 599 - mousey)
                plants.append(new_plant)

                space[int(mousex / 100)][int(mousey / 100)] = 1
                selete_plant = 0

            elif selete_plant == 2:
                new_flower = Flower()
                new_flower.creat(mousex, 599 - mousey)
                flowers.append(new_flower)

                space[int(mousex / 100)][int(mousey / 100)] = 1
                selete_plant = 0

            elif selete_plant == 3:
                new_walnut = Walnut()
                new_walnut.creat(mousex, 599 - mousey)
                walnuts.append(new_walnut)

                space[int(mousex / 100)][int(mousey / 100)] = 1
                selete_plant = 0

            elif selete_plant == 4:
                new_bomb = Bomb()
                new_bomb.creat(mousex, 599 - mousey)
                bombs.append(new_bomb)

                space[int(mousex / 100)][int(mousey / 100)] = 1
                selete_plant = 0

    elif 100 < mousex < 580 and 0 < mousey < 80: # 식물
        if 100 < mousex < 160:
            selete_plant = 1
        elif 160 < mousex < 220:
            selete_plant = 2
        elif 220 < mousex < 280:
            selete_plant = 3
        elif 280 < mousex < 340:
            selete_plant = 4
        elif 500 < mousex < 580: # 삽
            selete_plant = 5

def creat():
    global plants, zombies
    global zombie_cnt, random_cnt

    zombie_cnt += 1
    if zombie_cnt == random_cnt:
        new_zombie = Zombie()
        zombies.append(new_zombie)
        random_cnt = random.randint(10, 20)
        zombie_cnt = 0

    for plant in plants:
        if plant.attackcnt == 20:
            new_attack = Attack()
            new_attack.creat(plant.x, plant.y)
            attacks.append(new_attack)
            plant.attackcnt = 0

def handle_events(frame_time):
    global mousex, mousey

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            back.gamestart = False
            game_framework.change_state(title_state)
        elif event.type == SDL_MOUSEMOTION:
            mousex, mousey = event.x, event.y
        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            set_object()

def update(frame_time):
    global plants, flowers, walnuts, bombs, zombies, attacks

    # 새로운 좀비, 식물
    creat()

    # 좀비 범위 넘어가면 삭제
    for zombie in zombies:
        if zombie.x < 0:
            zombies.remove(zombie)

    # 식물 공격 범위 넘어가면 삭제
    for attack in attacks:
        if attack.x > 1400:
            attacks.remove(attack)

    if back.gamestart == True:
        for plant in plants:
            plant.update(frame_time)
        for attack in attacks:
            attack.update(frame_time)
        for flower in flowers:
            flower.update(frame_time)
        for walnut in walnuts:
            walnut.update(frame_time)
        for bomb in bombs:
            bomb.update(frame_time)
        for zombie in zombies:
            zombie.update(frame_time)

def draw(frame_time):
    global plants, flowers, walnuts, bombs, zombies, attacks
    clear_canvas()
    if back.gamestart == True:
        back.draw()
        for plant in plants:
            plant.draw(frame_time)
        for flower in flowers:
            flower.draw(frame_time)
        for walnut in walnuts:
            walnut.draw(frame_time)
        for bomb in bombs:
            bomb.draw(frame_time)
        for zombie in zombies:
            zombie.draw(frame_time)
        for attack in attacks:
            attack.draw(frame_time)
    update_canvas()
    delay(0.1)