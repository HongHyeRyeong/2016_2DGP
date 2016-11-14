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

def selete_space():
    global mousex, mousey, selete_plant
    space[int(mousex / 100)][int(mousey / 100)] = 1
    selete_plant = 0


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
                selete_space()

            elif selete_plant == 2:
                new_flower = Flower()
                new_flower.creat(mousex, 599 - mousey)
                flowers.append(new_flower)
                selete_space()

            elif selete_plant == 3:
                new_walnut = Walnut()
                new_walnut.creat(mousex, 599 - mousey)
                walnuts.append(new_walnut)
                selete_space()

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
    global plants, zombies, attacks
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

    # 새로운 좀비, 식물 공격
    creat()

    # 범위 넘어가는 좀비, 식물 공격 삭제
    remove()

    # 충돌체크
    for zombie in zombies:
        for plant in plants:
            if collide(zombie, plant):
                plants.remove(plant)
                zombie.attack()
        for flower in flowers:
            if collide(zombie, flower):
                flowers.remove(flower)
                zombie.attack()
        for walnut in walnuts:
            if collide(zombie, walnut):
                walnuts.remove(walnut)
                zombie.attack()
        for bomb in bombs:
            if collide(zombie, bomb):
                bombs.remove(bomb)
                zombie.attack()
        for attack in attacks:
            if collide(attack, zombie):
                zombie.state = zombie.DIE
                attacks.remove(attack)


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