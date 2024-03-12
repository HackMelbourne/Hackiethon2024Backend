import pygame 
  
# GLOBAL VARIABLES 
COLOR = (255, 100, 98) 
SURFACE_COLOR = (167, 255, 100) 

# Object class 
class Sprite(pygame.sprite.Sprite): 
    def __init__(self, color, height, width, coords, jsonCoords, moveData, hps, stuns): 
        super().__init__() 
  
        self.image = pygame.Surface([width, height]) 
        self.image.fill(SURFACE_COLOR) 
        self.image.set_colorkey(COLOR) 
  
        pygame.draw.rect(self.image, 
                         color, 
                         pygame.Rect(0, 0, width, height)) 
  
        self.rect = self.image.get_rect() 
        self.coords = coords
        self.jsonCoords = jsonCoords
        self.moveData = moveData
        self.hps = hps
        self.stuns = stuns
        self.moveNum = 0
    def next_move(self):
        try:
            next_pos = self.coords[self.moveNum]
            self.rect.x = next_pos[0]
            self.rect.y = next_pos[1]
            print(f"{self.jsonCoords[self.moveNum]} : {self.moveData[self.moveNum]}, {self.hps[self.moveNum]}, stun: {self.stuns[self.moveNum]}")
            print(f"next move:                        {self.moveData[self.moveNum + 1]}")
            self.moveNum += 1
        except IndexError:
            return None
        
    def prev_move(self):
        try:
            self.moveNum -= 1
            if self.moveNum < 0:
                self.moveNum = 0
            prev_pos = self.coords[self.moveNum]
            self.rect.x = prev_pos[0]
            self.rect.y = prev_pos[1]
            print(f"{self.jsonCoords[self.moveNum]} : {self.moveData[self.moveNum]}, {self.hps[self.moveNum]}, stun: {self.stuns[self.moveNum]}")
            print(f"next move:                        {self.moveData[self.moveNum + 1]}")
        except IndexError:
            return None
        
    def next_proj_move(self):
        try:
            next_pos = self.coords[self.moveNum]
            self.rect.x = next_pos[0]
            self.rect.y = next_pos[1]
            print(f"{self.jsonCoords[self.moveNum]}")
            self.moveNum += 1
        except IndexError:
            return None
        
    def prev_proj_move(self):
        try:
            self.moveNum -= 1
            if self.moveNum < 0:
                self.moveNum = 0
            prev_pos = self.coords[self.moveNum]
            self.rect.x = prev_pos[0]
            self.rect.y = prev_pos[1]
            print(f"{self.jsonCoords[self.moveNum]}")
        except IndexError:
            return None