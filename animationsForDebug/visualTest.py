# THIS MODULE IS TO TEST IF THE COORDINATES ETC WORK, pygame-wise
# import the pygame module 
import pygame 
from visualSprites import Sprite
from parseJson import *
#ensure this matches in game settings
LEFTBORDER = 0
RIGHTBORDER = 15

MULTIPLIER = 80
 
WIDTH = (RIGHTBORDER - LEFTBORDER) * 80
HEIGHT = 500 

left_file = "jsonfiles\p1.json"
right_file = "jsonfiles\p2.json"

RED = (255, 0, 0) 
BLUE = (0, 255, 0)
BLACK = (0,0,0)

# Define the background colour 
# using RGB color coding. 
background_colour = (234, 212, 252) 
  
  
def setup():
    # Define the dimensions of 
    # screen object(width,height) 
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    
    # Set the caption of the screen 
    pygame.display.set_caption('Visual testing') 
    
    # Fill the background colour to the screen 
    screen.fill(background_colour) 
    
    # Update the display using flip 
    pygame.display.flip() 
    
    # Variable to keep our game loop running 
    running = True
    
    pygame.init() 
    
    p1_coords = get_coordinates(left_file)
    p2_coords = get_coordinates(right_file)
    p1_moves = get_moves(left_file)
    p2_moves = get_moves(right_file)
    p1_hp = get_info(left_file,'hp')
    p2_hp = get_info(right_file, 'hp')
    p1_stuns = get_info(left_file, 'stun')
    p2_stuns = get_info(right_file, 'stun')

    newp1_coords = configure_coords(p1_coords)
    newp2_coords = configure_coords(p2_coords)
    init_p1_coord = newp1_coords[0]
    init_p2_coord = newp2_coords[0]


    
    size = (WIDTH, HEIGHT) 
    screen = pygame.display.set_mode(size) 
    pygame.display.set_caption("Creating Sprite") 
    
    all_sprites_list = pygame.sprite.Group() 
    
    p1_ = Sprite(RED, 50, 50, newp1_coords, p1_coords, p1_moves, p1_hp, p1_stuns) 
    p1_.rect.x, p1_.rect.y = init_p1_coord
    
    p2_ = Sprite(BLUE, 50, 50, newp2_coords, p2_coords, p2_moves, p2_hp, p2_stuns) 
    p2_.rect.x, p2_.rect.y = init_p2_coord

    all_sprites_list.add(p1_) 
    all_sprites_list.add(p2_) 

    screen.fill(background_colour) 
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, 300, WIDTH, 1000))
    pygame.display.flip()
    
    return all_sprites_list, screen, p1_ , p2_
 
# reconfigure the coords to match the screen size    
def configure_coords(coords):
    new_coords = list(coords)
    for pos_index in range(len(new_coords)):
        pos = list(new_coords[pos_index])
        pos[0] *= MULTIPLIER
        pos[1] =  250 - (pos[1] * 50)
        new_coords[pos_index] = pos
    print(new_coords)
    return new_coords

def gameLoop():
    all_sprites_list, screen, p1, p2 = setup()
    running = True
    turn = 0
    while running: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    p1.prev_move()
                    p2.prev_move()
                elif event.key == pygame.K_RIGHT:
                    p1.next_move()
                    p2.next_move()
                
        all_sprites_list.update() 
        screen.fill(background_colour) 
        all_sprites_list.draw(screen) 
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 300, WIDTH, 1000))
        pygame.display.flip() 
        
        #todo add button events to move between previous and next turn
        #todo : player stats, projectile sprites
        turn += 1
    
gameLoop()