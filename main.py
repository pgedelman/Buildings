import math
from dataclasses import dataclass
from designer import *
from random import randint
import random


@dataclass
class Meat:
    """
    The Meat class is used to define the objects that fall from FlyingObject after they are "sliced".
    rect(DesignerObject): This is the circular FlyingObject that provides the color and boundaries of the Meat.
    weight(int): This is the weight of the Meat, which effects the weight shown by display_weight and the scale.
    display_weight(DesignerObject): This is the text that shows what the weight of the Meat is.
    y_velocity(int): This is the current vertical velocity of the Meat.
    """
    rect: DesignerObject
    weight: int
    display_weight: DesignerObject
    y_velocity: int


@dataclass
class FlyingObject:
    """
    The FlyingObject class is used to define the FlyingObject that spawn
     from the side and can be "sliced" by the slicer.
    rect(DesignerObject): This is the circular FlyingObject that provides
     the image and boundaries of the FlyingObject image.
    moving_right(bool): This is the attribute that defines what direction the FlyingObject should move.
    period(int): This is the period of the movement wave of the FlyingObject.
    amplitude(int): This is the amplitude of the movement wave of the FlyingObject.
    midpoint(int): This is the midpoint of the movement wave of the FlyingObject.
    bug(bool): This attribute tracks if it is a bug or not.
    is_splatter(bool): This attribute tracks if the FlyingObject is a fruit that has been cut.
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
    The World class is used to define the world that holds all the other FlyingObjects in used in the game.
    started(bool): This determines if the game has started yet.
    bugs_mode(bool): This determines if the bugs game mode was selected.
    options(list[DesignerObject]): This displays the game mode options at the beginning of the game.
    slicer(DesignerObject): This is the rectangular FlyingObject that can be controlled with the space bar.
    slicer_speed(int): This is the attribute that defines what speed and direction the slicer should move.
    scale(DesignerObject): This is the scale that is shown with an image, and interacts with the Meat.
    lives(int): This is the amount of lives the player has.
    corner_box(DesignerObject): This is the box in the corner of the screen for aesthetic purposes.
    weight(int): This is the weight(points) the player has gained.
    weight_counter(DesignerObject): This is the text displaying the weight.
    flying_objects(list[FlyingObject]): This is the list containing the FlyingObject on screen.
    meats(list[Meat]): This is the list containing the meats on screen.
    end_text(DesignerObject): This is the text that will not be shown until the end of the game.
    total_flying_object(int): This is the amount of FlyingObject that have been spawned in total.
    life_counter(DesignerObject): This is the text displaying lives.
    flying_object_paths(list[str]): This is the
    bug_paths(list[str]):
    """
    started: bool
    bugs_mode: bool
    options: list[DesignerObject]
    slicer: DesignerObject
    slicer_speed: int
    scale: DesignerObject
    lives: int
    corner_box: DesignerObject
    weight: int
    weight_counter: DesignerObject
    flying_objects: list[FlyingObject]
    meats: list[Meat]
    total_flying_object: int
    life_counter: DesignerObject
    end_text_box: DesignerObject
    end_text: DesignerObject
    flying_object_paths: list[str]
    bug_paths: list[str]


def create_world() -> World:
    """
    Creates the world of the game
    :return: World
    """
    set_window_color('lightskyblue')
    new_world = World(False, False, display_options(), create_slicer(), 0, image("/images/scale.png", get_width() / 2,
                 get_height() - 50), 5, rectangle("white", 75, 75, 50, 50),
                 0, text("black", "0", 30, get_width() / 2, get_height() - 40, font_name="Josefin Sans"),
                 [], [], 0, text("black", "5", 100, 50, 50, font_name="Josefin Sans"),
                 rectangle("white", 700, 200, get_width() / 2, get_height() / 2),
                 text("black", "", 100, get_width() / 2, get_height() / 2, font_name="Josefin Sans"),
                 ["/images/apple.png", "/images/orange.png", "/images/pear.png", "/images/blueberry.png"],
                 ["/images/mite.png", "/images/bee.png"])
    hide(new_world.end_text_box)
    return new_world


def display_options() -> list[DesignerObject]:
    """
    This function is used to display the gamemode options at the beginning of the game
    :return:
    """
    buttons = []
    normal_button = rectangle("black", 150, 150, get_width() / 2 - 170, get_height() / 2)
    normal_text = text("white", "Normal", 40, normal_button.x, normal_button.y, font_name="Josefin Sans")
    bugs_button = rectangle("black", 150, 150, get_width() / 2 + 170, get_height() / 2)
    bugs_text = text("white", "Bugs", 40, bugs_button.x, bugs_button.y, font_name="Josefin Sans")
    buttons.append(normal_button)
    buttons.append(normal_text)
    buttons.append(bugs_button)
    buttons.append(bugs_text)
    return buttons


def select_gamemode(world: World, key: str):
    """
    This function controls the gamemode being selected
    :param world:
    :param key:
    :return:
    """
    if not world.started:
        if key == "n" or key == "b":
            world.started = True
            for flying_object in world.options:
                destroy(flying_object)
            if key == "n":
                world.bugs_mode = False
            else:
                world.bugs_mode = True


