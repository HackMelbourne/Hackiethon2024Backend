import random
from test import *
import importlib
from playerActions import *
from Skills import *
import json
import os
#game settings
timeLimit = 10
movesPerSecond = 1

# number of y-units to move when falling
gravity = 1

#direction constants

GORIGHT = 1
GOLEFT = -1

#player variables

def setupGame():
    
    p1Import = importlib.import_module("Submissions.PlayerConfigs")
    p2Import = importlib.import_module("Submissions.PlayerConfigs")
    player1 = p1Import.Player_Controller(1,0,50,GORIGHT, Boomerang, UppercutSkill, 1)
    player2 = p2Import.Player_Controller(4,0,50,GOLEFT, TeleportSkill, UppercutSkill, 2)
    return player1,player2

#------------------Adding to player1 and player2 move scripts for test----
def setMoves(player1, player2):    
    p1movelist = ("NoMove", None), ("boomerang", )
    
    p2movelist = ("NoMove", None), ("move", (0, 1))
    
    player1._inputs += p1movelist
    player2._inputs += p2movelist          

def updateCooldown(player):
    player._lightAtk.reduceCd(1)
    player._heavyAtk.reduceCd(1)
    player._primarySkill.reduceCd(1)
    player._secondarySkill.reduceCd(1)
    
# updates current position of player if they are midair or started jumping
def updateMidair(player):
    if player._yCoord == player._jumpHeight:
        player._falling = True
        player._yCoord -= gravity
        player._xCoord += player._velocity
    # not yet at apex of jump
    elif player._midair:
        if player._falling: 
            player._yCoord -= gravity
        else:
            player._yCoord += 1
        player._xCoord += player._velocity
        
    if player._yCoord == 0 and player._falling: 
        player._midair = player._falling = False
        player._velocity = 0
        
    correctPos(player)

def playerToJson(player, jsonDict):
    jsonDict['hp'].append(player._hp)
    jsonDict['xCoord'].append(player._xCoord)
    jsonDict['yCoord'].append(player._yCoord)
    jsonDict['state'].append(player._moves[-1][0])
    jsonDict['stun'].append(player._stun)
    jsonDict['midair'].append(player._midair)
    jsonDict['falling'].append(player._falling)

def projectileToJson(projectile, jsonDict, travelling):
    if travelling:
        jsonDict['ProjectileType'] = projectile.type
        jsonDict['projXCoord'].append(projectile.xCoord)
        jsonDict['projYCoord'].append(projectile.yCoord)
    else:
        jsonDict['projXCoord'].append(None)
        jsonDict['projYCoord'].append(None)    
                

def performActions(player1, player2, act1, act2, stun1, stun2, projectiles):
    knock1 = knock2 = 0

    if player1._stun:
        player1._stun -= 1
    if player2._stun:
        player2._stun -= 1

        
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
    if act1 in ("NoMove", ("NoMove", None)):
        player1._moves.append(("NoMove", None))
    if act2 in ("NoMove", ("NoMove", None)):
        player2._moves.append(("NoMove", None))
        
    if (act1[0] in defense_actions and not player1._stun):
        defense_actions[act1[0]](player1, player2, act1)
    if (act2[0] in defense_actions and not player2._stun):
        defense_actions[act2[0]](player2, player1, act2)

    if not player1._stun and act1[0] in attack_actions:
        knock1, stun1 = attack_actions[act1[0]](player1, player2, act1)
    if not player2._stun and act2[0] in attack_actions:
        knock2, stun2 = attack_actions[act2[0]](player2, player1, act2)
        
    if not player1._stun and act1[0] in projectile_actions:
        projectiles.append(projectile_actions[act1[0]](player1, player2, act1))
    if not player2._stun and act2[0] in projectile_actions:
        projectiles.append(projectile_actions[act2[0]](player2, player1, act2))
        
    player1._moveNum += 1
    player2._moveNum += 1
    
    return knock1, stun1, knock2, stun2
                
                
