from pprint import pprint
import sys
from pathlib import Path
from Game.GameManager import execute_one_turn
from Game.projectiles import Hadoken
from pytest_tests.helpers import init_game
from Game.gameSettings import HP

sys.path.append(str(Path("test_basics.py").parent.parent))
import pytest_tests.test_bots.JumpBot as jump_bot
import pytest_tests.test_bots.HadokenOnceBot as hadoken_once_bot
import pytest_tests.test_bots.GrenadeOnceBot as grenade_once_bot
import pytest_tests.test_bots.LassoOnceBot as lasso_once_bot
import pytest_tests.test_bots.IceWallOnceBot as icewall_once_bot
import pytest_tests.test_bots.BearTrapOnceBot as beartrap_once_bot
import pytest_tests.test_bots.BoomerangOnceBot as boomerang_once_bot
import pytest_tests.test_bots.BoomerangThenRunBot as boomerang_then_run_bot
import pytest_tests.test_bots.BoomerangThenTPBot as boomerang_then_tp_bot
import pytest_tests.test_bots.DoNothingBot as nothing_bot
import pytest_tests.test_bots.PermaBlockBot as perma_block_bot
import pytest_tests.test_bots.SpamHadokenBot as spam_hadoken_bot
import pytest_tests.test_bots.BlockOnceBot as block_once_bot
import pytest_tests.test_bots.TeleportOnceBot as teleport_once_bot
import pytest_tests.test_bots.DashAttackOnceBot as dash_attack_once_bot
import pytest_tests.test_bots.SaiyanHadokenBot as saiyan_hadoken_bot
import pytest_tests.test_bots.JumpHadokenBot as jump_hadoken_bot

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
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(grenade_once_bot, perma_block_bot, 4, 8)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 8

    for i in range(5):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)
    pprint(projectiles)

    n = 11
    assert p1_json_dict['xCoord'][-n:] == [4] + [5] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [8] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    # assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover', 'NoMove', 'NoMove']
    # assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'Fill', 'NoMove', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove'] + ['block'] * (n - 1)
    assert p1_json_dict['hp'][-n:] == [HP] * n
    assert p2_json_dict['hp'][-1] < HP

def test_parry_blockable_projectile():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, block_once_bot, 4, 7)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 7

    for i in range(4):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)
    pprint(projectiles)

    n = 9
    assert p1_json_dict['xCoord'][-n:] == [4] + [5] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [7] + [6] * (n-1)
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover', 'NoMove', 'NoMove']
    # assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'Fill', 'NoMove', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'block', 'block', 'block', 'block', 'block', 'block']
    assert p1_json_dict['stun'][-n:] == [0] * n
    assert p2_json_dict['stun'][-n:] == [0] * n
    assert p1_json_dict['hp'][-n:] == [50] * n
    assert p2_json_dict['hp'][-n:] == [50] * n

def test_jump_over_projectile():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, jump_bot, 5, 7)
    
    assert p1_json_dict['xCoord'][-1] == 5
    assert p2_json_dict['xCoord'][-1] == 7

    for i in range(4):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)
    pprint(projectiles)

    n = 9
    assert p1_json_dict['xCoord'][-n:] == [5] + [6] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [7] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0, 1, 1, 1, 1, 0, 0, 0, 0]
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover', 'NoMove', 'NoMove']
    assert p1_json_dict['actionType'][-n:] == ['NoMove', (1, 0), 'Fill', 'activate', 'Fill', 'NoMove', 'Fill', 'NoMove', 'Fill']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'jump', 'jump', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove'] 
    assert p1_json_dict['hp'][-n:] == [HP] * n
    assert p2_json_dict['hp'][-1] == HP

def test_parry_unblockable_projectile():
    pass

#TODO fix this + check projectiles
def test_projectile_cooldown():
    # here, i'm assuming that cooldown starts after the recovery

    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(spam_hadoken_bot, nothing_bot, 4, 8)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 8

    cooldown = Hadoken(player1)._maxCooldown
    turns = cooldown + 3

    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
        pprint(projectiles)
        print("===================")

    # pprint(p1_json_dict)
    # pprint(p2_json_dict)
    # print(projectiles)

    n = 2*turns + 1
    assert p1_json_dict['xCoord'][-n:] == [4] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 
                                          'hadoken', 'hadoken', 
                                          'recover', 'recover'] + ['NoMove', 'NoMove'] * cooldown + ['hadoken', 'hadoken']
    assert p1_json_dict['hp'][-n:] == [HP] * n

