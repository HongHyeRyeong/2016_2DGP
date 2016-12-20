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
stage, item, end = None, None, None
plants, attacks = None, None
flowers, suns = None, None
walnuts = None
bombs = None
snows, snow_attacks = None, None
zombies = None

Not_Select, Plant_Select, Flower_Select,Walnut_Select, Bomb_Select, Snow_Select, Shovel_Select = 0, 1, 2, 3, 4, 5, 6

mouse_x, mouse_y = 0, 0
sun_point = 500
select_plant = Not_Select
space = [[0 for col in range(5)] for row in range(8)]

def enter():
    global stage, item, end
    global plants, flowers, walnuts, bombs, snows, zombies
    global attacks, snow_attacks, suns
    stage = Stage()
    item = Item()
    end = Game_End()
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
    global stage, item, end
    global plants, flowers, walnuts, bombs, snows, zombies
    global attacks, snow_attacks, suns
    change_stage()
    del(stage)
    del(item)
    del(end)
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
    global space, item, select_plant
    global mouse_x, mouse_y
    item.plant()
    space_x, space_y = mouse_x - 200, mouse_y - 100
    space[int(space_x / 100)][int(space_y / 100)] = 1
    select_plant = Not_Select

def select_item():
    global stage
    global mouse_x, select_plant
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
    elif 500 < mouse_x < 575:
        if 0 < select_plant:
            select_plant = Not_Select
        else:
            select_plant = Shovel_Select

def select_sun():
    global item, suns, sun_point
    item.coin()
    sun_count = len(suns)
    if not sun_count == 0:
        sun_point += sun_count * 10
        suns.clear()

def select_shovel():
    global plants, flowers, walnuts, bombs, snows
    global mouse_x, mouse_y
    plants_x = int(mouse_x / 100) * 100 + 55
    plants_y = int((600-mouse_y) / 100) * 100 + 50

    for plant in plants:
        if plant.x == plants_x and plant.y == plants_y:
            remove_plant(plant.x, plant.y)
            plants.remove(plant)
            return
    for flower in flowers:
        if flower.x == plants_x and flower.y == plants_y:
            remove_plant(flower.x, flower.y)
            flowers.remove(flower)
            return
    for walnut in walnuts:
        if walnut.x == plants_x and walnut.y == plants_y:
            remove_plant(walnut.x, walnut.y)
            walnuts.remove(walnut)
            return
    for bomb in bombs:
        if bomb.x == plants_x and bomb.y == plants_y:
            remove_plant(bomb.x, bomb.y)
            bombs.remove(bomb)
            return
    for snow in snows:
        if snow.x == plants_x and snow.y == plants_y:
            remove_plant(snow.x, snow.y)
            snows.remove(snow)

def select_object():
    global plants, flowers, walnuts, bombs, snows
    global mouse_x, mouse_y
    global select_plant, space, sun_point
    global space
    if 210 < mouse_x < 1000 and 110 < mouse_y < 600: # 땅
        space_x, space_y = mouse_x - 200, mouse_y - 100
        if space[int(space_x / 100)][int(space_y / 100)] == 0:
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
        else:
            if select_plant == Shovel_Select:
                select_shovel()
    elif 100 < mouse_x < 580 and 0 < mouse_y < 80:
        select_item()
    elif 25 < mouse_x < 75 and 20 < mouse_y < 65:
        select_sun()

def creat_zombie():
    global stage, zombies
    new_zombie = Zombie()
    zombies.append(new_zombie)
    stage.zombie_time = 0

def creat():
    global stage, plants, zombies, attacks, suns, flowers, snows, snow_attacks
    if stage.bar_time < 50:
        if 3 == stage.zombie_time:
            creat_zombie()
    elif 150 < stage.bar_time:
        if 0.5 == stage.zombie_time:
            creat_zombie()
    else:
        if 1 == stage.zombie_time:
            creat_zombie()
    for plant in plants:
        if 2 == plant.attack_time:
            new_attack = Attack(plant.x, plant.y)
            attacks.append(new_attack)
            plant.attack_time = 0
    for snow in snows:
        if 2 == snow.attack_time:
            new_attack = Snow_Attack(snow.x, snow.y)
            snow_attacks.append(new_attack)
            snow.attack_time = 0
    for flower in flowers:
        if 3 == flower.sun_time:
            new_sun = Sun()
            suns.append(new_sun)
            flower.sun_time = 0

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

def remove_plant(x, y):
    global space
    space_col, space_row = (x - 55) / 100 - 2, 4 - (y - 50) / 100
    space[int(space_col)][int(space_row)] = 0

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
                remove_plant(plant.x, plant.y)
                plants.remove(plant)
                zombie.state = zombie.ATTACK
        for flower in flowers:
            if collide(zombie, flower):
                remove_plant(flower.x, flower.y)
                flowers.remove(flower)
                zombie.state = zombie.ATTACK
        for snow in snows:
            if collide(zombie, snow):
                remove_plant(snow.x, snow.y)
                snows.remove(snow)
                zombie.state = zombie.ATTACK
        for walnut in walnuts:
            if collide(zombie, walnut):
                if zombie.state == zombie.WALK:
                    if walnut.life > 0:
                        walnut.life -= 1
                    else:
                        remove_plant(walnut.x, walnut.y)
                        walnuts.remove(walnut)
                zombie.state = zombie.DIE
        for bomb in bombs:
            if collide(zombie, bomb):
                remove_plant(bomb.x, bomb.y)
                bombs.remove(bomb)
                zombie.state = zombie.DIE
        for attack in attacks:
            if collide(attack, zombie):
                zombie.attack()
                attacks.remove(attack)
        for snow_attack in snow_attacks:
            if collide(snow_attack, zombie):
                zombie.speed += 1
                snow_attacks.remove(snow_attack)

def change_stage():
    global stage, end
    global plants, flowers, walnuts, zombies, attacks, suns, bombs, snows, snow_attacks
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
    end.play()
    mouse_x, mouse_y = 0, 0
    select_plant = Not_Select
    sun_point = 500
    space = [[0 for col in range(5)] for row in range(8)]

def game_end():
    global end, stage, zombies
    if 270 == stage.bar_time:
        end.plant()
    for zombie in zombies:
        if zombie.x < 0:
            end.zombie()

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
    global stage, item, end
    global plants, flowers, walnuts, bombs, snows, zombies
    global attacks, snow_attacks, suns

    if end.state == 'play':
        stage.update()
        item.update(frame_time)
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
        game_end()
        creat()
        remove()
        collide_check()

def draw(frame_time):
    global stage, item, end
    global plants, flowers, walnuts, bombs, snows, zombies
    global attacks, snow_attacks, suns
    global select_plant, sun_point
    global mouse_x, mouse_y
    clear_canvas()
    if end.state == 'play':
        stage.draw(sun_point)
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
        item.draw(select_plant, mouse_x, 600 - mouse_y)
        for attack in attacks:
            attack.draw()
        for snow_attack in snow_attacks:
            snow_attack.draw()
        for sun in suns:
            sun.draw()
    else:
        end.draw()
    update_canvas()