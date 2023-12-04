import random
from PlayerConfigs import Player_Controller
from test import validMove


#game settings
timeLimit = 60
movesPerSecond =2

#move how many unit per tick
gravity = 2

#direction constants

GORIGHT = 1
GOLEFT = -1

#player variables


player1 = Player_Controller(1,0,50,GORIGHT)
player2 = Player_Controller(4,0,50,GOLEFT)



def move(player, action):
    if (action[0] == "move"):
        if validMove(action[1]) and not player.midair:
            player.moves.append(action)
            player.xCoord += player.direction * action[1][0]
            player.yCoord += action[1][1]
            if player.yCoord > 0:
                player.midair = True
        elif player.midair:
            player.yCoord -= 1
            if player.yCoord == 0:
                player.midair = False
        else:    
            raise Exception("Invalid movement direction")

def block(player, action):
    if (action[0] == "block"):
        player.moves.append(action)
        if player.blocking:
            player.blocking =True

def attack(player,target, action):
    if (action[0] == "attack"):
        player.moves.append(action)
        #TODO attack variations such as heavy and light
        # check if attack lands
        if (abs(player.xCoord-target.xCoord) == 1 and player.yCoord == target.yCoord):
            #check for blocks
            if(target.blocking):
                #parry if block is frame perfect
                if target.moves[-2] != "block":
                    player.stun = 2
            else:
                target.hp -=5
                
def flip_orientation(player1, player2):
    if player1.xCoord > player2.xCoord:
        # should flip orientations if they switch sides
        return True
    return False


def startGame():
    
    for tick in range(5):
        
        print(f"P1 : {player1.xCoord, player1.yCoord}")
        print(f"P2 : {player2.xCoord, player2.yCoord}")
        if flip_orientation(player1, player2):
            player1.direction = GOLEFT
            player2.direction = GORIGHT
        else:
            player1.direction = GORIGHT
            player2.direction = GOLEFT
            
        act1 = player1.action()
        act2 = player2.action()
        
        if not player1.stun:
            move(player1, act1)
            block(player1, act1)
            attack(player1, player2, act1)
            player1.moveNum += 1
        else:
            player1.stun -= 1
            
        if not player2.stun:
            move(player2, act2)
            block(player2, act2)
            attack(player2, player1, act2)
            player2.moveNum += 1
        else:
            player2.stun -= 1
        