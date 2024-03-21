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

# Manually choose bot files to test
SUBMISSIONPATH = "Submissions"
PATH1 = "MaxRangeHadokenBot"
PATH2 = "MeleeBot"


# Get scripts from bot files and return as script objects
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


# Checks for players moving into each other
def check_collision(player1, player2, knock1, knock2, checkMidair = False, stopVelo = False):
    if (correct_dir_pos(player1, player2, knock1, knock2)):
        # If an overlap occured, then a collision has occured, so set
        # horizontal midair velocity to 0
        player1._velocity = 0
        player2._velocity = 0
    elif checkMidair:
        # Check for midair players moving towards each other
        # If they end up face-to-face midair, set horizontal velocity to 0
        if ((player1._yCoord == player2._yCoord) and 
            (abs(player1._xCoord - player2._xCoord) == 1)
            and (player1._direction != player2._direction)):
            player1._velocity = 0
            player2._velocity = 0
            # Sets falling state to true for both players: Currently unused
            if stopVelo: 
                player1._airvelo = 0
                player2._airvelo = 0
                
# Plays out a single turn, doesn't check deaths
def execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2):
    # Initializing knockbacks: knock1 = knockback INFLICTED by player1 on player 2
    knock1 = knock2 = 0
    stun1 = stun2 = 0
    # If midair, start falling/rising and check if a collision occurs
    updateMidair(player1)
    check_collision(player1, player2, knock1, knock2)
    updateMidair(player2)
    check_collision(player1, player2, knock1, knock2)


    # Check for existing projectiles belonging to each player
    p1_projectiles = [proj["projectile"] for proj in projectiles if proj["projectile"]._player._id == 1]
    p2_projectiles = [proj["projectile"] for proj in projectiles if proj["projectile"]._player._id == 2]
    
    # Pass relevant information to player scripts, and get a move from them
    p1_move = p1_script.get_move(player1, player2, p1_projectiles, p2_projectiles)
    p2_move = p2_script.get_move(player2, player1, p2_projectiles, p1_projectiles)
  
    # In case the scripts return None
    if not p1_move:
        p1_move = ("NoMove",)
    if not p2_move:
        p2_move = ("NoMove",)
        
    # Add their move to their list of inputs
    player1._inputs.append(p1_move)
    player2._inputs.append(p2_move)
    
    # Get move from input list
    act1 = player1._action()
    act2 = player2._action()
    
    # Get game information from the result of the players performing their inputs
    knock1, stun1, knock2, stun2, projectiles = performActions(player1, player2, 
                                        act1, act2, stun1, stun2, 
                                        projectiles)
    # JSONFILL always True now...
    # Writes to json files the current actions, positions, hp etc...
    if JSONFILL:
        playerToJson(player1, p1_json_dict, not JSONFILL)
        playerToJson(player2,p2_json_dict, not JSONFILL)
        
    # Check if players move into each other, correct it if they do
    check_collision(player1, player2, knock1, knock2)
    
    # Make any currently existing projectiles move, and record them in json files
    projectiles, knock1, stun1, knock2, stun2 = projectile_move(projectiles, 
                            knock1, stun1, knock2, stun2, player1, player2,
                            p1_json_dict, p2_json_dict)

    print(knock1, knock2)
    # Only determine knockback and stun after attacks hit
    if (knock1 or stun1) and not player2._superarmor:
        player2._xCoord += knock1
        if not player2._stun:
            player2._stun = stun1
    if (knock2 or stun2) and not player1._superarmor:
        player1._xCoord += knock2
        if not player1._stun:
            player1._stun = stun2
        
    # Final position correction, if any, due to projectiles      
    check_collision(player1, player2, knock1, knock2, True, False)
        
    updateCooldown(player1)
    updateCooldown(player2)
    
    updateBuffs(player1)
    updateBuffs(player2)
    
    p1_dead = check_death(player1)
    p2_dead = check_death(player2)

    # Second write to json files, for any movement due to projectiles, and to 
    # check if a player got hurt
    playerToJson(player1, p1_json_dict, fill=JSONFILL, checkHurt = JSONFILL)
    playerToJson(player2,p2_json_dict, fill=JSONFILL, checkHurt = JSONFILL)

    return projectiles, stun1, stun2, p1_dead, p2_dead

