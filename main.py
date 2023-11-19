import math
from dataclasses import dataclass
from designer import *
from random import randint
import random


center_width = get_width() / 2
SLICER_SPEED = 50


@dataclass
class Fruit:
    rect: DesignerObject
    moving_right: bool
    period: int
    amplitude: int
    midpoint: int


@dataclass
class World:
    slicer: DesignerObject
    slicer_speed: int
    scale: DesignerObject
    lives: int
    life_counter: DesignerObject
    weight: int
    weight_counter: DesignerObject
    fruits: list[Fruit]


def set_background():
    """ Set the background color"""
    set_window_color('lightblue')


def create_scale()-> DesignerObject:
    """ Move the copter horizontally"""
    return rectangle('gray', 600, 100, get_width() / 2, get_height() - 50)


def create_world()-> World:
    """ Create the world """
    set_background()
    return World(create_slicer(), 0, create_scale(), 3,
                 text("red", "3", 100, 50, 50, font_name="Josefin Sans"), 0,
                 text("black", "0", 50, get_width() / 2, get_height() - 50, font_name="Josefin Sans"), [])


def create_slicer()-> DesignerObject:
    """"""
    return rectangle("black", 10, 80, get_width() / 2, 40)


def update_weight(world):
    """ Update the score """
    world.weight_counter.text = "Weight: " + str(world.weight)


def start_slicer_movement(world: World, key: str):
    if key == "space":
        if world.slicer.y == 40:
            world.slicer_speed = SLICER_SPEED
        elif world.slicer.y == get_height() - 140:
            world.slicer_speed = -SLICER_SPEED


def update_slicer(world: World):
    world.slicer.y += world.slicer_speed


def stop_slider(world: World):
    if world.slicer.y <= 40:
        world.slicer.y = 40
        world.slicer_speed = 0
    elif world.slicer.y >= get_height() - 140:
        world.slicer.y = get_height() - 140
        world.slicer_speed = 0


def create_fruit()-> Fruit:
    x = randint(0, 1) * get_width()
    midpoint = randint(0, 80)
    midpoints = [-midpoint, midpoint]
    return Fruit(circle("green", 30, x, int(math.sin(x / 20))),
                 x == 0, randint(16, 20), randint(30, 85), get_height() / 2 + random.choice(midpoints))


def update_fruit(world: World):
    for fruit in world.fruits:
        if fruit.moving_right:
            fruit.rect.x += 8
        else:
            fruit.rect.x -= 8
        fruit.rect.y = fruit.midpoint + int(math.sin(fruit.rect.x / fruit.period) * fruit.amplitude)
        if fruit.rect.x < 0 or fruit.rect.x > get_width():
            world.fruits.remove(fruit)
            world.lives -= 1
            destroy(fruit.rect)
    collide_slicer_fruit(world)


def collide_slicer_fruit(world: World):
    for fruit in world.fruits:
        if colliding(fruit.rect, world.slicer):
            world.fruits.remove(fruit)
            destroy(fruit.rect)


def spawn_fruit(world: World):
    """ Spawn fruit at random times """
    fruit_limit = len(world.fruits) < 4
    chance_of_fruit = randint(0, 40) == 1
    if fruit_limit and chance_of_fruit:
        world.fruits.append(create_fruit())


def update_lives(world: World):
    destroy(world.life_counter)
    world.life_counter = text("red", str(world.lives), 100, 50, 50, font_name="Josefin Sans")


when("updating", update_weight)
when("starting", create_world)
when("typing", start_slicer_movement)
when("updating", update_slicer)
when("updating", stop_slider)
when("updating", spawn_fruit)
when("updating", update_fruit)
when("updating", update_lives)
start()