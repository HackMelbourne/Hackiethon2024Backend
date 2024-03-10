import sys
from pathlib import Path
sys.path.append(str(Path("test_basics.py").parent.parent))

# from GameManager import execute_one_turn, setupGame'
from Game.gameSettings import *
from Game.test import *
from Game.playerActions import *
from Game.turnUpdates import playerToJson
import Submissions.Player1 as p1
import Submissions.Player2 as p2
import pytest_tests.test_bots.MoveBackwards as backwards_bot
import pytest_tests.test_bots.JumpBackwardsBot as jump_backwards_bot
import pytest_tests.test_bots.JumpBot as jump_bot
from Game.GameManager import setupGame, execute_one_turn

def init_game(p1, p2):
    p1_script = p1.Script()
    p2_script = p2.Script()
    player1, player2 = setupGame(p1_script, p2_script)
    stun1 = stun2 = 0
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

    return p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles

def write_turn(player1, player2, p1_json_dict, p2_json_dict, nomove=False, start=True):
    playerToJson(player1, p1_json_dict, nomove, start)
    playerToJson(player2,p2_json_dict, nomove,start)

def test_test():
    assert 1==1


def test_start_game():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(p1, p1)

    # artificially changing their starting coordinates
    player1._xCoord = 5
    player2._xCoord = 10

    playerToJson(player1, p1_json_dict, True, True)
    playerToJson(player2,p2_json_dict, True, True)
    
    assert p1_json_dict['xCoord'][-1] == 5
    assert p2_json_dict['xCoord'][-1] == 10


    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    write_turn(player1, player2, p1_json_dict, p2_json_dict)

    assert p1_json_dict['xCoord'][-1] == 6
    assert p2_json_dict['xCoord'][-1] == 9

def test_move_backwards_to_edge():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(backwards_bot, backwards_bot)

    # artificially changing their starting coordinates
    player1._xCoord = 0
    player2._xCoord = 30
    write_turn(player1, player2, p1_json_dict, p2_json_dict, True, True)

    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    write_turn(player1, player2, p1_json_dict, p2_json_dict)

    assert p1_json_dict['xCoord'][-1] == 0
    assert p1_json_dict['yCoord'][-1] == 0
    assert p2_json_dict['xCoord'][-1] == 15
    assert p2_json_dict['yCoord'][-1] == 0
    
    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    write_turn(player1, player2, p1_json_dict, p2_json_dict)

    assert p1_json_dict['xCoord'][-1] == 0
    assert p2_json_dict['xCoord'][-1] == 15

def test_jump_up():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot)

    # artificially changing their starting coordinates
    player1._xCoord = 2
    player2._xCoord = 5

    for i in range(5):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
        write_turn(player1, player2, p1_json_dict, p2_json_dict, True)

    print(p1_json_dict, p2_json_dict)

    assert p1_json_dict['xCoord'][-5:] == [2, 2,2,2,2]
    assert p2_json_dict['xCoord'][-5:] == [5,5,5,5,5]
    assert p1_json_dict['yCoord'][-5:] == [1,0, 1,0,1]
    assert p2_json_dict['yCoord'][-5:] == [1,0, 1,0,1]

def test_jump_backwards_to_edge():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_backwards_bot, jump_backwards_bot)

    # artificially changing their starting coordinates
    player1._xCoord = 0
    player2._xCoord = 15
    write_turn(player1, player2, p1_json_dict, p2_json_dict, True, True)

    for i in range(8):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
        write_turn(player1, player2, p1_json_dict, p2_json_dict, True, True)

    print(p1_json_dict)

    assert p1_json_dict['xCoord'][-3:] == [0 for i in range(3)]
    assert p2_json_dict['xCoord'][-3:] == [15 for i in range(3)]
    assert p1_json_dict['yCoord'][-3:] == [1, 0, 1]
    assert p2_json_dict['yCoord'][-3:] == [1,0,1]