def setupGame(p1_script, p2_script, leftstart=LEFTSTART, rightstart=RIGHTSTART):
    
    # Initializes player scripts as player controller objects
    player1 = Player_Controller(leftstart,0,HP,GORIGHT, *p1_script.init_player_skills(), 1)
    player2 = Player_Controller(rightstart,0,HP,GOLEFT, *p2_script.init_player_skills(), 2)
    # Ensure that valid primary and secondary skills are set
    assert(check_valid_skills(*p1_script.init_player_skills()))
    assert(check_valid_skills(*p2_script.init_player_skills()))
    return player1,player2

#ALERT: only for logic and animation testing, not for actual use
def swap_skills(player, new_prim, new_second):
    player._primarySkill = new_prim(player)
    player._secondarySkill = new_second(player)
    
# Resets player shield strength
def reset_block(player):
    player._block._regenShield()
    player._blocking = False
    
# Carries out player actions, return any resulting after effects to main loop  
def performActions(player1, player2, act1, act2, stun1, stun2, projectiles):
    knock1 = knock2 = 0

    # Empty move if player is currently stunned or doing recovery ticks
    if player1._stun or player1._recovery:
        act1 = ("NoMove", "NoMove")
        update_stun(player1)
    if player2._stun or player2._recovery:
        act2 = ("NoMove", "NoMove")
        update_stun(player2)
    
    # Checks if player does something to cancel a skill
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
    
    # Check if no valid move is input, or if the player is recovering 
    # If so, set act to None to prevent further checks
    print(act1, act2)
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

    # nullDef, nullAtk, nullProj = default functions that return (0,0) or None
    # actions can only occur if the player is not stunned
    # if a defensive action is taken, it has priority over damage moves/skills
    # defensive = any skill that does not deal damage
    
    # Movements are cached, and then carried out based on position 
    # If there are movements, set act to None to prevent going into attack check
    cached_move_1 = cached_move_2 = None
    if act1:
        if act1[0] != "block":
            reset_block(player1)
        cached_move_1 = defense_actions.get(act1[0], nullDef)(player1, player2, act1)
        if cached_move_1:
            act1 = None
    if act2:
        if act2[0] != "block":
            reset_block(player2)
        cached_move_2 = defense_actions.get(act2[0], nullDef)(player2, player1, act2)
        if cached_move_2:
            act2 = None

    # Prevent players that are directly facing each other from moving into each other
    if isinstance(cached_move_1, list) and isinstance(cached_move_2, list):
        if (check_move_collision(player1, player2, cached_move_1, cached_move_2) 
            and cached_move_1[1] == cached_move_2[1] and 
            abs(player1._xCoord - player2._xCoord) == 1):
            cached_move_1 = cached_move_2 = None
            player1._moves[-1] = ("NoMove", None)
            player2._moves[-1] = ("NoMove", None) 
    
    # Further checks for valid movement
    # Prevent horizontal movement if it would result in moving into a still player
    # Diagonal movements are allowed, since midair collision checks occur after
    if isinstance(cached_move_1, list):
        if player1._xCoord + cached_move_1[0] == player2._xCoord and cached_move_2 == [0,0] and not cached_move_1[1]:
            cached_move_1[0] = 0
        player1._xCoord += cached_move_1[0]
        player1._yCoord += cached_move_1[1]
        player1._moves[-1] = ("move", (cached_move_1[0]&player1._direction, cached_move_1[1]))
    if isinstance(cached_move_2, list):
        if player2._xCoord + cached_move_2[0] == player1._xCoord and cached_move_1 == [0,0] and not cached_move_1[1]:
            cached_move_2[0] = 0
        player2._xCoord += cached_move_2[0]
        player2._yCoord += cached_move_2[1]
        player2._moves[-1] = ("move", (cached_move_2[0]*player2._direction, cached_move_2[1]))
        
    # Prevent from going offscreen
    correctPos(player1)
    correctPos(player2)

    # Now check for damage dealing actions
    # Get any knockback and stun values if an attack lands
    # Summon projectiles if any projectile skills were casted
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

    # Correct positioning again just in case
    correctPos(player1)
    correctPos(player2)
    
    # Move to next move in player input list
    player1._moveNum += 1
    player2._moveNum += 1
    
    return knock1, stun1, knock2, stun2, projectiles

