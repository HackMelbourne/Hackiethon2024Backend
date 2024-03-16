import sys
from pathlib import Path
import importlib
import json
sys.path.append(str(Path("GameManager.py").parent))

from Game.test import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions, nullDef, nullAtk, nullProj
from Game.gameSettings import *
from Game.Skills import *
from Game.projectiles import *
from Game.turnUpdates import *
from Game.PlayerConfigs import Player_Controller

# SUBMISSIONPATH = "Submissions/"
# PATH1 = "Player1"
# PATH2 = "Player2"

SUBMISSIONPATH = "pytest_tests/test_bots"

PATH1 = "HadokenOnceBot"
PATH2 = "JumpBot"
#PATH1 = "Player1"
#PATH2 = "Player2"

def get_player_files(path1, path2, subpath):
    submissionFiles = Path(subpath)
    p1module = submissionFiles / (path1 + ".py")
    p2module = submissionFiles / (path2 + ".py")
    p = submissionFiles.glob("*")
    print([x for x in p if x.is_file()])
    if p1module.is_file() and p2module.is_file():
        subpath = subpath.replace('\\', '.')
        subpath = subpath.replace('/', '.')
        p1 = importlib.import_module(subpath + "." + path1)
        p2 = importlib.import_module(subpath+ "." + path2)
        return p1, p2
    else:
        raise Exception("A file does not exist in " + subpath)
    
def check_collision(player1, player2, knock1, knock2, checkMidair = False, stopVelo = False):
    # post midair update correction
    if (correct_dir_pos(player1, player2, knock1, knock2)):
        # player collision occured
        player1._velocity = 0
        #player1._airvelo = 0
        player2._velocity = 0
        #player2._airvelo = 0  
    elif checkMidair:
        # check for midair moving towards each other
        # midair, distance 1, velocity = direction
        if ((player1._yCoord == player2._yCoord) and 
            (abs(player1._xCoord - player2._xCoord) == 1)
            and (player1._direction != player2._direction)):
            # for sure
            player1._velocity = 0
            player2._velocity = 0
            if stopVelo: 
                player1._airvelo = 0
                player2._airvelo = 0
                
# plays out one turn without checking deaths
def execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2):
    """
    Plays out one turn without checking death.
    Isolating so we can unit test.
    """
    knock1 = knock2 = 0
    print(projectiles)

    #if midair, start falling/rising, and check if midair movement causes a collision
    updateMidair(player1)
    check_collision(player1, player2, knock1, knock2)
    updateMidair(player2)
    check_collision(player1, player2, knock1, knock2)
 
    #print(f"Post midair movement: P1: {player1.get_pos()}, P2: {player2.get_pos()}")
    # uncomment to allow for smoother movement (doubles frames, need to find a way to do the same for projectiles)
    # if uncommented, length of projectile json would be half of player json
    #playerToJson(player1, p1_json_dict, True)
    #playerToJson(player2,p2_json_dict, True)

    p1_projectiles = [proj["projectile"] for proj in projectiles if proj["projectile"]._player._id == 1]
    p2_projectiles = [proj["projectile"] for proj in projectiles if proj["projectile"]._player._id == 2]
    
    p1_move = p1_script.get_move(player1, player2, p1_projectiles, p2_projectiles)
    p2_move = p2_script.get_move(player2, player1, p2_projectiles, p1_projectiles)
    
    print(p1_move, p2_move)
    if not p1_move:
        p1_move = ("NoMove",)
    if not p2_move:
        p2_move = ("NoMove",)
    player1._inputs.append(p1_move)
    player2._inputs.append(p2_move)
    
    act1 = player1._action()
    act2 = player2._action()
    
    #print(f"Pre action HP:  P1: {player1._hp}, P2: {player2._hp}")
    knock1, stun1, knock2, stun2, projectiles = performActions(player1, player2, 
                                        act1, act2, stun1, stun2, 
                                        projectiles)
    #print("Post action, pre fill tick")
    #print(f"P1: {player1.get_pos(), player1._hp}, P2: {player2.get_pos(), player2._hp}")
    
    if JSONFILL:
        playerToJson(player1, p1_json_dict, not JSONFILL)
        playerToJson(player2,p2_json_dict, not JSONFILL)
        
    # post movement/attack position correction
    # this is after JSONFLL bcs movement of player into each other must still 
    # be recorded
    check_collision(player1, player2, knock1, knock2)
    # if there are projectiles, make them travel
    projectiles, knock1, stun1, knock2, stun2 = projectile_move(projectiles, 
                            knock1, stun1, knock2, stun2, player1, player2,
                            p1_json_dict, p2_json_dict)
    
    #print("Post action, post collision/proj check")
    #print(f"P1: {player1.get_pos(), player1._hp}, P2: {player2.get_pos(), player2._hp}")
    #only determine knockback and stun after attacks hit
    #knock1 and stun1 = knockback and stun inflicted by player1 on player2
    if knock1 and not player2._superarmor:
        player2._xCoord += knock1
        player2._stun = max(stun1, player2._stun)
    if knock2 and not player1._superarmor:
        player1._xCoord += knock2
        player1._stun = max(stun2, player1._stun)
        
    # final position correction, if any, due to projectiles      
    check_collision(player1, player2, knock1, knock2, True, False)
        
    updateCooldown(player1)
    updateCooldown(player2)
    
    updateBuffs(player1)
    updateBuffs(player2)
    
    p1_dead = check_death(player1)
    p2_dead = check_death(player2)

    #print("Post action, post tick fill")
    #print(f"P1: {player1.get_pos(), player1._hp}, P2: {player2.get_pos(), player2._hp}")
    playerToJson(player1, p1_json_dict, fill=JSONFILL, checkHurt = JSONFILL)
    playerToJson(player2,p2_json_dict, fill=JSONFILL, checkHurt = JSONFILL)

    return projectiles, stun1, stun2, p1_dead, p2_dead