def create_slicer() -> DesignerObject:
    """
    Creates the slicer
    :return: DesignerObject
    """
    return rectangle("black", 10, 80, get_width() / 2, 40)


def update_weight(world: World):
    """
    Updates the weight displayed on the scale
    :param world: The world of the game
    :return: Nothing
    """
    world.weight_counter.text = str(world.weight)


def start_slicer_movement(world: World, key: str):
    """
    Starts the slicer movement if the slicer is at either endpoint
    :param world: The world of the game
    :param key: The key pressed by the user
    :return: Nothing
    """
    if key == "space":
        if world.slicer.y == 40:
            world.slicer_speed = 50
        elif world.slicer.y == get_height() - 140:
            world.slicer_speed = -50


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


def create_flying_object_bug(paths: list[str]) -> FlyingObject:
    """
    Creates a FlyingObject using random numbers within a range
    :param paths: The list of paths that will be used for the FlyingObject
    :return: FlyingObject
    """
    x = randint(0, 1) * get_width()
    midpoint = randint(0, 80)
    midpoints = [-midpoint, midpoint]
    is_a_bug = "/images/mite.png" in paths
    return FlyingObject(image(random.choice(paths), x, int(math.sin(x / 20))),
                x == 0, randint(16, 75), randint(30, 85), get_height() / 2 + random.choice(midpoints),
                is_a_bug, False, 3)


def create_meat(world: World, x: int, y: int) -> Meat:
    """
    Creates meat and gives it a randomly generated weight within a certain range
    :param world: The world of the game
    :param x: The x location of the parent FlyingObject
    :param y: The y location of the parent FlyingObject
    :return: The Meat created
    """
    weight = randint(20, 40) + int(world.total_flying_object / 5) * 5
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


def update_flying_object(world: World):
    """
    Updates the FlyingObjects location and removes them from the world once they move offscreen
    :param world: The world of the game
    :return: Nothing
    """
    flying_object_speed = 8 + int(world.total_flying_object / 5)
    for flying_object in world.flying_objects:
        if not flying_object.is_splatter:
            if flying_object.moving_right:
                flying_object.rect.x += flying_object_speed
            else:
                flying_object.rect.x -= flying_object_speed
            flying_object.rect.y = flying_object.midpoint + int(math.sin(flying_object.rect.x / flying_object.period) * flying_object.amplitude)
            if flying_object.rect.x < 0 or flying_object.rect.x > get_width():
                world.flying_objects.remove(flying_object)
                if not world.bugs_mode:
                    world.lives -= 1
                destroy(flying_object.rect)
        else:
            flying_object.splatter_frames -= 1
    collide_slicer_flying_object(world)


def collide_slicer_flying_object(world: World):
    """
    Turns FlyingObjects into a splatter when they collide with the slicer, removes lives when the slicer hits bugs,
    drops meat when fruit are cut, and removes splatter after it has been on screen for its designated frames.
    :param world: The world of the game
    :return: Nothing
    """
    for flying_object in world.flying_objects:
        if colliding(flying_object.rect, world.slicer) and not flying_object.is_splatter:
            destroy(flying_object.rect)
            if not flying_object.bug:
                world.meats.append(create_meat(world, flying_object.rect.x, flying_object.rect.y))
                flying_object.rect = image("/images/splatter.png", flying_object.rect.x, flying_object.rect.y)
            else:
                flying_object.rect = image("/images/green_splatter.png", flying_object.rect.x, flying_object.rect.y)
                world.lives -= 1
            flying_object.is_splatter = True
        if flying_object.splatter_frames <= 0:
            world.flying_objects.remove(flying_object)
            destroy(flying_object.rect)


def spawn_flying_object(world: World):
    """
    Spawns FlyingObjects at random times when there are less than 4 on screen
    :param world: The world of the game
    :return: Nothing
    """
    flying_object_limit = len(world.flying_objects) < 4
    chance_of_flying_object = randint(0, 40) == 1
    if flying_object_limit and chance_of_flying_object and world.started:
        world.total_flying_object += 1
        world.flying_objects.append(create_flying_object_bug(world.flying_object_paths))


def spawn_bugs(world: World):
    """
    Spawns FlyingObjects at random times when there are less than 4 on screen
    :param world: The world of the game
    :return: Nothing
    """
    if not world.bugs_mode:
        return
    chance_of_bug = randint(0, 80) == 1
    if chance_of_bug and world.started:
        world.flying_objects.append(create_flying_object_bug(world.bug_paths))


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
    for flying_object in world.flying_objects:
        destroy(flying_object.rect)
    show(world.end_text_box)
    world.slicer.y = world.slicer.height / 2
    world.end_text.text = "Final Weight: " + str(world.weight) + "!"

# The functions that control the interaction and ecosystem of the game


when("updating", update_weight)
when("starting", create_world)
when("typing", select_gamemode)
when("typing", start_slicer_movement)
when("updating", update_slicer)
when("updating", stop_slicer)
when("updating", spawn_flying_object)
when("updating", spawn_bugs)
when("updating", update_meat)
when("updating", update_flying_object)
when("updating", update_lives)
when(zero_lives, display_end_text, pause)
start()
