import random
from test import *
import importlib
from playerActions import *

#game settings
timeLimit = 60
movesPerSecond =2

#move how many unit per tick
gravity = 2

#direction constants

GORIGHT = 1
GOLEFT = -1

#player variables

def setupGame(path1, path2):
    
    p1Import = importlib.import_module("Submissions." + path1)
    p2Import = importlib.import_module("Submissions." + path2)
    player1 = p1Import.Player_Controller(1,0,50,GORIGHT)
    player2 = p2Import.Player_Controller(4,0,50,GOLEFT)
    return player1,player2

#TODO additional checks for skill uses    

#------------------Adding to player1 and player2 move scripts for test----
def setMoves(player1, player2):    
    p1movelist = ("move", (1,0)), ("move", (1,0)), ("attack", "light"), ("attack", "light"),("attack", "light"),
    p2movelist = ("block"), ("block"), ("block"), ("block"), ("block")
    
    player1.moveList.extend(p1movelist)
    player2.moveList.extend(p2movelist)          

def updateCooldown(player):
    #TODO : once primary and secondary skills complete, add reduceCd
    
    # player.lightAtk.reduceCd(1)#TODO uncomment
    # player.heavyAtk.reduceCd(1) #TODO uncomment
    pass

def updateMidair(player):
    if player.midair:
        player.yCoord -= 1
        if player.yCoord == 0: 
            player.midair = False

#im not sure how to make this any more efficient
def performActions(player1, player2, act1, act2, stun1, stun2):
    knock1 = knock2 = 0
    
    if player1.stun:
        player1.stun -= 1
    else:
        player1.moveNum += 1
    if player2.stun:
        player2.stun -= 1
    else:
        player2.moveNum += 1
        
    if not player1.stun:
        move(player1, player2, act1)
    if not player2.stun:
        move(player2, player1, act2)
    if not player1.stun:
        block(player1, act1)
    if not player2.stun:
        block(player2, act2)
    if not player1.stun:
        knock1, stun1 = attack(player1, player2, act1)
    if not player2.stun:
        knock2, stun2 = attack(player2, player1, act2)

    return knock1, stun1, knock2, stun2
                
def startGame(path1, path2):
    print(path1,path2)
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    player1, player2 = setupGame(path1,path2)

    stun1 = stun2 = 0
    
    for tick in range(timeLimit *movesPerSecond):
        #print(f"\nTURN {tick}\n")
        #print(f"P1 : {player1.xCoord, player1.yCoord}")
        #print(f"P2 : {player2.xCoord, player2.yCoord}")

        #flips orientation if player jumps over each other
        if flip_orientation(player1, player2):
            player1.direction = GOLEFT
            player2.direction = GORIGHT
        else:
            player1.direction = GORIGHT
            player2.direction = GOLEFT

        #if midair, start falling
        updateMidair(player1)
        updateMidair(player2)
            
        knock1 = knock2 = 0
        
        act1 = player1.action()
        act2 = player2.action()
            
        knock1, stun1, knock2, stun2 = performActions(player1, player2, act1, act2, stun1, stun2)

        #only determine knockback and stun after attacks hit
        if knock1:
            player2.xCoord += player1.direction * knock1
            player2.stun += stun1
        if knock2:
            player1.xCoord += player2.direction * knock2
            player1.stun += stun2

        updateCooldown(player1)
        updateCooldown(player2)
        #TODO update current startup every tick

    if player1.hp == player2.hp:
        print('match won by: ', path1)
        return path1
    return max(player1.hp, player2.hp)