def test_saiyan_move_into_hadoken():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(saiyan_hadoken_bot, nothing_bot, 2, 8)
    
    assert p1_json_dict['xCoord'][-1] == 2
    assert p2_json_dict['xCoord'][-1] == 8

    cooldown = Hadoken(player1)._maxCooldown
    turns = 6

    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
        pprint(projectiles)
        print("===================")


    n = 2*turns + 1
    assert p1_json_dict['xCoord'][-n:] == [2, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 7, 7]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['state'][-n:] == ['NoMove', 
                                          'move', 'move', 
                                          'saiyan', 'saiyan'
                                          'hadoken', 'hadoken', 
                                          'recover', 'recover',
                                          'move', 'move',
                                          'move', 'move']
    assert p1_json_dict['hp'][-n:] == [HP] * n

def test_backwards_boomerang_breaks_ice_wall():
    pass

def test_grenade_breaks_ice_wall():
    # should it damage a person right behind the wall? I think yes
    pass

def test_teleport_onto_ice_wall():
    pass

def test_grenade():
    pass

def test_teleport_hadoken_combo():
    pass

def test_hadoken_in_air():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(jump_hadoken_bot, nothing_bot, 4, 7)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 7

    turns = 10
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2 * turns + 1
    assert p1_json_dict['xCoord'][-n:] == [4] + [5] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [7] * n
    assert p1_json_dict['yCoord'][-n:] == [0, 0, 0, 1, 1, 1, 1] + [0] * (n-7)
    assert p1_json_dict['projXCoord'][-n:] == [-1, -1, -1, -1, -1, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, -1, -1]
    assert p1_json_dict['projYCoord'][-n:] == [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1]
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover'] + ['NoMove'] * (n-9)
    assert p2_json_dict['state'][-n:] == ['NoMove'] * n
    assert p2_json_dict['hp'][-1] == HP

def test_hadoken():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, nothing_bot, 4, 7)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 7

    for i in range(3):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 7
    assert p1_json_dict['xCoord'][-n:] == [4, 5, 5, 5, 5, 5, 5]
    assert p2_json_dict['xCoord'][-n:] == [7, 7, 7, 7, 7, 7, 9]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'NoMove', 'Hurt']

    assert p2_json_dict['hp'][-1] < HP

def test_hadoken_ends():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, nothing_bot, 3, 12)
    
    assert p1_json_dict['xCoord'][-1] == 3
    assert p2_json_dict['xCoord'][-1] == 12

    turns = 9
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2*turns +1 
    assert p1_json_dict['xCoord'][-n:] == [3] + [4] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [12] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover'] + ['NoMove'] * (n - 7)
    assert p2_json_dict['state'][-n:] == ['NoMove'] * n
    assert p2_json_dict['hp'][-n:] == [HP] * n

def test_hadoken_hits_end():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, nothing_bot, 3, 11)
    
    assert p1_json_dict['xCoord'][-1] == 3
    assert p2_json_dict['xCoord'][-1] == 11

    turns = 9
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2*turns +1 
    assert p1_json_dict['xCoord'][-n:] == [3] + [4] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [11] * (n - 3) + [13, 13, 13]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover'] + ['NoMove'] * (n - 7)
    assert p2_json_dict['state'][-n:] == ['NoMove'] * (n-3) + ['Hurt', 'NoMove', 'NoMove']
    assert p2_json_dict['hp'][-n:] == [HP] * (n-3) + [45, 45, 45]
    assert p2_json_dict['hp'][-1] < HP

def test_hadoken_at_edge():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, jump_bot, 13, 15)
    
    assert p1_json_dict['xCoord'][-1] == 13
    assert p2_json_dict['xCoord'][-1] == 15

    turns = 4
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2*turns +1 
    assert p1_json_dict['xCoord'][-n:] == [13] + [14] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [15] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p1_json_dict['projXCoord'][-n:] == [-1, -1, -1, 15, 15, 15, -1, -1, -1]
    assert p1_json_dict['projYCoord'][-n:] == [-1, -1, -1, 0, 0, 0, -1, -1, -1]
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover','NoMove', 'NoMove']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'NoMove', 'NoMove', 'NoMove', 'Hurt', 'NoMove', 'NoMove']
    assert p1_json_dict['hp'][-n:] == [HP] * n
    assert p2_json_dict['hp'][-n:] == [HP] * 6 + [45] * (n-6)

def test_lasso_at_edge():
    pass

def test_bear_trap_at_edge():
    pass

def test_bear_trap_on_ground():
    pass

def test_bear_trap_midair():
    pass

