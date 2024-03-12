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

def test_skill_cancel():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_bot, jump_bot, 7, 8)

    pass

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

def test_teleport():
    pass

def test_teleport_outside_map():
    pass

def test_teleport_dodges_dash_attack():
    pass

def test_meditate_heals_before_damage():
    pass

def test_super_saiyan():
    pass

def test_dash_attack():
    pass

def test_uppercut():
    pass

def test_uppercut_hits_airborne_player():
    pass

def test_dash_dodges_hadoken():
    pass

def test_teleport_dodges_hadoken():
    pass

def test_uppercut_at_same_time():
    pass

