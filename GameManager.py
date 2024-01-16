import random
from test import *
import importlib
from playerActions import *
import json
import os
#game settings
timeLimit = 60
movesPerSecond = 1

# number of y-units to move when falling
gravity = 1

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

#------------------Adding to player1 and player2 move scripts for test----
def setMoves(player1, player2):    
    p1movelist = ("teleport", 1), ("NoMove", None), ("uppercut", None)
    
    p2movelist = ("teleport", -1), ("move", (0,1)), ("NoMove", None)
    
    player1.moveList += p1movelist
    player2.moveList += p2movelist          

def updateCooldown(player):
    #TODO : once primary and secondary skills complete, add reduceCd
    
    player.lightAtk.reduceCd(1)
    player.heavyAtk.reduceCd(1)
    player.primarySkill.reduceCd(1)
    player.secondarySkill.reduceCd(1)

# updates current position of player if they are midair or started jumping
def updateMidair(player):
    if player.yCoord == player.jumpHeight:
        player.falling = True
        player.yCoord -= gravity
    # not yet at apex of jump
    elif player.midair:
        if player.falling: 
            player.yCoord -= gravity
        else:
            player.yCoord += 1
    if player.yCoord == 0: 
        player.midair = player.falling = False

def playerToJson(player, jsonDict):
    jsonDict['hp'].append(player.hp)
    jsonDict['xCoord'].append(player.xCoord)
    jsonDict['yCoord'].append(player.yCoord)
    #TODO coordinates and such
    jsonDict['state'].append(player.moves[-1][0])
    jsonDict['stun'].append(player.stun)
    jsonDict['midair'].append(player.midair)
    jsonDict['falling'].append(player.falling)
                

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
        
    # all actions have the signature
    # function(player1, player2, act1)
    # and return (knock1, stun1)

    # to specify an action,
    # define an action inside playerActions with the signature above,
    # and then add it to attack_actions or defense_actions (inside playerActions)

    # works under assumption of only 1 action per turn

    # for debug
    # if (act1 != "NoMove"):
    # print(act1, act2)
    
    # movement and defensive actions take priority then attacks and skills 
    if (act1[0] in defense_actions and not player1.stun):
        defense_actions[act1[0]](player1, player2, act1)
    if (act2[0] in defense_actions and not player2.stun):
        defense_actions[act2[0]](player2, player1, act2)

    if not player1.stun and act1[0] in attack_actions:
        knock1, stun1 = attack_actions[act1[0]](player1, player2, act1)
    if not player2.stun and act2[0] in attack_actions:
        knock2, stun2 = attack_actions[act2[0]](player2, player1, act2)

    return knock1, stun1, knock2, stun2
                
def startGame(path1, path2):
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    player1, player2 = setupGame(path1,path2)

    stun1 = stun2 = 0
    
    #TODO uncomment to set moves for both players
    setMoves(player1, player2)

    #TODO dont hard code path use the player names and use os for current path
    # * Check if file exists if so delete it 
    if(os.path.isfile("jsonfiles\p1.json")):
        os.remove("jsonfiles\p1.json")
    if(os.path.isfile("jsonfiles\p2.json")):
        os.remove("jsonfiles\p2.json")
        
    player1_json = open("jsonfiles\p1.json", "a")
    player2_json = open("jsonfiles\p2.json", "a")
    # structure the dict
    p1_json_dict = {
        'hp': [],
        'xCoord': [],
        'yCoord': [],
        'state': [],
        'stun': [],
        'midair': [],
        'falling':[]
        }
    p2_json_dict = {
        'hp': [],
        'xCoord': [],
        'yCoord': [],
        'state': [],
        'stun': [],
        'midair': [],
        'falling':[]
    }

    for tick in range(timeLimit *movesPerSecond):
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

        #playerInfo(player1, path1, act1)
        #playerInfo(player2, path2, act2)
            
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

        playerToJson(player1, p1_json_dict)
        playerToJson(player2,p2_json_dict)
    print(p1_json_dict)
    #TODO uncomment to dump data to json files
    json.dump(p1_json_dict, player1_json)
    json.dump(p2_json_dict, player2_json)
    
    player1_json.close()
    player2_json.close()

    if player1.hp == player2.hp:
        print('match won by: ', path1)
        return path1
    return max(player1.hp, player2.hp)

startGame("Player1", "Player2")
