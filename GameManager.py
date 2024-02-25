import test
import importlib
from playerActions import defense_actions, attack_actions, projectile_actions, nullFunc, nullProj
from Skills import *
from projectiles import *
import json
import os
from turnUpdates import *
import Submissions.Player5 as p1
import Submissions.Player3 as p2
#game settings
timeLimit = 30
movesPerSecond = 1

#direction constants
GORIGHT = 1
GOLEFT = -1

#player variables

def setupGame():
    
    p1Import = importlib.import_module("Submissions.PlayerConfigs")
    p2Import = importlib.import_module("Submissions.PlayerConfigs")     
    player1 = p1Import.Player_Controller(4,0,50,GORIGHT, *p1.init_player_skills(), 1)
    player2 = p2Import.Player_Controller(7,0,50,GOLEFT, *p2.init_player_skills(), 2)
    return player1,player2

#------------------Adding to player1 and player2 move scripts for test---------
# no longer needed, add moves to player1.py and player2.py
def setMoves(player1, player2):    
    p1movelist = ("light", ), ("heavy", ), ("onepunch",), ("uppercut", ), ("move", (1,0)), ("move", (0,1)), ("move", (1,1)), ("block",), ("block",),
    p2movelist = None,
    
    player1._inputs += p1movelist
    player2._inputs += p2movelist          
    
def reset_block(player):
    player._block._regenShield()
    player._blocking = False
    
def performActions(player1, player2, act1, act2, stun1, stun2, projectiles):
    knock1 = knock2 = 0

    # empty move if player is currently stunned or doing recovery ticks
    if player1._stun or player1._recovery:
        act1 = ("NoMove", None)
        update_stun(player1)
        update_recovery(player1)
    if player2._stun or player2._recovery:
        act2 = ("NoMove", None)
        update_stun(player2)
        update_recovery(player2)
    
    if player1._midStartup or player1._skill_state:
        if player1._inputs[-1][0] == "skill_cancel":
            act1 = ("NoMove", None)
        else:
            act1 = player1._moves[-1]
            
    if player2._midStartup or player2._skill_state:
        if player2._inputs[-1][0] == "skill_cancel":
            act2 = ("NoMove", None)
        else:
            act2 = player2._moves[-1]
            
    # first check if a "no move" is input: 
    if act1[0] not in (attack_actions.keys() | defense_actions.keys() | projectile_actions.keys()):
        player1._moves.append(("NoMove", None))
        reset_block(player1)
        act1 = None
    if act2[0] not in (attack_actions.keys() | defense_actions.keys() | projectile_actions.keys()):
        player2._moves.append(("NoMove", None))
        reset_block(player2)
        act2 = None
        
    # nullFunc, nullProj = default functions that return (0,0) or None with params
    # actions can only occur if the player is not stunned
    # if a defensive action is taken, it has priority over damage moves/skills
    # defensive = any skill that does not deal damage
    if act1:
        if act1[0] != "block":
            reset_block(player1)
        defense_actions.get(act1[0], nullFunc)(player1, player2, act1)
    if act2:
        if act2[0] != "block":
            reset_block(player2)
        defense_actions.get(act2[0], nullFunc)(player2, player1, act2)

    # then check if a damage dealing action is taken
    # if an attack lands, return knockback and stun caused by player
    # if projectile is created, add to projectile list
    if act1:
        knock1, stun1 = attack_actions.get(act1[0], nullFunc)(player1, player2, act1)
        proj_obj = projectile_actions.get(act1[0], nullProj)(player1, player2, act1)
        if proj_obj:
            projectiles.append(proj_obj)
        reset_block(player1)
    if act2:
        knock2, stun2 = attack_actions.get(act2[0], nullFunc)(player2, player1, act2)
        proj_obj = projectile_actions.get(act2[0], nullProj)(player2, player1, act2)
        if proj_obj:
            projectiles.append(proj_obj)
        reset_block(player2)
    
     
    player1._moveNum += 1
    player2._moveNum += 1
    
    return knock1, stun1, knock2, stun2, projectiles
                                        
