import math
from dataclasses import dataclass
from designer import *
from random import randint
import random


center_width = get_width() / 2
SLICER_SPEED = 50
meat_y_acceleration = 2
paths = ["/images/apple.png", "/images/orange.png", "/images/pear.png", "/images/blueberry.png"]

@dataclass
class Meat:
    rect: DesignerObject
    weight: int
    display_weight: DesignerObject
    y_velocity: int


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
    meats: list[Meat]
    end_text: DesignerObject
    total_fruit: int


def create_world()-> World:
    """ Create the world """
    set_window_color('lightskyblue')
    return World(create_slicer(), 0, image("/images/scale.png", center_width, get_height() - 50), 5,
                 text("red", "5", 100, 50, 50, font_name="Josefin Sans"), 0,
                 text("black", "0", 30, center_width, get_height() - 40, font_name="Josefin Sans"), [], [],
                 text("black", "", 100, center_width, get_height() / 2), 0)


def create_slicer()-> DesignerObject:
    """"""
    return rectangle("black", 10, 80, center_width, 40)


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
    return Fruit(image(random.choice(paths), x, int(math.sin(x / 20))),
                 x == 0, randint(16, 75), randint(30, 85), get_height() / 2 + random.choice(midpoints))


def create_meat(world: World, x: int, y: int)-> Meat:
    weight = randint(20, 40) + int(world.total_fruit / 5) * 5
    return Meat(circle("green", 15, x, y),
                weight, text("white", str(weight), 25, x, y, font_name="Swis721 BlkEx BT"), 15)


def update_meat(world: World):
    for meat in world.meats:
        meat.y_velocity += meat_y_acceleration * .2
        meat.rect.y += meat.y_velocity
        meat.display_weight.y = meat.rect.y
        if colliding(meat.rect, world.scale):
            world.weight += meat.weight
            world.meats.remove(meat)
            destroy(meat.rect)
            destroy(meat.display_weight)


def update_fruit(world: World):
    fruit_speed = 8 + int(world.total_fruit / 5)
    for fruit in world.fruits:
        if fruit.moving_right:
            fruit.rect.x += fruit_speed
        else:
            fruit.rect.x -= fruit_speed
        fruit.rect.y = fruit.midpoint + int(math.sin(fruit.rect.x / fruit.period) * fruit.amplitude)
        if fruit.rect.x < 0 or fruit.rect.x > get_width():
            world.fruits.remove(fruit)
            world.lives -= 1
            destroy(fruit.rect)
    collide_slicer_fruit(world)


def collide_slicer_fruit(world: World):
    for fruit in world.fruits:
        if colliding(fruit.rect, world.slicer):
            world.meats.append(create_meat(world, fruit.rect.x, fruit.rect.y))
            world.fruits.remove(fruit)
            destroy(fruit.rect)


def spawn_fruit(world: World):
    """ Spawn fruit at random times """
    fruit_limit = len(world.fruits) < 4
    chance_of_fruit = randint(0, 40) == 1
    if fruit_limit and chance_of_fruit:
        world.total_fruit += 1
        world.fruits.append(create_fruit())


def update_lives(world: World):
    destroy(world.life_counter)
    world.life_counter = text("red", str(world.lives), 100, 50, 50, font_name="Josefin Sans")


def zero_lives(world: World):
    return world.lives <= 0


def display_end_text(world: World):
    """ Show the game over message """
    world.end_text.text = "Final Weight: " + str(world.weight) + "!"


when("updating", update_weight)
when("starting", create_world)
when("typing", start_slicer_movement)
when("updating", update_slicer)
when("updating", stop_slider)
when("updating", spawn_fruit)
when("updating", update_meat)
when("updating", update_fruit)
when("updating", update_lives)
when(zero_lives, display_end_text, pause)
start()