# Initializes json object 
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
                              
# Main game loop            
def startGame(path1, path2, submissionpath, roundNum):
    # Assert that paths are passed correctly
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    
    # Get bot files
    p1, p2 = get_player_files(path1, path2, submissionpath)
        
    # Initialize scripts and setup player positions and skills
    p1_script = p1.Script()
    p2_script = p2.Script()
    player1, player2 = setupGame(p1_script, p2_script)

    # Check if file exists if so delete it 
    player_json = Path("jsonfiles/")
    # create new battle file with player jsons
    new_battle = player_json / f"Round_{roundNum}"
    player1_json = new_battle / "p1.json"
    player2_json = new_battle / "p2.json"
    # create round result file
    round_results_json = new_battle / "round.json"
    # get list of battles 
    files = player_json.glob("*")
    battles = [x for x in files if x.is_dir()]   
    # check if this battle has not happened before
    if f"Round {roundNum}" not in battles:
        player1_json.parent.mkdir(parents=True, exist_ok=True)
        player2_json.parent.mkdir(parents=True, exist_ok=True)
        round_results_json.parent.mkdir(parents=True, exist_ok=True)
        
    player1_json.open("w")
    player2_json.open("w")
    round_results_json.open("w")
    # structure the dict, no need to structure round result dict until the end
    p1_json_dict = get_empty_json()
    p2_json_dict = get_empty_json()
    
    # Initialize variables
    projectiles = []
    stun1 = stun2 = 0
    tick = 0
    max_tick = timeLimit * movesPerSecond
    game_running = True
    
    # Buffer turn : for smoothness
    for i in range(BUFFERTURNS * 2): # 2 since fill ticks
        playerToJson(player1, p1_json_dict, fill=True, start=True)
        playerToJson(player2, p2_json_dict, fill=True, start=True)
        projectileToJson(None, p1_json_dict, False, fill=True)
        projectileToJson(None, p2_json_dict, False, fill=True)
        tick += 1
        max_tick += 1
        
    # Loops through turns
    while game_running:
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, 
            player2, p1_script, p2_script, p1_json_dict, p2_json_dict, 
            projectiles, stun1, stun2)
        # Ends game if a player dies or if time up
        game_running = (not(p1_dead or p2_dead) and (tick < max_tick))
        tick += 1
    
    # Write into json files
    player1_json.write_text(json.dumps(p1_json_dict))
    player2_json.write_text(json.dumps(p2_json_dict))
    
    # For testing
    for key in p1_json_dict.keys():
        print(key)
        print(p1_json_dict[key])
    for key in p2_json_dict.keys():
        print(key)
        print(p2_json_dict[key])

    for json_key in p1_json_dict:
        if json_key != "ProjectileType":
            print(f"{json_key} : {len(p1_json_dict[json_key])}")
            
    for json_key in p2_json_dict:
        if json_key != "ProjectileType":
            print(f"{json_key} : {len(p2_json_dict[json_key])}")
            
    print(f"START BUFFERS: {BUFFERTURNS}, ACTUAL TURNS: {len(player1._inputs)}")
    print(f"jsonfill is {JSONFILL}")
    print(f"{path1} HP: {player1._hp} --  {path2} HP: {player2._hp}")
    
    winner = None
    if player1._hp > player2._hp:
        print(f"{path1} won in {tick} turns!")
        winner = path1
    elif player1._hp < player2._hp:
        print(f"{path2} won in {tick} turns!")
        winner = path2
    else:
        print('Tie!')
    
    # create round info json dictionary
    round_info = {'p1': path1, 'p2':path2, 'winner':winner, 'roundNum':roundNum}
    round_results_json.write_text(json.dumps(round_info))
    
    return winner
    
    # todo add txt file for round info

if __name__ == "__main__":
    startGame(PATH1, PATH2, SUBMISSIONPATH, 0)