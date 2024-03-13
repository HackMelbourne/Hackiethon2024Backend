from pprint import pprint
import sys
from pathlib import Path

sys.path.append(str(Path("test_basics.py").parent.parent))

from Game.GameManager import execute_one_turn, setupGame
from pytest_tests.helpers import artificially_move_player, init_game
from ScriptingHelp.usefulFunctions import *
from Game.gameSettings import *
from Game.test import *
from Game.playerActions import *
import pytest_tests.test_bots.JumpBot as jump_bot

def test_get_hp():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot, 7, 8)
    assert get_hp(player1) == HP

    player1._hp = 21
    assert get_hp(player1) == 21

def test_get_pos():
    # initializing the game
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot, 5, 8)

    artificially_move_player(player1, 5, p1_json_dict)
    artificially_move_player(player2, 8, p2_json_dict)

    pos_list = [(5, 1), (5, 1), (5, 0)]
    # execute turns
    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
        assert get_pos(player1) == pos_list[i]
        

    pprint(p1_json_dict)
    pprint(p2_json_dict)


def test_get_last_move():
    pass

def test_get_stun_duration():
    pass

def test_get_block_status():
    pass

def test_get_proj_pos():
    pass

def test_primary_on_cooldown():
    pass

def test_secondary_on_cooldown():
    pass

def test_heavy_on_cooldown():
    pass

def test_prim_range():
    pass

def test_seco_range():
    pass

def test_get_past_move():
    pass

def test_get_recovery():
    pass

def test_skill_cancellable():
    pass

def test_get_primary_skill():
    pass

def test_get_secondary_skill():
    pass

# checks if the  has landed this turn: cannot make a movement but can still attack or block
def test_get_landed():
    pass
