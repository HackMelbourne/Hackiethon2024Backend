import sys
from pathlib import Path

sys.path.append(str(Path("test_basics.py").parent.parent))

# from GameManager import execute_one_turn, setupGame'
from ScriptingHelp.usefulFunctions import *
from pytest_tests.helpers import init_game
from Game.gameSettings import *
from Game.test import *
from Game.playerActions import *
from Game.turnUpdates import playerToJson
import pytest_tests.test_bots.JumpBot as jump_bot

def test_get_hp():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot, 7, 8)
    assert get_hp(player1) == HP

    player1._hp = 21
    assert get_hp(player1) == 21

def test_get_pos():
    pass

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
