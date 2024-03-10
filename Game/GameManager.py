import sys
from pathlib import Path
sys.path.append(str(Path("GameManager.py").parent))
from Game.test import *
import importlib

from Game.playerActions import defense_actions, attack_actions, projectile_actions, nullDef, nullAtk, nullProj
from Game.gameSettings import *
from Game.Skills import *
from Game.projectiles import *
import json
import os
from Game.turnUpdates import *



# import Submissions.finalpromoai1 as p1
# import Submissions.finalpromoai2 as p2

# import Submissions.Player1 as p1
# import Submissions.Player2 as p2
import pytest_tests.test_bots.DoNothingBot as p1
import pytest_tests.test_bots.DoNothingBot as p2
# import Submissions.Player5 as p1
# import Submissions.Player6 as p2
#import Submissions.Player4 as p2
# import Submissions.promotional_ai1 as p1
# import Submissions.promotional_ai2 as p2

# plays out one turn without checking deaths
def execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2):
    """
    Plays out one turn without checking death. \\
    Isolating so we can unit test.
    """
    knock1 = knock2 = 0
        
    #if midair, start falling/rising
    updateMidair(player1)
    updateMidair(player2)
    # post midair update correction
    correct_dir_pos(player1, player2, knock1, knock2)

    # uncomment to allow for smoother movement (doubles frames, need to find a way to do the same for projectiles)
    # if uncommented, length of projectile json would be half of player json
    #playerToJson(player1, p1_json_dict, True)
    #playerToJson(player2,p2_json_dict, True)
    print("PROJECTILES", projectiles)
    p1_projectiles = [proj["projectile"] for proj in projectiles if proj["projectile"]._player._id == 1]
    p2_projectiles = [proj["projectile"] for proj in projectiles if proj["projectile"]._player._id == 2]
    
    p1_move = p1_script.get_move(player1, player2, p1_projectiles, p2_projectiles)
    p2_move = p2_script.get_move(player2, player1, p2_projectiles, p1_projectiles)
    if not p1_move:
        p1_move = ("NoMove",)
    if not p2_move:
        p2_move = ("NoMove",)
    player1._inputs.append(p1_move)
    player2._inputs.append(p2_move)
    
    act1 = player1._action()
    act2 = player2._action()
                
    knock1, stun1, knock2, stun2, projectiles = performActions(player1, player2, 
                                        act1, act2, stun1, stun2, 
                                        projectiles)
    # post movement/attack position correction
    correct_dir_pos(player1, player2, knock1, knock2)
    
    if JSONFILL:
        playerToJson(player1, p1_json_dict, not JSONFILL)
        playerToJson(player2,p2_json_dict, not JSONFILL)
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
    # print(f"k1 {knock1}, k2 {knock2}")
    if knock1:
        player2._xCoord += knock1
        player2._stun = max(stun1, player2._stun)
    if knock2:
        player1._xCoord += knock2
        player1._stun = max(stun2, player1._stun)
        
    #print(f"P1: {player1.get_pos()}, P2: {player2.get_pos()}")
    # final position correction, if any, due to projectiles      
    correct_dir_pos(player1, player2, knock1, knock2)
        
    updateCooldown(player1)
    updateCooldown(player2)
    
    updateBuffs(player1)
    updateBuffs(player2)
    
    p1_dead = check_death(player1)
    p2_dead = check_death(player2)

    playerToJson(player1, p1_json_dict, fill=JSONFILL, checkHurt = JSONFILL)
    playerToJson(player2,p2_json_dict, fill=JSONFILL, checkHurt = JSONFILL)

    return projectiles, stun1, stun2, p1_dead, p2_dead

def setupGame(p1_script, p2_script):
    
    p1Import = importlib.import_module("Submissions.PlayerConfigs")
    p2Import = importlib.import_module("Submissions.PlayerConfigs")     
    player1 = p1Import.Player_Controller(LEFTSTART,0,50,GORIGHT, *p1_script.init_player_skills(), 1)
    player2 = p2Import.Player_Controller(RIGHTSTART,0,50,GOLEFT, *p2_script.init_player_skills(), 2)
    return player1,player2

#------------------Adding to player1 and player2 move scripts for test---------
# changes skills --  TODO finish
def swap_skills(player, new_prim, new_second):
    player._primarySkill = new_prim(player)
    player._secondarySkill = new_second(player)
    
def reset_block(player):
    player._block._regenShield()
    player._blocking = False
    
