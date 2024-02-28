# THIS MODULE IS TO TEST IF THE COORDINATES ETC WORK, pygame-wise
# import the pygame module 
import pygame 
from visualSprites import Sprite, SURFACE_COLOR
from parseJson import get_coordinates

RIGHTBORDER = 15
LEFTBORDER = 0
 
WIDTH = (RIGHTBORDER - LEFTBORDER) * 75
HEIGHT = 500 

left_file = "jsonfiles\p1.json"
right_file = "jsonfiles\p2.json"
# Define the background colour 
# using RGB color coding. 
background_colour = (234, 212, 252) 
  
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
  
RED = (255, 0, 0) 
BLUE = (0, 255, 0)

p1_coords = get_coordinates(left_file)
p2_coords = get_coordinates(right_file)

print(p1_coords)
init_p1_coord = p1_coords[0]
init_p2_coord = p2_coords[0]
  
size = (WIDTH, HEIGHT) 
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Creating Sprite") 
  
all_sprites_list = pygame.sprite.Group() 
  
p1_ = Sprite(RED, 50, 50) 
p1_.rect.x , p1_.rect.y = init_p1_coord[0] * 100, init_p1_coord[1] * 50 + 250

p2_ = Sprite(BLUE, 50, 50) 
p2_.rect.x , p2_.rect.y = init_p2_coord[0] * 100, init_p2_coord[1] * 50 + 250
  
all_sprites_list.add(p1_) 
all_sprites_list.add(p2_) 


while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
  
    all_sprites_list.update() 
    screen.fill(background_colour) 
    all_sprites_list.draw(screen) 
    pygame.display.flip() 
    
    #todo add button events to move between previous and next turn
    #todo : player stats, projectile sprites
    
    
    