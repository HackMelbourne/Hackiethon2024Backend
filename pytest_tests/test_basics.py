
import sys
from pathlib import Path

sys.path.append(str(Path("test_basics.py").parent.parent))

from Game.gameSettings import *
from Game.test import *
from Game.playerActions import *
from Game.turnUpdates import playerToJson
import Submissions.Player1 as p1
import Submissions.Player2 as p2

from pytest_tests.helpers import artificially_move_player, init_game
import pytest_tests.test_bots.MoveBackwards as backwards_bot
import pytest_tests.test_bots.JumpBackwardsBot as jump_backwards_bot
import pytest_tests.test_bots.JumpForwardsBot as jump_forwards_bot
import pytest_tests.test_bots.JumpBot as jump_bot
import pytest_tests.test_bots.DoNothingBot as nothing_bot
import pytest_tests.test_bots.ForwardsBot as forwards_bot
import pytest_tests.test_bots.PunchOnceBot as punch_once_bot
import pytest_tests.test_bots.PunchHeavyMultiBot as punch_heavy_multi_bot
from Game.GameManager import execute_one_turn

def test_test():
    assert 1==1


def test_start_game():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(forwards_bot, forwards_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(backwards_bot, backwards_bot)

    # artificially changing their starting coordinates
    artificially_move_player(player1, 1, p1_json_dict)
    artificially_move_player(player2, 30, p2_json_dict)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_backwards_bot, jump_backwards_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_backwards_bot, jump_backwards_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(nothing_bot, nothing_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_forwards_bot, jump_forwards_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(nothing_bot, punch_once_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(forwards_bot, forwards_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(forwards_bot, forwards_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_forwards_bot, jump_forwards_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_forwards_bot, jump_bot)

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_forwards_bot, jump_bot)

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
        # print("P2 JSON DICT", p2_json_dict)


    


def test_death_win():
    pass

def test_higher_hp_win():
    pass

def test_coin_flip_win():
    pass

def test_block():
    pass

def test_parry():
    pass

def no_jump_on_land():
    pass

