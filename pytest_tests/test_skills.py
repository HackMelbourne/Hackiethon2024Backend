from pprint import pprint
import sys
from pathlib import Path
from Game.GameManager import execute_one_turn

sys.path.append(str(Path("test_basics.py").parent.parent))

# from GameManager import execute_one_turn, setupGame'
from ScriptingHelp.usefulFunctions import *
from pytest_tests.helpers import init_game, artificially_move_player
from Game.gameSettings import *
from Game.test import *
from Game.playerActions import *
from Game.turnUpdates import playerToJson
import pytest_tests.test_bots.JumpBot as jump_bot
import pytest_tests.test_bots.OnePunchCancelBot as one_punch_cancel_bot # walks forward once, then heavy's, then cancels
import pytest_tests.test_bots.DoNothingBot as nothing_bot
import pytest_tests.test_bots.TeleportOnceBot as teleport_once_bot
import pytest_tests.test_bots.DashAttackOnceBot as dash_attack_once_bot
import pytest_tests.test_bots.SuperSaiyanAttackBot as super_saiyan_attack_bot
import pytest_tests.test_bots.UppercutOnceBot as uppercut_once_bot
import pytest_tests.test_bots.BlockOnceBot as block_once_bot
import pytest_tests.test_bots.PermaBlockBot as perma_block_bot
import pytest_tests.test_bots.MeditateOnceBot as meditate_once_bot
import pytest_tests.test_bots.PermaMeditateBot as perma_meditate_bot

def test_skill_cancel():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(one_punch_cancel_bot, nothing_bot, 6, 8)
    
    assert p1_json_dict['xCoord'][-1] == 6
    assert p2_json_dict['xCoord'][-1] == 8

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    # assumptions: heavy has startup of 1
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [6, 7, 7, 7, 7, 7, 7]
    assert p2_json_dict['xCoord'][-n:] == [8] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'heavy', 'heavy', 'skill_cancel', 'skill_cancel']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'startup', 'Fill', 'skill_cancel', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove'] * n
    assert p2_json_dict['actionType'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [50] * n
    assert p2_json_dict['hp'][-n:] == [50] * n

def test_block_blockable_skill():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(uppercut_once_bot, perma_block_bot, 6, 8)

    # executes turns
    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [6, 7, 7, 7, 7, 7, 7]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'uppercut', 'uppercut', 'NoMove', 'NoMove']

    assert p2_json_dict['hp'][-1] == HP
    assert p2_json_dict['state'][-n:] == ['NoMove'] + ['block'] * (6)
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['xCoord'][-n:] == [8] * n

def test_block_unblockable_skill():
    # assumption: dash_attack is unblockable
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(dash_attack_once_bot, perma_block_bot, 5, 8)

    # executes turns
    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [5, 6, 6, 11, 11, 11, 11]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'dash_attack', 'dash_attack', 'NoMove', 'NoMove']

    assert p2_json_dict['hp'][-1] < HP
    assert p2_json_dict['xCoord'][-n:] == [8] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['state'][-n:] == ['NoMove'] + ['block'] * (6)

def test_break_block_gets_stunned():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot, 7, 8)

    pass

def test_parry_blockable_skill():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(uppercut_once_bot, block_once_bot, 6, 9)

    # executes turns
    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [6, 7, 7, 7, 7, 7, 7]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'uppercut', 'uppercut', 'NoMove', 'NoMove']
    assert p1_json_dict['stun'][-1] > 0

    assert p2_json_dict['hp'][-1] == HP
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move'] + ['block'] * (4)
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['xCoord'][-n:] == [9] + [8] * 6

def test_parry_unblockable_skill():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(dash_attack_once_bot, block_once_bot, 6, 9)

    # executes turns
    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [6, 7, 7, 12, 12, 12, 12]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'dash_attack', 'dash_attack', 'NoMove', 'NoMove']
    assert p1_json_dict['stun'][-1] == 0

    assert p2_json_dict['hp'][-1] < HP
    assert p2_json_dict['xCoord'][-n:] == [9, 8, 8, 8, 9, 9, 9]
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move'] + ['block'] * (4)

def test_skill_cooldown():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(perma_meditate_bot, nothing_bot, 6, 9)

    # executes turns
    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [6] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'meditate', 'meditate', 'NoMove', 'NoMove', 'NoMove', 'NoMove']

    assert p2_json_dict['xCoord'][-n:] == [9] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['state'][-n:] == ['NoMove'] * n

def test_teleport_onto_player():
    pass

#TODO: need to finishe
def test_teleport():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(teleport_once_bot, nothing_bot, 5, 8)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    # assumptions: heavy has startup of 1
    #TODO: IDK
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [5, 6, 6, 1, 1, 1, 1]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'teleport', 'teleport', 'NoMove', 'NoMove']

