import random
import json
import os
import time
from pico2d import *

import game_framework
import title_state
from plants import *
from zombies import *
from stage import*

name = "MainState"

# 객체
stage = None
plants, attacks = None, None
flowers, suns = None, None
walnuts = None
bombs = None
snows, snow_attacks = None, None
zombies = None

Not_Select, Plant_Select, Flower_Select,Walnut_Select, Bomb_Select, Snow_Select, Remove_Select = 0, 1, 2, 3, 4, 5, 6

mouse_x, mouse_y = 0, 0
sun_point = 1000
select_plant = Not_Select
space = [[0 for col in range(20)] for row in range(20)]

def enter():
    global stage, plants, flowers, walnuts, bombs, snows, zombies
    global attacks, snow_attacks, suns
    stage = Stage()
    plants = []
    attacks = []
    flowers = []
    suns = []
    walnuts = []
    bombs = []
    snows = []
    snow_attacks = []
    zombies = []

def exit():
    global stage, plants, flowers, walnuts, bombs, snows, zombies
    global attacks, snow_attacks, suns
    change_stage()
    del(stage)
    del(plants)
    del(attacks)
    del(flowers)
    del(suns)
    del(walnuts)
    del(bombs)
    del(snows)
    del(snow_attacks)
    del(zombies)

def pause():
    pass

def resume():
    pass

def select_space():
    global space, select_plant
    global mouse_x, mouse_y
    space[int(mouse_x / 100)][int(mouse_y / 100)] = 1
    select_plant = Not_Select

def select_item():
    global stage
    global mouse_x, mouse_y, select_plant
    if 100 < mouse_x < 155:
        select_plant = Plant_Select
    elif 160 < mouse_x < 210:
        select_plant = Flower_Select
    elif 215 < mouse_x < 260:
        select_plant = Walnut_Select
    elif 270 < mouse_x < 315:
        if stage.state in ('stage2', 'stage3'):
            select_plant = Bomb_Select
    elif 320 < mouse_x < 365:
        if stage.state == 'stage3':
            select_plant = Snow_Select
    elif 500 < mouse_x < 575:  # 삽
        select_plant = Not_Select

def select_sun():
    global suns, sun_point
    sun_count = len(suns)
    if not sun_count == 0:
        sun_point += sun_count * 15
        suns.clear()

def select_object():
    global plants, flowers, walnuts, bombs, snows
    global mouse_x, mouse_y
    global select_plant, space, sun_point
    if 260 < mouse_x < 980 and 90 < mouse_y < 600: # 땅
        if space[int(mouse_x / 100)][int(mouse_y / 100)] == 0:
            if select_plant == Plant_Select and sun_point - 100 >= 0:
                sun_point -= 100
                new_plant = Plant(mouse_x, 599 - mouse_y)
                plants.append(new_plant)
                select_space()
            elif select_plant == Flower_Select and sun_point - 50 >= 0:
                sun_point -= 50
                new_flower = Flower(mouse_x, 599 - mouse_y)
                flowers.append(new_flower)
                select_space()
            elif select_plant == Walnut_Select and sun_point - 50 >= 0:
                sun_point -= 50
                new_walnut = Walnut(mouse_x, 599 - mouse_y)
                walnuts.append(new_walnut)
                select_space()
            elif select_plant == Bomb_Select and sun_point - 25 >= 0:
                sun_point -= 25
                new_bomb = Bomb(mouse_x, 599 - mouse_y)
                bombs.append(new_bomb)
                select_space()
            elif select_plant == Snow_Select and sun_point - 175 >= 0:
                sun_point -= 175
                new_snow = Snow_Plant(mouse_x, 599 - mouse_y)
                snows.append(new_snow)
                select_space()
    elif 100 < mouse_x < 580 and 0 < mouse_y < 80:
        select_item()
    elif 25 < mouse_x < 75 and 20 < mouse_y < 65:
        select_sun()