def test_boomerang_hits_forwards():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(boomerang_once_bot, nothing_bot, 3, 7)
    
    assert p1_json_dict['xCoord'][-1] == 3
    assert p2_json_dict['xCoord'][-1] == 7

    turns = 3
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2*turns +1 
    assert p1_json_dict['xCoord'][-n:] == [3] + [4] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [7] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'boomerang', 'boomerang', 'recover', 'recover']
    assert p2_json_dict['state'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [HP] * n
    assert p2_json_dict['hp'][-n:-2] == [HP] *(n-2)

def test_boomerang_hits_backwards():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(boomerang_once_bot, jump_bot, 4, 6)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 6

    turns = 10
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2*turns +1 
    assert p1_json_dict['xCoord'][-n:] == [4] + [5] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [6] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'boomerang', 'boomerang', 'recover', 'recover'] + ['NoMove'] * (n-7)
    assert p2_json_dict['state'][-n:] == ['NoMove', 'jump', 'jump'] + ['NoMove'] * (n-3)
    assert p1_json_dict['hp'][-n:] == [HP] * n
    assert p2_json_dict['hp'][-n:-2] == [HP] *(n-2)
    assert p2_json_dict['hp'][-1] < HP

def test_boomerang_pickup_backwards():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(boomerang_then_run_bot, nothing_bot, 4, 11)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 11

    turns = 10
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2*turns +1 
    assert p1_json_dict['xCoord'][-n:] == [4, 5, 5, 5, 5, 5, 5] + [6] * (n-7)
    assert p2_json_dict['xCoord'][-n:] == [11] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'boomerang', 'boomerang', 'recover', 'recover', 'move', 'move'] + ['NoMove'] * (n-9)
    assert p2_json_dict['state'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [HP] * n
    assert p2_json_dict['hp'][-n:] == [HP] * n
    assert p1_json_dict['projXCoord'][-n:] == [-1, -1, -1, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 9, 9, 8, 8, 7, 7, -1, -1]

def test_boomerang_pickup_forwards():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(boomerang_then_tp_bot, nothing_bot, 4, 11)
    
    assert p1_json_dict['xCoord'][-1] == 4
    assert p2_json_dict['xCoord'][-1] == 11

    turns = 5
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2*turns +1 
    assert p1_json_dict['xCoord'][-n:] == [4, 5, 5, 5, 5, 5, 5, 10, 10, 9, 9]
    assert p2_json_dict['xCoord'][-n:] == [11] * n
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'boomerang', 'boomerang', 'recover', 'recover', 'teleport', 'teleport', 'move', 'move']
    assert p2_json_dict['state'][-n:] == ['NoMove'] * n
    assert p1_json_dict['hp'][-n:] == [HP] * n
    assert p2_json_dict['hp'][-n:] == [HP] * n
    assert p1_json_dict['projXCoord'][-n:] == [-1, -1, -1, 6, 6, 7, 7, 8, 8, -1 -1]
    assert p1_json_dict['projYCoord'][-n:] == [-1, -1, -1, 0, 0, 0, 0, 0, 0, -1 -1]

def test_boomerang_in_air():
    pass

def test_knockup_into_edge():
    pass

def test_lasso():
    pass

def test_teleport_dodges_lasso():
    pass

def test_dash_dodges_hadoken():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, dash_attack_once_bot, 3, 6)
    
    assert p1_json_dict['xCoord'][-1] == 3
    assert p2_json_dict['xCoord'][-1] == 6

    turns = 3
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2*turns +1 
    assert p1_json_dict['xCoord'][-n:] == [3,4,4,4,3,3,3]
    assert p2_json_dict['xCoord'][-n:] == [6, 5, 5, 0, 0, 0, 0]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'Hurt', 'recover', 'recover']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'dash_attack', 'dash_attack', 'NoMove', 'NoMove']
    assert p1_json_dict['hp'][-n:] == [HP] * 3 + [45] * (n-3)
    assert p2_json_dict['hp'][-n:] == [HP] * n

def test_teleport_dodges_hadoken():
    p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles = init_game(hadoken_once_bot, teleport_once_bot, 3, 6)
    
    assert p1_json_dict['xCoord'][-1] == 3
    assert p2_json_dict['xCoord'][-1] == 6

    turns = 3
    for i in range(turns):
        projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)

    pprint(p1_json_dict)
    pprint(p2_json_dict)

    n = 2*turns +1 
    assert p1_json_dict['xCoord'][-n:] == [3] + [4] * (n-1)
    assert p2_json_dict['xCoord'][-n:] == [6, 5, 5, 0, 0, 0, 0]
    assert p1_json_dict['yCoord'][-n:] == [0] * n
    assert p2_json_dict['yCoord'][-n:] == [0] * n 
    assert p1_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'hadoken', 'hadoken', 'recover', 'recover']
    assert p2_json_dict['state'][-n:] == ['NoMove', 'move', 'move', 'teleport', 'teleport', 'NoMove', 'NoMove']
    assert p1_json_dict['hp'][-n:] == [HP] * n
    assert p2_json_dict['hp'][-n:] == [HP] * n

def test_lasso_breaks_ice_wall():
    pass

def test_ice_wall_breaks_ice_wall():
    pass

def test_ice_wall_squishes_player_at_edge():
    pass