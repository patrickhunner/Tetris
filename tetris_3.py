from asyncio.windows_events import NULL
import pygame
import random
from sys import exit
pygame.init()

screen = pygame.display.set_mode((700,660))
pygame.display.set_caption('TETRIS')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
frame = 60
current_squares = {}
background_image = pygame.image.load('tetris_background.png')
background_image = pygame.transform.smoothscale(background_image,(700,660)).convert_alpha()

background_surface = pygame.Surface((700,660))
background_surface.fill('Light Gray')
title_surface = test_font.render('TETRIS', False, 'Blue')
score = 0
level = 0
iteration = 0
level_framerate = {0:300,1:240,2:180,3:120,4:60}
rows_deleted = 0
font = pygame.font.Font('freesansbold.ttf',32)
object_list = []
timer = 0
keep_squares = []
grid_line = [['.','.','.','.','.','.','.','.','.','.']]
full_grid = grid_line * 21
next_objects = []
c_held = [NULL]

def piece_dictionary(y,x,orientation,piece):
    piece_layouts = {'J':[((x,y),(x,y + 30),(x,y + 60),(x - 30,y + 60),'Red')],
                    'O':[((x,y),(x + 30,y),(x + 30,y + 30),(x,y + 30),'Yellow')],
                    'L':[((x,y),(x,y + 30),(x,y + 60),(x + 30,y + 60),'Blue')],
                    'I':[((x - 30,y),(x,y),(x + 30,y),(x + 60,y),'Brown')],
                    'S':[((x + 30,y),(x,y),(x,y + 30),(x - 30,y + 30),'Black')],
                    'Z':[((x - 30,y),(x,y),(x,y + 30),(x + 30,y + 30),'Green')],
                    'T':[((x,y),(x + 30,y + 30),(x,y + 30),(x - 30,y + 30),'Purple')]}
    for coord in piece_layouts[piece]:
        for i in range(0,4):
            pygame.draw.rect(screen,coord[4],pygame.Rect(coord[i][0],coord[i][1],30,30))

def reload_the_screen():
    global next_objects
    full_rows = []
    x_start = 0
    row_number = 0
    y_start = 0
    constant_x = x_start
    global score
    screen.blit(background_image,(-2,0))
    screen.blit(font.render('Score: ' + str(score), True, 'Red'),(230,50))
    screen.blit(font.render('Next', True, 'Black'),(560,100))
    screen.blit(font.render('Hold',True,'Black'),(30,200))
    next_pieces(next_objects)
    for rows in full_grid:
        dot_count = 0
        row_number += 1
        for dot in rows:
            if dot != '.':
                if dot[1] == 'not moving':
                    dot_count += 1
                pygame.draw.rect(screen,dot[0],pygame.Rect((x_start * 30) + 200,(y_start * 30) + 100,30,30))
            x_start += 1
        if dot_count == 10:
            full_rows.append(row_number)
        y_start += 1
        x_start = constant_x
    if len(full_rows) > 0:
        full_row(full_rows)

def next_pieces(pieces):
    global c_held
    x = 580
    y = 150
    for i in pieces:
        piece_dictionary(y,x,0,i)
        y += 120
    x = 45
    y = 245
    if c_held[0] != NULL:
        piece_dictionary(y,x,0,c_held[0])
    
def full_row(indexes):
    global full_grid
    global rows_deleted
    global score
    global just_moved
    if len(indexes) == 1:
        score += (40 * (level + 1))
        rows_deleted += 1
    if len(indexes) == 2:
        score += (100 * (level + 1))
        rows_deleted += 2
    if len(indexes) == 3:
        score += (300 * (level + 1))
        rows_deleted += 3
    if len(indexes) == 4:
        score += (1200 * (level + 1))
        rows_deleted += 4
    for num in indexes:
        full_grid = full_grid[:num - 1] + [['.','.','.','.','.','.','.','.','.','.']] + full_grid[num:]
    for num in indexes:
        full_grid = [['.','.','.','.','.','.','.','.','.','.']] + full_grid[:num - 1] + full_grid[num:]

def create_new_object(iteration):
    global object_list
    possible_objects = ['S','I','T','J','L','O','Z']
    if iteration == 0:
        for i in range(0,10):
            object_list.append(random.choice(possible_objects))
    else:
        object_list.append(random.choice(possible_objects))

def clear_moving():
    global full_grid
    for col in range(0,20):
        for dot_index in range(0,10):
            if full_grid[col][dot_index] != '.':
                if full_grid[col][dot_index][1] == 'moving':
                    full_grid[col] = full_grid[col][:dot_index] + ['.'] + full_grid[col][dot_index + 1:]
                else:
                    pass

def static_squares(squares,color):
    global down
    global faster
    global stop_moving
    global full_grid
    for ind in squares:
        for points in ind:
            x_index = points[0]
            y_index = points[1] - 1
            full_grid = full_grid[:y_index] + [full_grid[y_index][:x_index] + [[color,'not moving']] + full_grid[y_index][x_index + 1:]] + full_grid[y_index + 1:]
        down = False
        faster = False
        stop_moving = True

def update_grid(coordinates,color,orientation):
    global keep_squares
    keep_squares = []
    keep_squares.append(coordinates[orientation])
    global full_grid
    for rectangles in coordinates[orientation]:
        x_index = rectangles[0]
        y_index = rectangles[1]
        if y_index == 18 or full_grid[y_index][x_index] != '.':
            static_squares(keep_squares,color)
            break
        elif full_grid[y_index][x_index] == '.':
            full_grid = full_grid[:y_index] + [full_grid[y_index][:x_index] + [[color,'moving']] + full_grid[y_index][x_index + 1:]] + full_grid[y_index + 1:]