def performActions(player1, player2, act1, act2, stun1, stun2, projectiles):
    knock1 = knock2 = 0
    print(act1, act2)
    # empty move if player is currently stunned or doing recovery ticks
    if player1._stun or player1._recovery:
        act1 = ("NoMove", "NoMove")
        update_stun(player1)
    if player2._stun or player2._recovery:
        act2 = ("NoMove", "NoMove")
        update_stun(player2)
    
    
    if player1._midStartup or player1._skill_state:
        #print("p1 skill state")
        if player1._inputs[-1][0] in ("skill_cancel", "move", "block"):
            player1._skill_state = False
        else:
            act1 = player1._moves[-1]
            
    if player2._midStartup or player2._skill_state:
        #print("p2 skill state")
        if player2._inputs[-1][0] in ("skill_cancel", "move", "block"):
            player2._skill_state = False
        else:
            act2 = player2._moves[-1]
        print(act2)
        
    # exclusively for testing
    if act1[0] == "swap":
        swap_skills(player1, act1[1], act1[2])
        act1 = ("NoMove", "NoMove")
    if act2[0] == "swap":
        swap_skills(player2, act1[1], act1[2])
        act2 = ("NoMove", "NoMove")
    
    #print(act1, act2)
    # first check if a "no move" is input: 
    if act1[0] not in (attack_actions.keys() | defense_actions.keys() | projectile_actions.keys()):
        if player1._recovery:
            player1._moves.append(("recover", None))
            update_recovery(player1)
        else:
            player1._moves.append(("NoMove", "NoMove"))
        reset_block(player1)
        act1 = None
    if act2[0] not in (attack_actions.keys() | defense_actions.keys() | projectile_actions.keys()):
        if player2._recovery:
            player2._moves.append(("recover", None))
            update_recovery(player2)
        else:
            player2._moves.append(("NoMove", "NoMove"))
        reset_block(player2)
        act2 = None
    #print(act1, act2)
    # nullFunc, nullProj = default functions that return (0,0) or None with params
    # actions can only occur if the player is not stunned
    # if a defensive action is taken, it has priority over damage moves/skills
    # defensive = any skill that does not deal damage
    if act1:
        if act1[0] != "block":
            reset_block(player1)
        if defense_actions.get(act1[0], nullDef)(player1, player2, act1):
            act1 = None # prevent from going into attacks
    if act2:
        if act2[0] != "block":
            reset_block(player2)
        if defense_actions.get(act2[0], nullDef)(player2, player1, act2):
            act2 = None
        

    # then check if a damage dealing action is taken
    # if an attack lands, return knockback and stun caused by player
    # if projectile is created, add to projectile list
    print(act1, act2)
    if act1:
        knock1, stun1 = attack_actions.get(act1[0], nullAtk)(player1, player2, act1)
        proj_obj = projectile_actions.get(act1[0], nullProj)(player1, player2, act1)
        if proj_obj:
            projectiles.append(proj_obj)
        reset_block(player1)
    if act2:
        knock2, stun2 = attack_actions.get(act2[0], nullAtk)(player2, player1, act2)
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
    
    p1_script = p1.Script()
    p2_script = p2.Script()
    player1, player2 = setupGame(p1_script, p2_script)

    stun1 = stun2 = 0

    #setMoves(player1, player2)

    #TODO dont hard code path use the player names and use os for current path
    # * Check if file exists if so delete it 
    player_json = Path("jsonfiles/")
    if("p1.json" in player_json.glob('*.json')):
        player1_json = Path("jsonfiles/p1.json")
        print("found p1")
    if("p1.json" in player_json.glob('*.json')):
        player2_json = Path("jsonfiles/p2.json")
        print("foudn p2")
    player1_json = player_json / "p1.json"
    player2_json = player_json / "p2.json"
    player1_json.open("w")
    player2_json.open("w")
    # structure the dict
    p1_json_dict = {
        'hp': [],
        'xCoord': [],
        'yCoord': [],
        'state': [],
        'actionType': [],
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
        'actionType': [],
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
    
    # buffer turn : for smoothness
    for i in range(BUFFERTURNS):
        playerToJson(player1, p1_json_dict, fill=True, start=True)
        playerToJson(player2, p2_json_dict, fill=True, start=True)
        projectileToJson(None, p1_json_dict, False, fill=False)
        projectileToJson(None, p2_json_dict, False, fill=False)
        tick += 1
    #instantiate the player scripts
    while game_running:
        

        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, 
            player2, p1_script, p2_script, p1_json_dict, p2_json_dict, 
            projectiles, stun1, stun2)

        game_running = (not(p1_dead or p2_dead) and (tick < max_tick))
        tick += 1
        
    player1_json.write_text(json.dumps(p1_json_dict))
    player2_json.write_text(json.dumps(p2_json_dict))
        
    for key in p1_json_dict.keys():
        print(key)
        print(p1_json_dict[key])
    for key in p2_json_dict.keys():
        print(key)
        print(p2_json_dict[key])
    
    # for json checking purposes
    for json_key in p1_json_dict:
        if json_key != "ProjectileType":
            print(f"{json_key} : {len(p1_json_dict[json_key])}")
            
    for json_key in p2_json_dict:
        if json_key != "ProjectileType":
            print(f"{json_key} : {len(p2_json_dict[json_key])}")
    
    print(f"START BUFFERS: {BUFFERTURNS}, ACTUAL TURNS: {len(player1._inputs)}")
    print(f"jsonfill is {JSONFILL}")
    print("p1 HP:", player1._hp, " -- p2 HP:", player2._hp)
    if player1._hp > player2._hp:
        print(f"{path1} won in {tick} turns!")
        return path1
    elif player1._hp < player2._hp:
        print(f"{path2} won in {tick} turns!")
        return path2
    else:
        print('Tie!')
        return None

if __name__ == "__main__":
    startGame("p1", "p2")