"""
TO DO:
- Add movement object to the list
- Calculate velocity vector of the object
- Each tick increase the
- Draw the progress
"""
import pygame
import math
import copy

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
class Colors:
    BLACK       = (  0,   0,   0)
    WHITE       = (255, 255, 255)
    GRAY        = (200, 200, 200)
    LIGHT_GRAY  = (128, 128, 128)
    BLUE        = (  0,  38, 255)
    DARK_BLUE   = (  0,  19, 127)
    GREEN       = (  0, 255,  33)
    DARK_GREEN  = (  0, 127,  14)
    RED         = (255,   0,   0)
    DARK_RED    = (127,   0,   0)
    YELLOW      = (255, 216,   0)
    DARK_YELLOW = (127, 106,   0)

class SpaceColors:
    GREEN = [Colors.DARK_GREEN, Colors.GREEN]
    BLUE = [Colors.DARK_BLUE, Colors.BLUE]
    RED = [Colors.DARK_RED, Colors.RED]
    YELLOW = [Colors.DARK_YELLOW, Colors.YELLOW]
    GRAY = [Colors.GRAY, Colors.GRAY]

# Size in pixels of each Space type
class SpaceSizes:
    SMALL   = (50, 50)
    MEDIUM  = (60, 60)
    LARGE   = (80, 80)
    XLARGE  = (90, 90)

# Amount of (100 members = 1 unit)
class SpaceRecruiting:
    # Ammount of units increase each tick
    SMALL   = 0.01
    MEDIUM  = 0.02
    LARGE   = 0.03
    XLARGE  = 0.04

class Space:
    _id = 0
    color = SpaceColors.GRAY
    pos = [0, 0]
    center = [0, 0]
    size = SpaceSizes.XLARGE
    units = 10
    #owner = PlayerColors.GRAY

    # Get the center position considering the top-left pos and size
    def getCenter(self):
        center = []
        center.append(int(self.pos[0] + (self.size[0] / 2)))
        center.append(int(self.pos[1] + (self.size[1] / 2)))
        return center

class Movement:
    space_origin_id = 0
    space_dest_id = 0
    # Current progress and total
    progress = [0, 0]
    # Vector to express speed in units/s
    speed = [0.0, 0.0]
    current_pos = [0, 0]
    units = 0
    player_color = None

_debug = True

# Set the height and width of the screen
size = (800, 600)
screen = pygame.display.set_mode(size)
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("World render")

units_font = pygame.font.SysFont("Arial", 20)
movement_font = pygame.font.SysFont("Arial", 16)

mouse_pos = [0, 0]
current_selection = []

spaces = []
movements = []
players = [SpaceColors.BLUE, SpaceColors.GREEN]

# Constants
FPS = 30 # Frames per second
UNITS_SPEED = 8 # Px per tick (px * 30)
MOVEMENT_SIZE = (30, 30)

back = pygame.image.load('back.jpg')
back_rect = back.get_rect()

def createSampleSpaces():
    current_space = Space()
    current_space._id = 0
    current_space.color = SpaceColors.BLUE
    current_space.pos = [50, 50]
    current_space.size = SpaceSizes.XLARGE
    current_space.units = 100

    spaces.append(current_space)

    current_space = Space()
    current_space._id = 1
    current_space.color = SpaceColors.GREEN
    current_space.pos = [650, 450]
    current_space.size = SpaceSizes.XLARGE
    current_space.units = 100

    spaces.append(current_space)

    current_space = Space()
    current_space._id = 2
    current_space.color = SpaceColors.GRAY
    current_space.pos = [400, 400]
    current_space.size = SpaceSizes.SMALL

    spaces.append(current_space)

    current_space = Space()
    current_space._id = 3
    current_space.color = SpaceColors.GRAY
    current_space.pos = [240, 120]
    current_space.size = SpaceSizes.SMALL

    spaces.append(current_space)

    current_space = Space()
    current_space._id = 4
    current_space.color = SpaceColors.GRAY
    current_space.pos = [350, 250]
    current_space.size = SpaceSizes.MEDIUM

    spaces.append(current_space)

def checkClick(mouse_position):
    global current_selection

    was_space_found = False

    # Check if we've clicked a space
    for space in spaces:
        is_in_x = space.pos[0] <= mouse_position[0] <= (space.pos[0] + space.size[0])
        is_in_y = space.pos[1] <= mouse_position[1] <= (space.pos[1] + space.size[1])
        if is_in_x and is_in_y:
            was_space_found = True
            found_space_id = space._id

    # Check if we've something selected
    if (len(current_selection) != 0) and was_space_found:
        # Send a command
        percent_to_move = 0.5
        createMovement(current_selection[0], found_space_id, percent_to_move)
        was_space_found = False # Deselect both spaces

    if was_space_found:
        current_selection = [found_space_id]
    else:
        current_selection = []

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

def renderWorld():
    global screen

    # Clear the screen and set the screen background
    screen.blit(back, back_rect)

    # Draw all spaces
    for space in spaces:
        drawSpace(space)

    for movement in movements:
        drawMovement(movement)

    # Update the screen
    pygame.display.flip()

def increaseTick():
    global spaces
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
        #log("Mov:", current_movement_id, movements[current_movement_id].progress[0], \
        #    movements[current_movement_id].progress[1])
        movements[current_movement_id].progress[0] += UNITS_SPEED
        movements[current_movement_id].current_pos[0] += \
            movements[current_movement_id].speed[0] * UNITS_SPEED
        movements[current_movement_id].current_pos[1] += \
            movements[current_movement_id].speed[1] * UNITS_SPEED

        if movements[current_movement_id].progress[0] > \
                movements[current_movement_id].progress[1]:
            print("Movement reached")

            # Action: Add the units to the destination
            applyMovement(movements[current_movement_id])
            movements_to_remove.append(current_movement_id)

    for current_movement_id in reversed(movements_to_remove):
        del(movements[current_movement_id])

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

    travel_distance = math.floor(getDistanceBetweenSpaces(space_origin_id, space_destination_id))
    position_origin = spaces[space_origin_key].pos
    position_destination = spaces[space_destination_key].pos
    speed = getUnitVector(position_origin, position_destination)

    current_movement = Movement()
    current_movement.space_origin_id = space_origin_id
    current_movement.space_dest_id = space_destination_id
    current_movement.progress = [0, travel_distance]
    current_movement.speed = speed
    current_movement.units = units_to_move
    current_movement.player_color = spaces[space_origin_key].color
    current_movement.current_pos = copy.copy(spaces[space_origin_key].pos)

    movements.append(current_movement)
    log("Travel distance:", travel_distance, "Speed:", speed)

def applyMovement(movement):
    dest_key = 0 # Destination key

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

def log(*strings):
    if _debug:
        print(strings)

def main():
    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    createSampleSpaces()

    while not done:
        clock.tick(FPS)

        # User's events
        for event in pygame.event.get():
            # User clicked close?
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    checkClick(pygame.mouse.get_pos())

        renderWorld()
        increaseTick()

    # Be IDLE friendly
    pygame.quit()

main()