def setupGame(p1_script, p2_script, leftstart=LEFTSTART, rightstart=RIGHTSTART):
   
    player1 = Player_Controller(leftstart,0,50,GORIGHT, *p1_script.init_player_skills(), 1)
    player2 = Player_Controller(rightstart,0,50,GOLEFT, *p2_script.init_player_skills(), 2)
    # check if correct primary and secondary skills
    assert(check_valid_skills(*p1_script.init_player_skills()))
    assert(check_valid_skills(*p2_script.init_player_skills()))
    return player1,player2

#------------------Adding to player1 and player2 move scripts for test---------
#ALERT: only for logic and animation testing, not for actual use
def swap_skills(player, new_prim, new_second):
    player._primarySkill = new_prim(player)
    player._secondarySkill = new_second(player)
    
# resets player shield strength
def reset_block(player):
    player._block._regenShield()
    player._blocking = False
    
# carries out player actions, return any resulting after effects to main loop  
def performActions(player1, player2, act1, act2, stun1, stun2, projectiles):
    knock1 = knock2 = 0
    # empty move if player is currently stunned or doing recovery ticks
    print(f"P1 input: {act1}, P2 input: {act2}")
    if player1._stun or player1._recovery:
        act1 = ("NoMove", "NoMove")
        update_stun(player1)
    if player2._stun or player2._recovery:
        act2 = ("NoMove", "NoMove")
        update_stun(player2)
    
    if player1._midStartup or player1._skill_state:
        if player1._inputs[-1][0] in ("skill_cancel", "move", "block"):
            player1._skill_state = False
            player1._midStartup = False
        else:
            act1 = player1._moves[-1]
            
    if player2._midStartup or player2._skill_state:
        if player2._inputs[-1][0] in ("skill_cancel", "move", "block"):
            player2._skill_state = False
            player2._midStartup = False
        else:
            act2 = player2._moves[-1]
        
    # exclusively for testing
    if act1[0] == "swap":
        swap_skills(player1, act1[1], act1[2])
        act1 = ("NoMove", "NoMove")
    if act2[0] == "swap":
        swap_skills(player2, act1[1], act1[2])
        act2 = ("NoMove", "NoMove")
    
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

    # nullFunc, nullProj = default functions that return (0,0) or None with params
    # actions can only occur if the player is not stunned
    # if a defensive action is taken, it has priority over damage moves/skills
    # defensive = any skill that does not deal damage
    cached_move_1 = cached_move_2 = None
    if act1:
        if act1[0] != "block":
            reset_block(player1)
        cached_move_1 = defense_actions.get(act1[0], nullDef)(player1, player2, act1)
        if cached_move_1:
            print(f"P1 move: {act1}")
            act1 = None # prevent from going into attacks
    if act2:
        if act2[0] != "block":
            reset_block(player2)
        cached_move_2 = defense_actions.get(act2[0], nullDef)(player2, player1, act2)
        if cached_move_2:
            print(f"P2 move: {act2}")
            act2 = None

    # check if they would move into each other
    if isinstance(cached_move_1, list) and isinstance(cached_move_2, list):
        # if right in front of each other and moving exactly towards each other
        if (check_move_collision(player1, player2, cached_move_1, cached_move_2) 
            and cached_move_1[1] == cached_move_2[1] and 
            abs(player1._xCoord - player2._xCoord) == 1):
            cached_move_1 = cached_move_2 = None
            player1._moves[-1] = ("NoMove", None)
            player2._moves[-1] = ("NoMove", None) 
    if isinstance(cached_move_1, list):
        # this is a movement
        if player1._xCoord + cached_move_1[0] == player2._xCoord and cached_move_2 == [0,0]:
            cached_move_1[0] = 0
        player1._xCoord += cached_move_1[0]
        player1._yCoord += cached_move_1[1]
    if isinstance(cached_move_2, list):
        # this is a movement
        print(player2._xCoord + cached_move_2[0] == player1._xCoord)
        print(cached_move_1)
        if player2._xCoord + cached_move_2[0] == player1._xCoord and cached_move_1 == [0,0]:
            cached_move_2[0] = 0
        player2._xCoord += cached_move_2[0]
        player2._yCoord += cached_move_2[1]
        
    correctPos(player1)
    correctPos(player2)
    # then check if a damage dealing action is taken
    # if an attack lands, return knockback and stun caused by player
    # if projectile is created, add to projectile list


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

    correctPos(player1)
    correctPos(player2)
    
    player1._moveNum += 1
    player2._moveNum += 1
    
    if act1:
        print(f"P1 move {act1}")
    if act2:
        print(f"P2 move {act2}")
    return knock1, stun1, knock2, stun2, projectiles