def test_teleport_outside_map():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(teleport_once_bot, nothing_bot, 3, 8)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    # assumptions: heavy has startup of 1
    #TODO: IDK
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [3, 4, 4, 0, 0, 0, 0]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'teleport', 'teleport', 'NoMove', 'NoMove']

def test_teleport_dodges_dash_attack():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(teleport_once_bot, dash_attack_once_bot, 5, 8)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    # assumptions: heavy has startup of 1
    #TODO: IDK
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [5, 6, 6, 1, 1, 1, 1]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'teleport', 'teleport', 'NoMove', 'NoMove']
    assert p1_json_dict['hp'][-1] == HP

    assert p2_json_dict['xCoord'][-n:] == [8, 7, 7, 2, 2, 2, 2]
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'dash_attack', 'dash_attack', 'NoMove', 'NoMove']

def test_meditate_heals_before_damage():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(meditate_once_bot, dash_attack_once_bot, 5, 8)

    player1._hp = 1
    artificially_move_player(player1, 5, p1_json_dict)
    artificially_move_player(player2, 8, p2_json_dict)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    # assumptions: heavy has startup of 1
    #TODO: IDK
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [5, 6, 6, 5, 5, 5, 5]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'meditate', 'meditate', 'NoMove', 'NoMove']
    assert p1_json_dict['hp'][-1] > 0

    assert p2_json_dict['xCoord'][-n:] == [8, 7, 7, 2, 2, 2, 2]
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'dash_attack', 'dash_attack', 'NoMove', 'NoMove']

def test_super_saiyan():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(super_saiyan_attack_bot, nothing_bot, 5, 8)

    for i in range(4):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    # assumptions: heavy has startup of 1
    #TODO: IDK
    n = 9
    assert p1_json_dict['xCoord'][-n:] == [5, 5, 5, 7, 7, 7, 7, 7, 7]
    assert p2_json_dict['xCoord'][-n:] == [8, 8, 8, 8, 8, 8, 8, 8, 8]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'saiyan', 'saiyan', 'move', 'move', 'light', 'light', 'light', 'light']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', 'activate', 'Fill', (2, 0), 'Fill', 'activate', 'Fill', 'activate', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove']
    assert p2_json_dict['actionType'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [50] * n
    assert p2_json_dict['hp'][-n:] == [HP, HP, HP, HP, HP, HP-4, HP-4, HP-8, HP-8]

def test_dash_attack():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(dash_attack_once_bot, nothing_bot, 4, 8)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 8

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 7
    assert p1_json_dict['xCoord'][-n:] == [4, 5, 5, 10, 10, 10, 10]
    assert p2_json_dict['xCoord'][-n:] == [8, 8, 8, 8, 9, 9, 9]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'dash_attack', 'dash_attack', 'NoMove', 'NoMove']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'NoMove', 'NoMove', 'NoMove', 'Hurt', 'NoMove', 'NoMove']
    assert p2_json_dict['actionType'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [50] * n
    assert p2_json_dict['hp'][-1] < HP

def test_uppercut():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(uppercut_once_bot, nothing_bot, 4, 6)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 6

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 7
    assert p1_json_dict['xCoord'][-n:] == [4, 5, 5, 5, 5, 5, 5]
    assert p2_json_dict['xCoord'][-n:] == [6, 6, 6, 6, 8, 8, 8]
    assert p1_json_dict['yCoord'][-n:] == [0, 0, 0, 0, 0, 1, 1]
    assert p2_json_dict['yCoord'][-n:] == [0, 1, 1, 1, 1, 1, 1]
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'uppercut', 'uppercut', 'uppercut', 'uppercut']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'NoMove', 'NoMove', 'NoMove', 'Hurt', 'NoMove', 'NoMove']
    assert p2_json_dict['actionType'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [50] * n
    assert p2_json_dict['hp'][-1] < HP

def test_uppercut_hits_airborne_player():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(uppercut_once_bot, jump_bot, 4, 6)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 6

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 7
    assert p1_json_dict['xCoord'][-n:] == [4, 5, 5, 5, 5, 5, 5]
    assert p2_json_dict['xCoord'][-n:] == [6, 6, 6, 6, 8, 8, 8]
    assert p1_json_dict['yCoord'][-n:] == [0, 0, 0, 0, 0, 0, 0]
    assert p2_json_dict['yCoord'][-n:] == [0, 1, 1, 1, 1, 0, 0]
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'uppercut', 'uppercut', 'NoMove', 'NoMove']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'NoMove', 'Hurt', 'NoMove', 'NoMove']
    assert p2_json_dict['actionType'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [50] * n
    assert p2_json_dict['hp'][-1] < HP

#TODO: idk if this is the intented behaviour - Yes, player is invulnerable during dash
def test_dash_dodges_hadoken():
    pass

def test_teleport_dodges_hadoken():
    pass

def test_uppercut_at_same_time():
    pass

def test_teleport_into_hadoken():
    pass