#!/usr/bin/env python
# coding:utf-8
__author__      = "Emmanuel Parada Licea (@eaplmx)"
__license__     = "The MIT License (MIT)"
__copyright__   = "Copyright (C) 2014"
__version__     = "0.0.2"

# TO DO:
# - Change all strings to a translatable dictionary
# - Allow checkGameOver to work with 4 players. Currently only works for 2.
# - Bug when conquering a space (Appears negative units !)

import pygame
import math
import copy
import random
import os

class Colors:
    "Define the colors we will use in RGB format"
    BLACK       = (  0,   0,   0)
    WHITE       = (255, 255, 255)
    GRAY        = (200, 200, 200)
    LIGHT_GRAY  = (128, 128, 128)
    BLUE        = (  0,  30, 255)
    DARK_BLUE   = (  0,  19, 160)
    GREEN       = (  0, 255,  33)
    DARK_GREEN  = (  0, 127,  14)
    RED         = (255,   0,   0)
    DARK_RED    = (127,   0,   0)
    YELLOW      = (255, 216,   0)
    DARK_YELLOW = (127, 106,   0)

class SpaceColors:
    "Light and Dark colors for each player"
    GREEN   = [Colors.DARK_GREEN, Colors.GREEN]
    BLUE    = [Colors.DARK_BLUE, Colors.BLUE]
    RED     = [Colors.DARK_RED, Colors.RED]
    YELLOW  = [Colors.DARK_YELLOW, Colors.YELLOW]
    GRAY    = [Colors.GRAY, Colors.GRAY]

class SpaceSizes:
    "Size in pixels of each Space type"
    SMALL   = (50, 50)
    MEDIUM  = (60, 60)
    LARGE   = (80, 80)
    XLARGE  = (90, 90)

class SpaceRecruiting:
    "Ammount of units increase each tick"
    SMALL   = 0.01
    MEDIUM  = 0.02
    LARGE   = 0.03
    XLARGE  = 0.04

class Space:
    "Space object (Represented in the screen as a square)"
    _id     = 0
    color   = SpaceColors.GRAY
    pos     = [0, 0]
    center  = [0, 0]
    size    = SpaceSizes.XLARGE
    units   = 10

    # Get the center position considering the top-left pos and size
    def getCenter(self):
        center = []
        center.append(int(self.pos[0] + (self.size[0] / 2)))
        center.append(int(self.pos[1] + (self.size[1] / 2)))
        return center

class Movement:
    "Represents the units moving in the screen from a space to another"
    space_origin_id = 0 # Id of the space where the movement is started
    space_dest_id = 0 # Id of the spece that will receive the units

    # Current progress and total
    progress = [0, 0] # Index 0 = current progress, Index 1 = Max step
    # Vector to express speed in units/s
    movement_vect = [0.0, 0.0]  # Index 0 = X, Index 1 = Y
    current_pos = [0, 0]        # Index 0 = X, Index 1 = Y
    player_color = None         # Instance of SpaceColors
    units = 0

class Player:
    "Object to represent every player color and current spaces conquered"
    color = None
    spaces_num = 0

class Scenes:
    WELCOME = 1
    MAIN_LOOP = 2
    GAME_OVER = 3

# Set it to True to show in the console some debugging messages
_debug = True

"""
Initialization of the game engine
"""
# Init Pygame game engine
pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
icon = pygame.Surface((1,1))
icon.set_alpha(0)
pygame.display.set_icon(icon)
pygame.display.set_caption("GalaHack v0.0.1") # To do: Change to global strings translation

# TO DO: Center the screen

# Game constants
FPS = 30 # Frames per second
UNITS_SPEED = 10 # Px per tick
MOVEMENT_SIZE = (30, 30) # Movement graphic size
MAX_TURN_TIME = 10 * FPS # Ticks (5 secs * 30 = 150)
ART_DIR = "art" + os.sep
TURN_TIMER_SIZE = 30

# Game variables
main_font = ART_DIR + "exo.ttf"
welcome_font = pygame.font.Font(main_font, 50)
units_font = pygame.font.Font(main_font, 20)
movement_font = pygame.font.Font(main_font, 14)

mouse_pos = [0, 0]
current_selection = []
current_turn = None
out = []
current_turn_timer = 0
current_tick = 0

spaces = []
movements = []
players = []

background = pygame.image.load(ART_DIR + 'background.jpg')
background_rect = background.get_rect()

background_welcome = pygame.image.load(ART_DIR + 'back_welcome.jpg')
background_welcome_rect = background_welcome.get_rect()

def randomPos(x, y, margin):
    "Create fuzzy random positions from a point and a range"
    new_pos = []
    new_pos.append(x + random.randint(-margin, margin))
    new_pos.append(y + random.randint(-margin, margin))
    return new_pos