def projectile_move(projectiles, knock1, stun1, knock2, stun2, player1, player2,
                    p1_dict, p2_dict):
    for projectileNum in range(len(projectiles)):
        
        proj_info = projectiles[projectileNum]
        proj_obj = proj_info["projectile"]
        print(f"PROJ {proj_obj.xCoord, proj_obj.yCoord}")

        # first check if the projectile already travelled its range or offscreen
        if proj_obj.size == (0,0):
            # remove projectile from array
            projectiles.pop(projectileNum)
            continue
        
        # check for projectiles colliding with each other
        for nextProjNum in range(len(projectiles)):
            nextproj_obj = projectiles[nextProjNum]["projectile"]
            if (nextProjNum != projectileNum and 
                proj_obj.checkProjCollision(nextproj_obj)):
                    projectiles.pop(projectileNum)
                    projectiles.pop(nextproj_obj)
                    break
        
        # list of ids of projectiles currently on screen
        projectile_ids = [projectile_obj["projectile"].id for projectile_obj in projectiles]
        # check if this projectile still exists
        if proj_obj.id in projectile_ids:
            # get projectile info and initialise
            proj_info = projectiles[projectileNum]
            proj_knock1 = proj_knock2 = proj_stun1 = proj_stun2 = 0
            
            # collision checks and attack checks
            if proj_obj.checkCollision(player1):
                proj_knock2, proj_stun2 = attackHit(proj_obj, player1,
                                                proj_info["damage"],
                                                proj_obj.size[0],
                                                proj_obj.size[1],
                                                proj_info["blockable"],
                                                proj_info["knockback"],
                                                proj_info["stun"])
            if proj_obj.checkCollision(player2):
                proj_knock1, proj_stun1 = attackHit(proj_obj, player2,
                                                proj_info["damage"],
                                                proj_obj.size[0],
                                                proj_obj.size[1],
                                                proj_info["blockable"],
                                                proj_info["knockback"],
                                                proj_info["stun"])
            # if attack and projectile hits target at same time, use
            # total knockback and highest stun
            knock1 += proj_knock1
            stun1 = max(stun1, proj_stun1)
            knock2 += proj_knock2
            stun2 = max(stun2, proj_stun2)
                
            if proj_obj.player._id == 1:
                proj_json_dict = p1_dict
            else:
                proj_json_dict = p2_dict
            
            # then pop the projectile if it hit anyone, else continue travel
            if proj_knock1 or proj_knock2:
                projectileToJson(proj_obj, proj_json_dict, False)
                projectiles.pop(projectileNum)
            else:
                projectileToJson(proj_obj, proj_json_dict, True)
                proj_obj.travel()
                    
    return projectiles, knock1, stun1, knock2, stun2    

def startGame(path1, path2):
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    player1, player2 = setupGame()

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
        'falling':[],
        'ProjectileType': None,
        'projXCoord':[],
        'projYCoord':[]
        }
    p2_json_dict = {
        'hp': [],
        'xCoord': [],
        'yCoord': [],
        'state': [],
        'stun': [],
        'midair': [],
        'falling':[],
        'ProjectileType': None,
        'projXCoord':[],
        'projYCoord':[]
    }
    projectiles = []
    
    
    for tick in range(timeLimit *movesPerSecond):
        #flips orientation if player jumps over each other
        if flip_orientation(player1, player2):
            player1.direction = GOLEFT
            player2.direction = GORIGHT
        else:
            player1.direction = GORIGHT
            player2.direction = GOLEFT
        
        knock1 = knock2 = 0
        
        act1 = player1._action()
        act2 = player2._action()
        
        playerInfo(player1, path1, act1)
        playerInfo(player2, path2, act2)
        
        knock1, stun1, knock2, stun2 = performActions(player1, player2, 
                                                      act1, act2, stun1, stun2, 
                                                      projectiles)
        # if there are projectiles, make them travel
        projectiles, knock1, stun1, knock2, stun2 = projectile_move(projectiles, 
                                knock1, stun1, knock2, stun2, player1, player2,
                                p1_json_dict, p2_json_dict)
        
        #only determine knockback and stun after attacks hit
        #knock1 and stun1 = knockback and stun inflicted by player1
        if knock1:
            player2._xCoord += knock1
            player2._stun += stun1
        if knock2:
            player1._xCoord += knock2
            player1._stun += stun2
            
        #if midair, start falling/rising
        updateMidair(player1)
        updateMidair(player2)

        updateCooldown(player1)
        updateCooldown(player2)
        
        #TODO update current startup every tick 

        playerToJson(player1, p1_json_dict)
        playerToJson(player2,p2_json_dict)
    #print(p1_json_dict)
    #TODO uncomment to dump data to json files
    json.dump(p1_json_dict, player1_json)
    json.dump(p2_json_dict, player2_json)
    
    player1_json.close()
    player2_json.close()

    print(player1._moves)
    print(player1._inputs)
    print(p1_json_dict)
    if player1._hp == player2._hp:
        print('match won by: ', path1)
        return path1
    return max(player1._hp, player2._hp)

startGame("a", "b")
