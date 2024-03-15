
from pprint import pprint
import sys
from pathlib import Path

sys.path.append(str(Path("test_basics.py").parent.parent))

from Game.gameSettings import *
from Game.test import *
from Game.playerActions import *

from pytest_tests.helpers import artificially_move_player, init_game
from Game.GameManager import execute_one_turn
import pytest_tests.test_bots.MoveBackwards as backwards_bot
import pytest_tests.test_bots.JumpBackwardsBot as jump_backwards_bot
import pytest_tests.test_bots.JumpForwardsBot as jump_forwards_bot
import pytest_tests.test_bots.JumpBot as jump_bot
import pytest_tests.test_bots.DoNothingBot as nothing_bot
import pytest_tests.test_bots.ForwardsBot as forwards_bot
import pytest_tests.test_bots.PunchOnceBot as punch_once_bot
import pytest_tests.test_bots.PunchHeavyMultiBot as punch_heavy_multi_bot
import pytest_tests.test_bots.BlockOnceBot as block_once_bot
import pytest_tests.test_bots.LightAttackBot as light_attack_bot
import pytest_tests.test_bots.RepeatJumpBot as repeat_jump_bot

def test_test():
    assert 1==1


def test_start_game():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(forwards_bot, forwards_bot, 5, 10)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 5, p1_json_dict)
    artificially_move_player(player2, 10, p2_json_dict)
    
    assert p1_json_dict['xCoord'][-1] == 5
    assert p2_json_dict['xCoord'][-1] == 10


    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    assert p1_json_dict['xCoord'][-2:] == [6, 6]
    assert p2_json_dict['xCoord'][-2:] == [9, 9]

def test_move_backwards_to_edge():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(backwards_bot, backwards_bot, 1, 14)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 1, p1_json_dict)
    artificially_move_player(player2, 14, p2_json_dict)

    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    assert p1_json_dict['xCoord'][-2:] == [0, 0]
    assert p1_json_dict['yCoord'][-2:] == [0, 0]
    assert p2_json_dict['xCoord'][-2:] == [15, 15]
    assert p2_json_dict['yCoord'][-2:] == [0,0]
    
    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    assert p1_json_dict['xCoord'][-1] == 0
    assert p2_json_dict['xCoord'][-1] == 15

def test_jump_up():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot, 2, 5)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 2, p1_json_dict)
    artificially_move_player(player2, 5, p2_json_dict)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)


    assert p1_json_dict['xCoord'][-7:] == [2 for i in range(7)]
    assert p2_json_dict['xCoord'][-7:] == [5 for i in range(7)]
    assert p1_json_dict['yCoord'][-7:] == [0,1,1, 1, 1,0, 0]
    assert p2_json_dict['yCoord'][-7:] == [0,1,1, 1, 1, 0, 0]

def test_jump_backwards_from_edge():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_backwards_bot, jump_backwards_bot, 0, 15)

    # artificially changing their starting coordinates
    # artificially changing their starting coordinates
    artificially_move_player(player1, 0, p1_json_dict)
    artificially_move_player(player2, 15, p2_json_dict)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    print(p1_json_dict)

    assert p1_json_dict['xCoord'][-7:] == [0,0,0,0,0,0,0]
    assert p2_json_dict['xCoord'][-7:] == [15, 15, 15,15,15,15,15]
    assert p1_json_dict['yCoord'][-7:] == [0, 1, 1, 1, 1,0,0]
    assert p2_json_dict['yCoord'][-7:] == [0, 1, 1, 1,1,0, 0]

def test_jump_backwards_to_edge():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_backwards_bot, jump_backwards_bot, 1, 13)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 1, p1_json_dict)
    artificially_move_player(player2, 13, p2_json_dict)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    print(p1_json_dict)

    assert p1_json_dict['xCoord'][-7:] == [1, 0, 0, 0, 0, 0,0]
    assert p2_json_dict['xCoord'][-7:] == [13, 14, 14, 15,15, 15, 15]
    assert p1_json_dict['yCoord'][-7:] == [0, 1, 1, 1, 1, 0, 0]
    assert p2_json_dict['yCoord'][-7:] == [0,1,1, 1, 1, 0, 0]