def createSampleSpaces():
    current_space = Space()
    current_space._id = 0
    current_space.color = SpaceColors.BLUE
    current_space.pos = randomPos(50, 50, 15)
    current_space.size = SpaceSizes.XLARGE
    current_space.units = 150
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 1
    current_space.color = SpaceColors.GREEN
    current_space.pos = randomPos(650, 450, 15)
    current_space.size = SpaceSizes.XLARGE
    current_space.units = 150
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 2
    current_space.color = SpaceColors.GRAY
    current_space.pos = randomPos(460, 420, 15)
    current_space.size = SpaceSizes.SMALL
    current_space.units = random.randint(30, 40)
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 3
    current_space.color = SpaceColors.GRAY
    current_space.pos = randomPos(240, 120, 15)
    current_space.size = SpaceSizes.SMALL
    current_space.units = random.randint(30, 40)
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 4
    current_space.color = SpaceColors.GRAY
    current_space.pos = randomPos(350, 250, 15)
    current_space.size = SpaceSizes.MEDIUM
    current_space.units = random.randint(40, 55)
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 5
    current_space.color = SpaceColors.RED
    current_space.pos = randomPos(550, 150, 15)
    current_space.size = SpaceSizes.XLARGE
    current_space.units = 150
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 6
    current_space.color = SpaceColors.YELLOW
    current_space.pos = randomPos(150, 450, 15)
    current_space.size = SpaceSizes.XLARGE
    current_space.units = 150
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 7
    current_space.color = SpaceColors.GRAY
    current_space.pos = randomPos(120, 280, 15)
    current_space.size = SpaceSizes.SMALL
    current_space.units = random.randint(30, 40)
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 8
    current_space.color = SpaceColors.GRAY
    current_space.pos = randomPos(320, 380, 15)
    current_space.size = SpaceSizes.SMALL
    current_space.units = random.randint(30, 40)

    current_space = Space()
    current_space._id = 9
    current_space.color = SpaceColors.GRAY
    current_space.pos = randomPos(310, 470, 15)
    current_space.size = SpaceSizes.SMALL
    current_space.units = random.randint(30, 40)
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 10
    current_space.color = SpaceColors.GRAY
    current_space.pos = randomPos(560, 290, 15)
    current_space.size = SpaceSizes.SMALL
    current_space.units = random.randint(30, 40)
    spaces.append(current_space)

    current_space = Space()
    current_space._id = 11
    current_space.color = SpaceColors.GRAY
    current_space.pos = randomPos(390, 90, 15)
    current_space.size = SpaceSizes.SMALL
    current_space.units = random.randint(30, 40)
    spaces.append(current_space)

def checkWelcomeClick(mouse_position):
    global current_scene
    current_scene = Scenes.MAIN_LOOP

def checkMainLoopClick(mouse_position):
    "Manages selection of spaces and commands each player's turn"
    global current_selection, current_turn

    was_space_found = False
    something_selected = len(current_selection) != 0

    # Check if we've clicked a space
    for space in spaces:
        is_in_x = space.pos[0] <= mouse_position[0] <= (space.pos[0] + space.size[0])
        is_in_y = space.pos[1] <= mouse_position[1] <= (space.pos[1] + space.size[1])

        if something_selected:
            # When something was selected any space is selectable
            selectable = True
        else:
            # Only allow player's spaces on first selection
            selectable = players[current_turn].color == space.color

        different = space._id not in current_selection

        if is_in_x and is_in_y and selectable and different:
            was_space_found = True
            found_space_id = space._id

    # Check if we've something selected
    if something_selected and was_space_found:
        # Send a command
        percent_to_move = 0.5
        createMovement(current_selection[0], found_space_id, percent_to_move)
        was_space_found = False # Deselect both spaces

    if was_space_found:
        current_selection = [found_space_id]
    else:
        current_selection = []

""" REGION: Screen rendering and drawing """

def drawSpace(space):
    global current_selection
    # If selected, get the altenative color
    if space._id in current_selection:
        color_to_render = space.color[1]
    else:
        color_to_render = space.color[0]

    pygame.draw.rect(screen, Colors.BLACK, (space.pos, space.size), 0)
    pygame.draw.rect(screen, color_to_render, (space.pos, space.size), 2)

    # Draw the text
    units = str(int(math.floor(space.units)))
    units_text = units_font.render(units, True, Colors.WHITE)
    text_pos = units_text.get_rect()

    # Center to the space
    text_pos.center = pygame.Rect(space.pos, space.size).center
    screen.blit(units_text, text_pos)