def get_empty_json():
    return {
        'hp': [],
        'xCoord': [],
        'yCoord': [],
        'state': [],
        'actionType': [],
        'stun': [],
        'midair': [],
        'falling':[],
        'direction':[],
        'ProjectileType': None,
        'projXCoord':[],
        'projYCoord':[]
    }
                                          
def startGame(path1, path2, submissionpath, roundNum):
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    
    p1, p2 = get_player_files(path1, path2, submissionpath)
        
    p1_script = p1.Script()
    p2_script = p2.Script()
    player1, player2 = setupGame(p1_script, p2_script)

    stun1 = stun2 = 0

    # Check if file exists if so delete it 
    player_json = Path("jsonfiles/")
    # check for battle json
    p1vp2 = f"{path1} vs {path2}"
    p2vp1 = f"{path2} vs {path1}"
    # create new battle file with player jsons
    new_battle = player_json / f"Round {roundNum}"
    player1_json = new_battle / "p1.json"
    player2_json = new_battle / "p2.json"
    # get list of battles 
    files = player_json.glob("*")
    battles = [x for x in files if x.is_dir()]   
    # check if this battle has not happened before
    if f"Round {roundNum}" not in battles:
        player1_json.parent.mkdir(parents=True, exist_ok=True)
        player2_json.parent.mkdir(parents=True, exist_ok=True)
        
    player1_json.open("w")
    player2_json.open("w")
    # structure the dict
    p1_json_dict = get_empty_json()
    p2_json_dict = get_empty_json()
    
    projectiles = []
    tick = 0
    max_tick = timeLimit * movesPerSecond
    game_running = True
    
    # buffer turn : for smoothness
    for i in range(BUFFERTURNS * 2): # 2 since fill ticks
        playerToJson(player1, p1_json_dict, fill=True, start=True)
        playerToJson(player2, p2_json_dict, fill=True, start=True)
        projectileToJson(None, p1_json_dict, False, fill=True)
        projectileToJson(None, p2_json_dict, False, fill=True)
        tick += 1
        max_tick += 1
        
    print(p1_json_dict)
    print(p2_json_dict)
        
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
    print(f"{path1} HP: {player1._hp} --  {path2} HP: {player2._hp}")
    
    if player1._hp > player2._hp:
        print(f"{path1} won in {tick} turns!")
        return path1
    elif player1._hp < player2._hp:
        print(f"{path2} won in {tick} turns!")
        return path2
    else:
        print('Tie!')
        return None
    
    # todo add txt file for round info

if __name__ == "__main__":
    startGame(PATH1, PATH2, SUBMISSIONPATH, 0)