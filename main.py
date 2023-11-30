import math
from dataclasses import dataclass
from designer import *
from random import randint
import random


center_width = get_width() / 2
SLICER_SPEED = 50
object_paths = ["/images/apple.png", "/images/orange.png", "/images/pear.png", "/images/blueberry.png"]
bug_paths = ["/images/mite.png", "/images/bee.png"]


@dataclass
class Meat:
    """
    The Meat class is used to define the objects that fall from objects after they are "sliced".
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
class Object:
    """
    The Object class is used to define the objects that spawn from the side and can be "sliced" by the slicer.
    rect(DesignerObject): This is the circular object that provides the image and boundaries of the Object image.
    moving_right(bool): This is the attribute that defines what direction the Object should move.
    period(int): This is the period of the movement wave of the Object.
    amplitude(int): This is the amplitude of the movement wave of the Object.
    midpoint(int): This is the midpoint of the movement wave of the Object.
    bug(bool): This attribute tracks if it is a bug or not.
    is_splatter(bool): This attribute tracks if the Object is a fruit that has been cut.
    splatter_frames(int): This is the amount of frames the splatter will be on screen.
    """
    rect: DesignerObject
    moving_right: bool
    period: int
    amplitude: int
    midpoint: int
    bug: bool
    is_splatter: bool
    splatter_frames: int


@dataclass
class World:
    """
    The World class is used to define the world that holds all the other objects in used in the game.
    started(bool): This determines if the game has started yet.
    bugs_mode(bool): This determines if the bugs game mode was selected.
    options(list[DesignerObject]): This displays the game mode options at the beginning of the game.
    slicer(DesignerObject): This is the rectangular object that can be controlled with the space bar.
    slicer_speed(int): This is the attribute that defines what speed and direction the slicer should move.
    scale(DesignerObject): This is the scale that is shown with an image, and interacts with the Meat.
    lives(int): This is the amount of lives the player has.
    life_counter(DesignerObject): This is the text displaying lives.
    weight(int): This is the weight(points) the player has gained.
    weight_counter(DesignerObject): This is the text displaying the weight.
    objects(list[Object]): This is the list containing the objects on screen.
    meats(list[Meat]): This is the list containing the meats on screen.
    end_text(DesignerObject): This is the text that will not be shown until the end of the game.
    total_object(int): This is the amount of objects that have been spawned in total.
    """
    started: bool
    bugs_mode: bool
    options: list[DesignerObject]
    slicer: DesignerObject
    slicer_speed: int
    scale: DesignerObject
    lives: int
    life_counter: DesignerObject
    weight: int
    weight_counter: DesignerObject
    objects: list[Object]
    meats: list[Meat]
    end_text: DesignerObject
    total_object: int


def create_world() -> World:
    """
    Creates the world of the game
    :return: World
    """
    set_window_color('lightskyblue')
    return World(False, False, display_options(), create_slicer(), 0, image("/images/scale.png", center_width,
                 get_height() - 50), 5, text("red", "5", 100, 50, 50, font_name="Josefin Sans"),
                 0, text("black", "0", 30, center_width, get_height() - 40, font_name="Josefin Sans"),
                 [], [], text("black", "", 100, center_width, get_height() / 2), 0)


def display_options() -> list[DesignerObject]:
    buttons = []
    normal_button = rectangle("black", 150, 150, center_width - 170, get_height() - 180)
    normal_text = text("white", "Normal", 40, normal_button.x, normal_button.y)
    bugs_button = rectangle("black", 150, 150, center_width + 170, get_height() - 180)
    bugs_text = text("white", "Bugs", 40, bugs_button.x, bugs_button.y)
    buttons.append(normal_button)
    buttons.append(normal_text)
    buttons.append(bugs_button)
    buttons.append(bugs_text)
    return buttons


def select_gamemode(world: World, key: str):
    if not world.started:
        if key == "n" or key == "b":
            world.started = True
            for obj in world.options:
                destroy(obj)
            if key == "n":
                world.bugs_mode = False
            else:
                world.bugs_mode = True


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


def create_object_bug(paths: list[str]) -> Object:
    """
    Creates a object using random numbers within a range
    :return: Nothing
    """
    x = randint(0, 1) * get_width()
    midpoint = randint(0, 80)
    midpoints = [-midpoint, midpoint]
    is_a_bug = "/images/mite.png" in paths
    return Object(image(random.choice(paths), x, int(math.sin(x / 20))),
                 x == 0, randint(16, 75), randint(30, 85), get_height() / 2 + random.choice(midpoints),
                 is_a_bug, False, 3)


def create_meat(world: World, x: int, y: int) -> Meat:
    """
    Creates meat and gives it a randomly generated weight within a certain range
    :param world: The world of the game
    :param x: The x location of the parent object
    :param y: The y location of the parent object
    :return: The Meat created
    """
    weight = randint(20, 40) + int(world.total_object / 5) * 5
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


def update_object(world: World):
    """
    Updates the objects location and removes them from the world once they move offscreen
    :param world: The world of the game
    :return: Nothing
    """
    object_speed = 8 + int(world.total_object / 5)
    for object in world.objects:
        if not object.is_splatter:
            if object.moving_right:
                object.rect.x += object_speed
            else:
                object.rect.x -= object_speed
            object.rect.y = object.midpoint + int(math.sin(object.rect.x / object.period) * object.amplitude)
            if object.rect.x < 0 or object.rect.x > get_width():
                world.objects.remove(object)
                if not world.bugs_mode:
                    world.lives -= 1
                destroy(object.rect)
        else:
            object.splatter_frames -= 1
    collide_slicer_object(world)


def collide_slicer_object(world: World):
    """
    Turns objects into a splatter when they collide with the slicer, removes lives when the slicer hits bugs,
    drops meat when fruit are cut, and removes splatter after it has been on screen for its designated frames.
    :param world: The world of the game
    :return: Nothing
    """
    for object in world.objects:
        if colliding(object.rect, world.slicer) and not object.is_splatter:
            destroy(object.rect)
            if not object.bug:
                world.meats.append(create_meat(world, object.rect.x, object.rect.y))
                object.rect = image("/images/splatter.png", object.rect.x, object.rect.y)
            else:
                object.rect = image("/images/green_splatter.png", object.rect.x, object.rect.y)
                world.lives -= 1
            object.is_splatter = True
        if object.splatter_frames <= 0:
            world.objects.remove(object)
            destroy(object.rect)


def spawn_object(world: World):
    """
    Spawns objects at random times when there are less than 4 on screen
    :param world: The world of the game
    :return: Nothing
    """
    object_limit = len(world.objects) < 4
    chance_of_object = randint(0, 40) == 1
    if object_limit and chance_of_object and world.started:
        world.total_object += 1
        world.objects.append(create_object_bug(object_paths))


def spawn_bugs(world: World):
    """
    Spawns objects at random times when there are less than 4 on screen
    :param world: The world of the game
    :return: Nothing
    """
    if not world.bugs_mode:
        return
    chance_of_bug = randint(0, 80) == 1
    if chance_of_bug and world.started:
        world.objects.append(create_object_bug(bug_paths))


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
when("typing", select_gamemode)
when("typing", start_slicer_movement)
when("updating", update_slicer)
when("updating", stop_slicer)
when("updating", spawn_object)
when("updating", spawn_bugs)
when("updating", update_meat)
when("updating", update_object)
when("updating", update_lives)
when(zero_lives, display_end_text, pause)
start()