def drawMovement(movement):
    pygame.draw.rect(screen, Colors.BLACK, (movement.current_pos, MOVEMENT_SIZE), 0)
    pygame.draw.rect(screen, movement.player_color[0], (movement.current_pos, MOVEMENT_SIZE), 2)

    # Draw the text
    units = str(int(math.floor(movement.units)))
    units_text = units_font.render(units, True, Colors.WHITE)
    text_pos = units_text.get_rect()

    # Center to the space
    text_pos.center = pygame.Rect(movement.current_pos, MOVEMENT_SIZE).center
    screen.blit(units_text, text_pos)

def drawTurnTimer():
    # The -1 and +1 are small visual hacks, because the square was jumping !
    # Remember to cast the turn timer to float for compatibility with Python 2.7
    fill_amount = (float(current_turn_timer) / MAX_TURN_TIME) * (TURN_TIMER_SIZE - 1) + 1

    # Filling square
    pygame.draw.rect(screen, players[current_turn].color[1], ((740, 32), (TURN_TIMER_SIZE, fill_amount)), 0)
    # Border
    pygame.draw.rect(screen, players[current_turn].color[1], ((740, 30), (TURN_TIMER_SIZE, TURN_TIMER_SIZE)), 2)

def renderWelcome():
    global screen

    # Clear the screen and set the screen background
    screen.blit(background_welcome, background_welcome_rect)

    # Welcome text
    welcome_text = welcome_font.render("GalaHack", True, Colors.WHITE)
    welcome_pos = welcome_text.get_rect()
    welcome_pos.center = background_rect.center
    screen.blit(welcome_text, welcome_pos)

def renderMainLoop():
    global screen

    screen.blit(background, background_rect) # Overwrite all with the background

    # Draw all spaces
    for space in spaces:
        drawSpace(space)

    for movement in movements:
        drawMovement(movement)

    drawTurnTimer()

def renderGameOver():
    renderMainLoop()

    # Welcome text
    welcome_text = welcome_font.render("Game Over", True, Colors.WHITE)
    welcome_pos = welcome_text.get_rect()
    welcome_pos.center = background_rect.center
    screen.blit(welcome_text, welcome_pos)

""" REGION: Math and geometry functions """

def getDistanceBetweenSpaces(space_1_id, space_2_id):
    space_1_pos = [0, 0]
    space_2_pos = [0, 0]

    for space in spaces:
        if space._id == space_1_id:
            space_1_pos = space.getCenter()
        if space._id == space_2_id:
            space_2_pos = space.getCenter()

    distance = ((space_1_pos[0] - space_2_pos[0]) ** 2) + \
                ((space_1_pos[1] - space_2_pos[1]) ** 2)
    distance = math.sqrt(distance)
    log("Distance between spaces:", distance, "S1:", space_1_pos, "S2:", space_2_pos)
    return distance

def getUnitVector(pos_1, pos_2):
    x = pos_1[0] - pos_2[0]
    y = pos_1[1] - pos_2[1]
    distance = math.hypot(x, y)

    if distance != 0:
        i = x / distance;
        j = y / distance;
        return [-i, -j]
    else:
        return [0, 0]

""" REGION: Initialization and flow of the game """

def initGame():
    "Load first scene, define current players and init turns"
    global current_scene, current_turn

    current_scene = Scenes.WELCOME
    createSampleSpaces()

    # The index of current_turn is related with players index
    current_turn = 0

    current_player = Player()
    current_player.color = SpaceColors.BLUE
    players.append(current_player)

    current_player = Player()
    current_player.color = SpaceColors.GREEN
    players.append(current_player)

    current_player = Player()
    current_player.color = SpaceColors.RED
    players.append(current_player)

    current_player = Player()
    current_player.color = SpaceColors.YELLOW
    players.append(current_player)

    """
    DEBUG: Add more players

    current_player = Player()
    current_player.color = SpaceColors.RED
    players.append(current_player)

    current_player = Player()
    current_player.color = SpaceColors.YELLOW
    players.append(current_player)
    """

def nextTurn():
    global current_turn, current_turn_timer, current_selection

    # Loop over the players in the order were defined in "players"
    current_turn += 1
    if current_turn > (len(players) - 1):
        current_turn = 0
    log(current_turn)
    log(out)
    # Restart the turn timer and remove selections of last player
    current_turn_timer = 0
    current_selection = []