def startGame(path1, path2):
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    player1, player2 = setupGame()

    stun1 = stun2 = 0

    #setMoves(player1, player2)

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
    
    tick = 0
    max_tick = timeLimit * movesPerSecond
    game_running = True
    
    while game_running:
        #flips orientation if player jumps over each other
        if test.flip_orientation(player1, player2):
            player1.direction = GOLEFT
            player2.direction = GORIGHT
        else:
            player1.direction = GORIGHT
            player2.direction = GOLEFT
        
        knock1 = knock2 = 0
        
        p1_projectiles = [proj["projectile"] for proj in projectiles if proj["projectile"]._player._id == 1]
        p2_projectiles = [proj["projectile"] for proj in projectiles if proj["projectile"]._player._id == 2]
        
        player1._inputs.append(p1.get_move(player1, player2, p1_projectiles, p2_projectiles))
        player2._inputs.append(p2.get_move(player2, player1, p2_projectiles, p1_projectiles))
        
        act1 = player1._action()
        act2 = player2._action()
                    
        knock1, stun1, knock2, stun2, projectiles = performActions(player1, player2, 
                                            act1, act2, stun1, stun2, 
                                            projectiles)
        
        #print(f"Inputs: {player1._moveNum}, {player1._inputs}")
        #print(f"Moves : {len(player1._moves)}, {player1._moves}")
        #print("After movement:")
        #test.playerInfo(player1, path1, act1)
        #test.playerInfo(player2, path2, act2)
        # if there are projectiles, make them travel
        projectiles, knock1, stun1, knock2, stun2 = projectile_move(projectiles, 
                                knock1, stun1, knock2, stun2, player1, player2,
                                p1_json_dict, p2_json_dict)
        
        
        #only determine knockback and stun after attacks hit
        #knock1 and stun1 = knockback and stun inflicted by player1 on player2
        if knock1:
            player2._xCoord += knock1
            player2._stun = max(stun1, player2._stun)
        if knock2:
            player1._xCoord += knock2
            player1._stun = max(stun2, player1._stun)
            
        #if midair, start falling/rising
        updateMidair(player1)
        updateMidair(player2)

        # correct player positions if off screen/under ground
        test.correctPos(player1)
        test.correctPos(player2)
        
        test.correctOverlap(player1, player2, knock1, knock2)
        
        #print("After all projectile movement:")
        test.playerInfo(player1, path1, act1)
        print(player1._moves[-1])
        test.playerInfo(player2, path2, act2)
        print(player2._moves[-1])
        #print(player1._moves[-1], player1._moveNum)
            
        updateCooldown(player1)
        updateCooldown(player2)
        
        updateBuffs(player1)
        updateBuffs(player2)
        
        p1_dead = check_death(player1)
        p2_dead = check_death(player2)
        game_running = (not(p1_dead or p2_dead) and (tick < max_tick))
        tick += 1
        
        playerToJson(player1, p1_json_dict)
        playerToJson(player2,p2_json_dict)
        
        
    json.dump(p1_json_dict, player1_json)
    json.dump(p2_json_dict, player2_json)
        
    player1_json.close()
    player2_json.close()

    print(p1_json_dict)
    print(p2_json_dict)
    
    # for json checking purposes
    for json_key in p1_json_dict:
        if json_key != "ProjectileType":
            print(f"{json_key} : {len(p1_json_dict[json_key])}")
            
    for json_key in p2_json_dict:
        if json_key != "ProjectileType":
            print(f"{json_key} : {len(p2_json_dict[json_key])}")
    
    print(len(player1._inputs))
    if player1._hp > player2._hp:
        print(f"{path1} won in {tick} turns!")
        return path1
    elif player1._hp < player2._hp:
        print(f"{path2} won in {tick} turns!")
        return path2
    else:
        print('Tie!')
        return None

startGame("p1", "p2")