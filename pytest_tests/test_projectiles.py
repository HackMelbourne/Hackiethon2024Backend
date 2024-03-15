from pprint import pprint
import sys
from pathlib import Path
from Game.GameManager import execute_one_turn
from pytest_tests.helpers import init_game
from Game.gameSettings import HP

sys.path.append(str(Path("test_basics.py").parent.parent))
import pytest_tests.test_bots.JumpBot as jump_bot
import pytest_tests.test_bots.HadokenOnceBot as hadoken_once_bot
import pytest_tests.test_bots.DoNothingBot as nothing_bot
import pytest_tests.test_bots.PermaBlockBot as perma_block_bot

# no skills have startup
def test_projectile_skill_cancel():
    pass

# boomerang, hadoken and lasso are blockable
# icewall, beartrap and grenade are unblockable

def test_block_blockable_projectile():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, perma_block_bot, 4, 7)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 7

    for i in range(4):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)
    pprint(projectiles)

    n = 9
    assert p1_json_dict['xCoord'][-n:] == [4] + [5] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [7] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover', 'NoMove', 'NoMove']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'Fill', 'NoMove', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove'] + ['Block'] * (n - 1)
    assert p1_json_dict['hp'][-n:] == [50] * n
    assert p2_json_dict['hp'][-1] == 50

def test_block_unblockable_projectile():
    pass

def test_parry_blockable_projectile():
    pass

def test_jump_over_projectile():
    pass

def test_parry_unblockable_projectile():
    pass

def test_projectile_cooldown():
    pass

def test_teleport():
    pass

def test_backwards_boomerange_breaks_ice_wall():
    pass

def test_grenade_breaks_ice_wall():
    # should it damage a person right behind the wall?
    pass

def test_grenade():
    pass

def test_hadoken():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, nothing_bot, 4, 8)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 7

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 7
    assert p1_json_dict['xCoord'][-n:] == [4, 5, 5, 5, 5, 5, 5]
    assert p2_json_dict['xCoord'][-n:] == [7, 7, 7, 7, 7, 7, 7]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'NoMove', 'NoMove']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove']

    assert p2_json_dict['hp'][-1] < HP

def test_hadoken_ends():
    pass

def test_hadoken_at_edge():
    pass

def test_lasso_at_edge():
    pass

def test_bear_trap_at_edge():
    pass

def test_bear_trap_on_ground():
    pass

def test_bear_trap_midair():
    pass

def test_boomerang():
    pass

def test_lasso():
    pass

def test_teleport_dodges_lasso():
    pass

def test_dash_dodges_hadoken():
    pass

def test_teleport_dodges_hadoken():
    pass

def test_lasso_breaks_ice_wall():
    pass

def test_ice_wall_breaks_ice_wall():
    pass

def test_ice_wall_squishes_player_at_edge():
    pass