def collide_left_right():
    global keep_squares
    for squares in keep_squares:
        for points in squares:
            if points[0] == 0:
                return 'left'
            if points[0] == 9:
                return 'right'
            if full_grid[points[1]][points[0] + 1] != '.':
                if full_grid[points[1]][points[0] + 1][1] == 'not moving':
                    return 'right'
            if full_grid[points[1]][points[0] - 1] != '.':
                if full_grid[points[1]][points[0] - 1][1] == 'not moving':
                    return 'left'

def find_piece(y,x,orientation,piece,nature):
    global piece_layouts
    if piece == 'J':
        rect_coordinates = [((x,y),(x,y + 1),(x,y + 2),(x - 1,y + 2)),
                            ((x - 1,y),(x - 1,y + 1),(x,y + 1),(x + 1,y + 1)),
                            ((x,y),(x - 1,y),(x - 1,y + 1),(x - 1,y + 2)),
                            ((x - 1,y),(x,y),(x + 1,y),(x + 1,y + 1))]
        if nature == 'current':
            update_grid(rect_coordinates,'Red',orientation)
    elif piece == 'O':
        rect_coordinates = [((x,y),(x + 1,y),(x + 1,y + 1),(x,y + 1))]
        if nature == 'current':
            update_grid(rect_coordinates,'Yellow',orientation)
    elif piece == 'L':
        rect_coordinates = [((x,y),(x,y + 1),(x,y + 2),(x + 1,y + 2)),
                            ((x - 1,y),(x - 1,y + 1),(x,y),(x + 1,y)),
                            ((x - 1,y),(x,y),(x,y + 1),(x,y + 2)),
                            ((x - 1,y + 1),(x,y + 1),(x + 1,y + 1),(x + 1,y))]
        if nature == 'current':
            update_grid(rect_coordinates,'Blue',orientation)
    elif piece == 'I':
        rect_coordinates = [((x,y),(x - 1,y),(x + 1,y),(x - 2,y)),
                            ((x,y),(x,y + 1),(x,y + 2),(x,y + 3))]
        if nature == 'current':
            update_grid(rect_coordinates,'Brown',orientation)
    elif piece == 'S':
        rect_coordinates = [((x + 1,y),(x,y),(x,y + 1),(x - 1,y + 1)),
                            ((x - 1,y),(x - 1,y + 1),(x,y + 1),(x,y + 2))]
        if nature == 'current':
            update_grid(rect_coordinates,'Black',orientation)
    elif piece == 'Z':
        rect_coordinates = [((x - 1,y),(x,y),(x,y + 1),(x + 1,y + 1)),
                            ((x + 1,y),(x + 1,y + 1),(x,y + 1),(x,y + 2))]
        if nature == 'current':
            update_grid(rect_coordinates,'Green',orientation)
    elif piece == 'T':
        rect_coordinates = [((x,y),(x + 1,y + 1),(x,y + 1),(x - 1,y + 1)),
                            ((x - 1,y),(x - 1,y + 1),(x - 1,y + 2),(x,y + 1)),
                            ((x - 1,y),(x,y),(x + 1,y),(x,y + 1)),
                            ((x,y + 1),(x + 1,y),(x + 1,y + 1),(x + 1,y + 2))]
        if nature == 'current':
            update_grid(rect_coordinates,'Purple',orientation)

def switch_pieces():
    global c_switched
    global c_held
    global current_object
    if c_held[0] == NULL:
        c_held[0] = current_object
        current_object = next_objects[0]
    else:
        trade = c_held[0]
        c_held[0] = current_object
        current_object = trade
    c_switched = True

while True:
    screen.fill('Light Gray')
    reload_the_screen()
    x = 0
    y = 4
    orientation = 0
    two_orientation_objects = ['S','I','Z']
    four_orientation_objects = ['J','L','T']
    one_orientation_objects = ['O']
    create_new_object(iteration)
    current_object = object_list[iteration]
    next_objects = [object_list[iteration + 1],object_list[iteration + 2],object_list[iteration + 3]]
    iteration += 1
    faster = False
    stop_moving = False 
    just_moved = False
    level = rows_deleted // 10
    down = False
    move_left = False
    move_right = False
    c_switched = False
    just_switched = False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and collide_left_right() != 'left':
                    y -= 1
                if event.key == pygame.K_RIGHT and collide_left_right() != 'right':
                    y += 1
                if event.key == pygame.K_UP:
                    orientation += 1
                    if current_object in two_orientation_objects and orientation == 2:
                        orientation = 0
                    if current_object in four_orientation_objects and orientation == 4:
                        orientation = 0
                    elif current_object == 'O' and orientation == 1:
                        orientation = 0
                if event.key == pygame.K_DOWN:
                    faster = True
                if event.key == pygame.K_SPACE:
                    down = True
                if event.key == pygame.K_c and c_switched == False:
                    switch_pieces()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    faster = False

        clear_moving()
        reload_the_screen()
        find_piece(x,y,orientation,current_object,'current')
        reload_the_screen()
        pygame.display.update()
        clock.tick(300)
        if stop_moving == True:
            break
        if c_switched == True and just_switched == False:
            x = 0
            just_switched = True
        else:
            timer += 1
            if faster == True:
                if timer % 15 == 0:
                    x += 1
            elif down == True:
                if timer % 1 == 0:
                    x += 1
            else:
                if timer % level_framerate[level] == 0:
                    x += 1

    pygame.display.update()
    clock.tick(300)