def test_do_nothing():
    # init game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(nothing_bot, nothing_bot, 7,8)

    # turn 1
    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    print("DO NOTHING")
    print(p1_json_dict)
    print(p2_json_dict)

    # players should be in same position
    assert p1_json_dict['xCoord'][0] == p1_json_dict['xCoord'][1] 
    assert p1_json_dict['yCoord'][0] == p1_json_dict['yCoord'][1]
    assert p2_json_dict['xCoord'][0] == p2_json_dict['xCoord'][1] 
    assert p2_json_dict['yCoord'][0] == p2_json_dict['yCoord'][1]

    # turn 2
    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    # players should be in same position
    assert p1_json_dict['xCoord'][-3] == p1_json_dict['xCoord'][-1] 
    assert p1_json_dict['yCoord'][-3] == p1_json_dict['yCoord'][-1] 
    assert p2_json_dict['xCoord'][-3] == p2_json_dict['xCoord'][-1] 
    assert p2_json_dict['yCoord'][-3] == p2_json_dict['yCoord'][-1] 

def test_jump_forward():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_forwards_bot, jump_forwards_bot, 1, 14)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 1, p1_json_dict)
    artificially_move_player(player2, 14, p2_json_dict)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    print(p1_json_dict)

    assert p1_json_dict['xCoord'][-7:] == [1, 2, 2, 3, 3, 4, 4]
    assert p2_json_dict['xCoord'][-7:] == [14, 13, 13, 12, 12, 11, 11]
    assert p1_json_dict['yCoord'][-7:] == [0, 1, 1, 1, 1, 0, 0]
    assert p2_json_dict['yCoord'][-7:] == [0,1,1, 1,1, 0, 0]

def test_knockback_offstage():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(nothing_bot, punch_once_bot, 0, 1)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 0, p1_json_dict)
    artificially_move_player(player2, 1, p2_json_dict)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    assert p1_json_dict['xCoord'][-7:] == [0 for i in range(7)]
    assert p2_json_dict['xCoord'][-7:] == [1 for i in range(7)]
    assert p1_json_dict['yCoord'][-7:] == [0 for i in range(7)]
    assert p2_json_dict['yCoord'][-7:] == [0 for i in range(7)]
    
    # turn 2
    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    # turn 3
    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    print(p1_json_dict)
    print(p2_json_dict)

def test_players_collide_ground_odd():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(forwards_bot, forwards_bot, 6,8)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 6, p1_json_dict)
    artificially_move_player(player2, 8, p2_json_dict)

    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    assert p2_json_dict['xCoord'][-5:] == [8, 7, 8, 7, 8]
    assert p1_json_dict['xCoord'][-5:] == [6, 7, 6, 7, 6]
    assert p1_json_dict['yCoord'][-5:] == [0, 0,0, 0, 0]
    assert p2_json_dict['yCoord'][-5:] == [0,0, 0, 0, 0]

def test_players_collide_ground_even():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(forwards_bot, forwards_bot, 5,8)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 5, p1_json_dict)
    artificially_move_player(player2, 8, p2_json_dict)

    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    assert p1_json_dict['xCoord'][-5:] == [5, 6, 6, 6, 6]
    assert p2_json_dict['xCoord'][-5:] == [8, 7, 7, 7, 7]
    assert p1_json_dict['yCoord'][-5:] == [0, 0,0, 0, 0]
    assert p2_json_dict['yCoord'][-5:] == [0,0, 0, 0, 0]    


def test_players_collide_midair():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_forwards_bot, jump_forwards_bot,5,8)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 5, p1_json_dict)
    artificially_move_player(player2, 8, p2_json_dict)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    assert p1_json_dict['xCoord'][-7:] == [5, 6, 6, 6, 6, 6, 6]
    assert p2_json_dict['xCoord'][-7:] == [8, 7, 7, 7, 7, 7, 7]
    assert p1_json_dict['yCoord'][-7:] == [0, 1, 1, 1, 1,0, 0]
    assert p2_json_dict['yCoord'][-7:] == [0, 1, 1, 1, 1,0, 0] 

def test_player_jump_into_player_midair():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_forwards_bot, jump_bot, 5,6)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 5, p1_json_dict)
    artificially_move_player(player2, 6, p2_json_dict)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    assert p1_json_dict['xCoord'][-7:] == [5, 6, 5, 5, 5, 5, 5]
    assert p2_json_dict['xCoord'][-7:] == [6, 6, 7, 7, 7, 7, 7]
    assert p1_json_dict['yCoord'][-7:] == [0, 1, 1, 1, 1,0, 0]
    assert p2_json_dict['yCoord'][-7:] == [0, 1, 1, 1, 1,0, 0] 

def test_player_jump_into_player_midair_at_edge():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_forwards_bot, jump_bot, 14,15)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 14, p1_json_dict)
    artificially_move_player(player2, 15, p2_json_dict)

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    assert p1_json_dict['xCoord'][-7:] == [14, 15, 14, 14, 14, 14, 14]
    assert p2_json_dict['xCoord'][-7:] == [15 for i in range(7)]
    assert p1_json_dict['yCoord'][-7:] == [0, 1, 1, 1, 1,0, 0]
    assert p2_json_dict['yCoord'][-7:] == [0, 1, 1, 1, 1,0, 0] 