def increaseTick():
    "Create new units, manage movement position, apply action when reached the destination"
    global spaces, current_turn_timer, current_tick,current_turn
    for space in spaces:
        if space.size == SpaceSizes.SMALL:
            space.units += SpaceRecruiting.SMALL
        elif space.size == SpaceSizes.MEDIUM:
            space.units += SpaceRecruiting.MEDIUM
        elif space.size == SpaceSizes.LARGE:
            space.units += SpaceRecruiting.LARGE
        elif space.size == SpaceSizes.XLARGE:
            space.units += SpaceRecruiting.XLARGE

    movements_to_remove = []
    
    for current_movement_id in range(len(movements)):
        movements[current_movement_id].progress[0] += UNITS_SPEED
        movements[current_movement_id].current_pos[0] += \
            movements[current_movement_id].movement_vect[0] * UNITS_SPEED
        movements[current_movement_id].current_pos[1] += \
            movements[current_movement_id].movement_vect[1] * UNITS_SPEED

        if movements[current_movement_id].progress[0] > \
                movements[current_movement_id].progress[1]:

            # Action: Add the units to the destination
            applyMovement(movements[current_movement_id])
            movements_to_remove.append(current_movement_id)

    for current_movement_id in reversed(movements_to_remove):
        del(movements[current_movement_id])
    

    current_turn_timer += 1 # Increase turn tick timer
    if current_turn_timer > MAX_TURN_TIME or current_turn in out:
        nextTurn()

    current_tick += 1

def checkGameOver():
    "Check if the players have at least one space to keep playing"
    number_of_players = 0
    global out
    aux = 0
    # Clear the spaces number for each player
    for player in players:
        player.spaces_num = 0

    # Get the spaces each player has in control
    for space in spaces:
        for player in players:
            if space.color == player.color:
                player.spaces_num += 1

    for player in players:
        if player.spaces_num >= 1:            
            number_of_players+=1            
        else:
            if aux not in out:
                out.append(aux)
        aux+=1
          
    return number_of_players

def createMovement(space_origin_id, space_destination_id, percent):
    global movements
    space_origin_key = -1
    space_destination_key = -1

    # Get the keys in the spaces array for the supplied spaces
    for current_space in range(len(spaces)):
        if spaces[current_space]._id == space_origin_id:
            space_origin_key = current_space
        if spaces[current_space]._id == space_destination_id:
            space_destination_key = current_space

    units_to_move = math.floor(percent * spaces[space_origin_key].units)
    log("Units to move:", units_to_move)

    # Add the sustracted units to the movement
    spaces[space_origin_key].units -= units_to_move

    travel_distance = \
        math.floor(getDistanceBetweenSpaces(space_origin_id, space_destination_id))
    position_origin = \
        pygame.Rect(spaces[space_origin_key].pos, spaces[space_origin_key].size).center
    position_destination = \
        pygame.Rect(spaces[space_destination_key].pos, spaces[space_destination_key].size).center
    movement_vect = getUnitVector(position_origin, position_destination)

    current_movement = Movement()
    current_movement.space_origin_id = space_origin_id
    current_movement.space_dest_id = space_destination_id
    current_movement.progress = [0, travel_distance]
    current_movement.movement_vect = movement_vect
    current_movement.units = units_to_move
    current_movement.player_color = spaces[space_origin_key].color
    current_movement.current_pos = [position_origin[0], position_origin[1]]

    movements.append(current_movement)
    log("Travel distance:", travel_distance, "Speed:", movement_vect)
    log("Current tick:", current_tick)

    nextTurn()

def applyMovement(movement):
    "When the movement arrived, add units or conquer the space"
    dest_key = 0 # Key of the destination space

    for current_space in range(len(spaces)):
        if spaces[current_space]._id == movement.space_dest_id:
            dest_key = current_space

    same_player = movement.player_color[0] == spaces[dest_key].color[0]
    if same_player:
        spaces[dest_key].units += movement.units
    else: # Units arrived from a different player color
        if (spaces[dest_key].units - movement.units) < 1:
            # Change the owner color
            spaces[dest_key].color = movement.player_color
            # Fill the space with the opponent player
            new_units = (spaces[dest_key].units - movement.units) * -1
            spaces[dest_key].units = new_units
        else:
            spaces[dest_key].units -= movement.units

""" REGION: Debugging tools """

def log(*strings):
    if _debug:
        print(strings)

def main():
    global current_scene, current_turn

    exit_pygame = False
    clock = pygame.time.Clock()

    initGame()

    while not exit_pygame:
        clock.tick(FPS)

        clicked = False

        # Get the user's events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Clicked close button?
                exit_pygame = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True

        if current_scene == Scenes.WELCOME:
            if clicked:
                checkWelcomeClick(pygame.mouse.get_pos())
            renderWelcome()
        elif current_scene == Scenes.MAIN_LOOP:
            if clicked:
                checkMainLoopClick(pygame.mouse.get_pos())

            renderMainLoop()
            increaseTick()
            if checkGameOver() <= 1:
                print(len(players))

                current_scene = Scenes.GAME_OVER
        elif current_scene == Scenes.GAME_OVER:
             renderGameOver()

        pygame.display.flip() # Update (draw) the screen
    pygame.quit() #IDLE friendly

main()