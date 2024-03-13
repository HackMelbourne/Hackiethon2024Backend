from pprint import pprint
import sys
from pathlib import Path
from Game.GameManager import execute_one_turn

sys.path.append(str(Path("test_basics.py").parent.parent))

# from GameManager import execute_one_turn, setupGame'
from ScriptingHelp.usefulFunctions import *
from pytest_tests.helpers import init_game
from Game.gameSettings import *
from Game.test import *
from Game.playerActions import *
from Game.turnUpdates import playerToJson
import pytest_tests.test_bots.JumpBot as jump_bot
import pytest_tests.test_bots.OnePunchCancelBot as one_punch_cancel_bot # walks forward once, then heavy's, then cancels
import pytest_tests.test_bots.DoNothingBot as nothing_bot
import pytest_tests.test_bots.TeleportOnceBot as teleport_once_bot
import pytest_tests.test_bots.DashAttackOnceBot as dash_attack_once_bot

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot, 7, 8)
    
    pass

def test_block_unblockable_skill():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot, 7, 8)

    pass

def test_long_block_gets_stunned():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot, 7, 8)

    pass

def test_parry_blockable_skill():
    pass

def test_parry_unblockable_skill():
    pass

def test_skill_cooldown():
    pass

def test_teleport_onto_player():
    pass

def test_teleport():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(teleport_once_bot, nothing_bot, 4, 8)
    
    assert p1_json_dict['xCoord'][-1] == 1
    assert p2_json_dict['xCoord'][-1] == 8

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    # assumptions: heavy has startup of 1
    #TODO: IDK
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [4, 5, 5, 10, 10, 10, 10]
    assert p2_json_dict['xCoord'][-n:] == [8, 8, 8, 8, 9, 9, 9]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'dash_attack', 'dash_attack', 'NoMove', 'NoMove']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'NoMove', 'NoMove', 'NoMove', 'Hurt', 'NoMove']
    assert p2_json_dict['actionType'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [50] * n
    assert p2_json_dict['hp'][-1] < HP

def test_teleport_outside_map():
    pass

def test_teleport_dodges_dash_attack():
    pass

def test_meditate_heals_before_damage():
    pass

def test_super_saiyan():
    pass

def test_dash_attack():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(dash_attack_once_bot, nothing_bot, 4, 8)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 8

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    # assumptions: heavy has startup of 1
    #TODO: IDK
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [4, 5, 5, 10, 10, 10, 10]
    assert p2_json_dict['xCoord'][-n:] == [8, 8, 8, 8, 9, 9, 9]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'dash_attack', 'dash_attack', 'NoMove', 'NoMove']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'NoMove', 'NoMove', 'NoMove', 'Hurt', 'NoMove']
    assert p2_json_dict['actionType'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [50] * n
    assert p2_json_dict['hp'][-1] < HP

def test_uppercut():
    pass

def test_uppercut_hits_airborne_player():
    pass

#TODO: idk if this is the intented behaviour
def test_dash_dodges_hadoken():
    pass

def test_teleport_dodges_hadoken():
    pass

def test_uppercut_at_same_time():
    pass