def test_heavy_cooldown():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(nothing_bot, punch_heavy_multi_bot)

    artificially_move_player(player1, 3, p1_json_dict)
    artificially_move_player(player2, 15, p2_json_dict)

    # execute turns
    for i in range(2):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    n = 7
    assert p1_json_dict['state'][-n:] == ['NoMove', 'heavy', 'heavy', 'heavy', 'heavy', 'NoMove', 'NoMove']


# don't think we need to test these
def test_death():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(light_attack_bot, light_attack_bot)

    player2._hp = 1
    
    # also writes a turn to dict
    artificially_move_player(player1, 3, p1_json_dict)
    artificially_move_player(player2, 4, p2_json_dict)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    #artificially KILLS p2
    player2._hp = 0
    # execute turns
    for i in range(2):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)
    
    
    

    assert p2_dead == True

def test_higher_hp_win():
    pass

def test_coin_flip_win():
    pass

def test_both_die_same_time():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(light_attack_bot, light_attack_bot)

    player1._hp = 1
    player2._hp = 1

    # also writes a turn to dict
    artificially_move_player(player1, 3, p1_json_dict)
    artificially_move_player(player2, 4, p2_json_dict)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    # execute turns
    # artificially kills both players
    player1._hp = 0
    player2._hp = 0
    for i in range(2):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    assert p1_dead == True
    assert p2_dead == True

def test_block():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(punch_once_bot, block_once_bot)

    artificially_move_player(player1, 3, p1_json_dict)
    artificially_move_player(player2, 7, p2_json_dict)

    # execute turns
    for i in range(4):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    print(p1_json_dict)
    print(p2_json_dict)

    # assumptions: heavy has startup of 1
    n = 9
    assert p1_json_dict['xCoord'][-n:] == [3, 4, 4, 5, 5, 5, 5, 5, 5]
    assert p2_json_dict['xCoord'][-n:] == [7, 6, 6, 6, 6, 6, 6, 6, 6]
    assert p1_json_dict['yCoord'][-n:] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert p2_json_dict['yCoord'][-n:] == [0, 0, 0, 0, 0, 0, 0, 0, 0] 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'move', 'move', 'heavy', 'heavy', 'heavy', 'heavy']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', (1, 0), 'Fill', 'startup', 'Fill', 'activate', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'block', 'block', 'block', 'block', 'block', 'block']
    assert p2_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'activate', 'Fill', 'activate', 'Fill']
    assert p1_json_dict['hp'][-n:] == [50 for i in range(n)]
    assert p2_json_dict['hp'][-n:] == [50 for i in range(n)]

def test_parry():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(light_attack_bot, block_once_bot, 5, 8)

    artificially_move_player(player1, 5, p1_json_dict)
    artificially_move_player(player2, 8, p2_json_dict)

    # execute turns
    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    print(p1_json_dict)
    print(p2_json_dict)
    
    n = 7
    assert p1_json_dict['xCoord'][-n:] == [5, 6, 6, 6, 6, 6, 6]
    assert p2_json_dict['xCoord'][-n:] == [8, 7, 7, 7, 7, 7, 7]
    assert p1_json_dict['yCoord'][-n:] == [0, 0, 0, 0, 0, 0, 0]
    assert p2_json_dict['yCoord'][-n:] == [0, 0, 0, 0, 0, 0, 0] 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'light', 'light', 'NoMove', 'NoMove']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'NoMove']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'block', 'block', 'block', 'block']
    assert p2_json_dict['actionType'][-n:] == ['NoMove', (-1, 0), 'Fill', 'activate', 'Fill', 'activate', 'Fill']
    assert p1_json_dict['hp'][-n:] == [50 for i in range(n)]
    assert p2_json_dict['hp'][-n:] == [50 for i in range(n)]
    assert p1_json_dict['stun'][-n:] == [0, 0, 0, 0, 0, 2, 2]
    assert p2_json_dict['stun'][-n:] == [0 for i in range(n)]

def test_no_jump_on_land():
    """
    Can't jump multiple times
    """

    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(repeat_jump_bot, nothing_bot)

    artificially_move_player(player1, 5, p1_json_dict)
    artificially_move_player(player2, 8, p2_json_dict)

    # execute turns
    for i in range(7):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    print(p1_json_dict)
    print(p2_json_dict)

    n = 15
    assert p1_json_dict['xCoord'][-n:] == [5 for i in range(n)]
    assert p1_json_dict['yCoord'][-n:] == [0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0]
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'move', 'move', 'NoMove', 'NoMove', 'NoMove', 'NoMove','NoMove', 'NoMove']

def test_combo_attack():
    pass