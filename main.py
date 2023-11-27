import math
from dataclasses import dataclass
from designer import *
from random import randint
import random


center_width = get_width() / 2
SLICER_SPEED = 50
paths = ["/images/apple.png", "/images/orange.png", "/images/pear.png", "/images/blueberry.png"]


@dataclass
class Meat:
    """
    The Meat class is used to define the objects that fall from fruits after they are "sliced".
    rect(DesignerObject): This is the circular object that provides the color and boundaries of the Meat object.
    weight(int): This is the weight of the Meat, which effects the weight shown by display_weight and the scale.
    display_weight(DesignerObject): This is the text that shows what the weight of the Meat is.
    y_velocity(int): This is the current vertical velocity of the Meat.
    """
    rect: DesignerObject
    weight: int
    display_weight: DesignerObject
    y_velocity: int


@dataclass
class Fruit:
    """
    The Fruit class is used to define the objects that spawn from the side and can be "sliced" by the slicer.
    rect(DesignerObject): This is the circular object that provides the image and boundaries of the Fruit object.
    moving_right(bool): This is the attribute that defines what direction the Fruit should move.
    period(int): This is the period of the movement wave of the Fruit.
    amplitude(int): This is the amplitude of the movement wave of the Fruit.
    midpoint(int): This is the midpoint of the movement wave of the Fruit.
    """
    rect: DesignerObject
    moving_right: bool
    period: int
    amplitude: int
    midpoint: int


@dataclass
class World:
    """
    The World class is used to define the world that holds all the other objects in used in the game.
    slicer(DesignerObject): This is the rectangular object that can be controlled with the space bar.
    slicer_speed(int): This is the attribute that defines what speed and direction the slicer should move.
    scale(DesignerObject): This is the scale that is shown with an image, and interacts with the Meat.
    lives(int): This is the amount of lives the player has.
    life_counter(DesignerObject): This is the text displaying lives.
    weight(int): This is the weight(points) the player has gained.
    weight_counter(DesignerObject): This is the text displaying the weight.
    fruits(list[Fruit]): This is the list containing the fruits on screen.
    meats(list[Meat]): This is the list containing the meats on screen.
    end_text(DesignerObject): This is the text that will not be shown until the end of the game.
    total_fruit(int): This is the amount of fruit that have been spawned in total.
    """
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


def create_world() -> World:
    """
    Creates the world of the game
    :return: World
    """
    set_window_color('lightskyblue')
    return World(create_slicer(), 0, image("/images/scale.png", center_width, get_height() - 50), 5,
                 text("red", "5", 100, 50, 50, font_name="Josefin Sans"), 0,
                 text("black", "0", 30, center_width, get_height() - 40, font_name="Josefin Sans"), [], [],
                 text("black", "", 100, center_width, get_height() / 2), 0)


def create_slicer() -> DesignerObject:
    """
    Creates the slicer
    :return: DesignerObject
    """
    return rectangle("black", 10, 80, center_width, 40)


def update_weight(world: World):
    """
    Updates the weight displayed on the scale
    :param world: The world of the game
    :return: Nothing
    """
    world.weight_counter.text = "Weight: " + str(world.weight)


def start_slicer_movement(world: World, key: str):
    """
    Starts the slicer movement if the slicer is at either endpoint
    :param world: The world of the game
    :param key: The key pressed by the user
    :return: Nothing
    """
    if key == "space":
        if world.slicer.y == 40:
            world.slicer_speed = SLICER_SPEED
        elif world.slicer.y == get_height() - 140:
            world.slicer_speed = -SLICER_SPEED


def update_slicer(world: World):
    """
    Updates the slicer location
    :param world: The world of the game
    :return: Nothing
    """
    world.slicer.y += world.slicer_speed


def stop_slicer(world: World):
    """
    Stops the slider from moving once it hits an endpoint
    :param world: The world of the game
    :return: Nothing
    """
    if world.slicer.y <= 40:
        world.slicer.y = 40
        world.slicer_speed = 0
    elif world.slicer.y >= get_height() - 140:
        world.slicer.y = get_height() - 140
        world.slicer_speed = 0


def create_fruit() -> Fruit:
    """
    Creates a fruit using random numbers within a range
    :return: Nothing
    """
    x = randint(0, 1) * get_width()
    midpoint = randint(0, 80)
    midpoints = [-midpoint, midpoint]
    return Fruit(image(random.choice(paths), x, int(math.sin(x / 20))),
                 x == 0, randint(16, 75), randint(30, 85), get_height() / 2 + random.choice(midpoints))


def create_meat(world: World, x: int, y: int) -> Meat:
    """
    Creates meat and gives it a randomly generated weight within a certain range
    :param world: The world of the game
    :param x: The x location of the parent fruit
    :param y: The y location of the parent fruit
    :return: The Meat created
    """
    weight = randint(20, 40) + int(world.total_fruit / 5) * 5
    return Meat(circle("green", 15, x, y),
                weight, text("white", str(weight), 25, x, y, font_name="Swis721 BlkEx BT"), 15)


def update_meat(world: World):
    """
    Updates the location of the meats on screen, and removes them from the world and adds it weight to the world
    when they collide with the scale
    :param world: The world of the game
    :return: Nothing
    """
    for meat in world.meats:
        meat.y_velocity += 2 * .2
        meat.rect.y += meat.y_velocity
        meat.display_weight.y = meat.rect.y
        if colliding(meat.rect, world.scale):
            world.weight += meat.weight
            world.meats.remove(meat)
            destroy(meat.rect)
            destroy(meat.display_weight)


def update_fruit(world: World):
    """
    Updates the fruits location and removes them from the world once they move offscreen
    :param world: The world of the game
    :return: Nothing
    """
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
    """
    Removes fruits and adds a meat when the slicer collides with a fruit
    :param world: The world of the game
    :return: Nothing
    """
    for fruit in world.fruits:
        if colliding(fruit.rect, world.slicer):
            world.meats.append(create_meat(world, fruit.rect.x, fruit.rect.y))
            world.fruits.remove(fruit)
            destroy(fruit.rect)


def spawn_fruit(world: World):
    """
    Spawns fruits at random times when there are less than 4 on screen
    :param world: The world of the game
    :return: Nothing
    """
    fruit_limit = len(world.fruits) < 4
    chance_of_fruit = randint(0, 40) == 1
    if fruit_limit and chance_of_fruit:
        world.total_fruit += 1
        world.fruits.append(create_fruit())


def update_lives(world: World):
    """
    Updates the life counter with the amount of lives the player has
    :param world: The world of the game
    :return: Nothing
    """
    world.life_counter.text = str(world.lives)


def zero_lives(world: World) -> bool:
    """
    Determines if the player has 0 lives or fewer
    :param world: The world of the game
    :return: bool
    """
    return world.lives <= 0


def display_end_text(world: World):
    """
    Displays the text when the player loses
    :param world: The world of the game
    :return: Nothing
    """
    world.end_text.text = "Final Weight: " + str(world.weight) + "!"

# The functions that control the interaction and ecosystem of the game


when("updating", update_weight)
when("starting", create_world)
when("typing", start_slicer_movement)
when("updating", update_slicer)
when("updating", stop_slicer)
when("updating", spawn_fruit)
when("updating", update_meat)
when("updating", update_fruit)
when("updating", update_lives)
when(zero_lives, display_end_text, pause)
start()