def creat():
    global stage, plants, zombies, attacks, suns, flowers, snows, snow_attacks

    if stage.zombie_cnt == stage.random_cnt:
        new_zombie = Zombie()
        zombies.append(new_zombie)
        stage.zombie_set_count()
    for plant in plants:
        if plant.attack_cnt == 200:
            new_attack = Attack(plant.x, plant.y)
            attacks.append(new_attack)
            plant.attack_cnt = 0
    for snow in snows:
        if snow.attack_cnt == 200:
            new_attack = Snow_Attack(snow.x, snow.y)
            snow_attacks.append(new_attack)
            snow.attack_cnt = 0
    for flower in flowers:
        if flower.sun_cnt == 300:
            new_sun = Sun()
            suns.append(new_sun)
            flower.sun_cnt = 0

def remove():
    global attacks, zombies, snow_attacks
    for zombie in zombies:
        if zombie.x < 0:
            zombies.remove(zombie)
        if zombie.state == zombie.END:
            zombies.remove(zombie)
    for attack in attacks:
        if attack.x > 1400:
            attacks.remove(attack)
    for snow_attack in snow_attacks:
        if snow_attack.x > 1400:
            snow_attacks.remove(snow_attack)

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
    global plants, flowers, walnuts, zombies, attacks, bombs, snows, snow_attacks

    for zombie in zombies:
        for plant in plants:
            if collide(zombie, plant):
                plants.remove(plant)
                zombie.state = zombie.ATTACK
        for flower in flowers:
            if collide(zombie, flower):
                flowers.remove(flower)
                zombie.state = zombie.ATTACK
        for snow in snows:
            if collide(zombie, snow):
                snows.remove(snow)
                zombie.state = zombie.ATTACK
        for walnut in walnuts:
            if collide(zombie, walnut):
                if zombie.state == zombie.WALK:
                    if walnut.life > 0:
                        walnut.life -= 1
                    else:
                        walnuts.remove(walnut)
                zombie.state = zombie.DIE
        for bomb in bombs:
            if collide(zombie, bomb):
                bombs.remove(bomb)
                zombie.state = zombie.DIE
        for attack in attacks:
            if collide(attack, zombie):
                zombie.state = zombie.DIE
                attacks.remove(attack)
        for snow_attack in snow_attacks:
            if collide(snow_attack, zombie):
                zombie.slow += 1
                snow_attacks.remove(snow_attack)

def change_stage():
    global stage, plants, flowers, walnuts, zombies, attacks, suns, bombs, snows, snow_attacks
    global mouse_x, mouse_y
    global select_plant, space
    global sun_point
    plants.clear()
    attacks.clear()
    flowers.clear()
    suns.clear()
    walnuts.clear()
    bombs.clear()
    snows.clear()
    snow_attacks.clear()
    zombies.clear()
    stage.cnt_init()
    mouse_x, mouse_y = 0, 0
    select_plant = Not_Select
    sun_point = 1000
    for i in range(20):
        for j in range(20):
            space[i][j] = 0

def handle_events(frame_time):
    global stage, mouse_x, mouse_y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            stage.state = 'stage1'
            change_stage()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            stage.state = 'stage2'
            change_stage()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            stage.state = 'stage3'
            change_stage()
        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, event.y
        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            select_object()

def update(frame_time):
    global stage, plants, flowers, walnuts, bombs, snows, zombies
    global attacks, snow_attacks, suns

    stage.update()
    for plant in plants:
        plant.update(frame_time)
    for attack in attacks:
        attack.update(frame_time)
    for flower in flowers:
        flower.update(frame_time)
    for snow in snows:
        snow.update(frame_time)
    for snow_attack in snow_attacks:
        snow_attack.update(frame_time)
    for sun in suns:
        sun.update(frame_time)
    for walnut in walnuts:
        walnut.update(frame_time)
    for bomb in bombs:
        bomb.update(frame_time)
    for zombie in zombies:
        zombie.update(frame_time)
    creat()
    remove()
    collide_check()

def draw(frame_time):
    global stage, plants, flowers, walnuts, bombs, snows, zombies
    global attacks, snow_attacks, suns
    global select_plant, sun_point
    clear_canvas()
    stage.draw(select_plant, sun_point)
    for plant in plants:
        plant.draw()
    for flower in flowers:
        flower.draw()
    for walnut in walnuts:
        walnut.draw()
    for bomb in bombs:
        bomb.draw()
    for snow in snows:
        snow.draw()
    for zombie in zombies:
        zombie.draw()
    for attack in attacks:
        attack.draw()
    for snow_attack in snow_attacks:
        snow_attack.draw()
    for sun in suns:
        sun.draw()
    update_canvas()