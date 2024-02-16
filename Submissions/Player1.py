# bot code goes here
from Skills import *
from projectiles import *
from Submissions.PlayerConfigs import Player_Controller

#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = UppercutSkill
SECONDARY_SKILL = OnePunchSkill

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)


# skills
prim = PRIMARY_SKILL()
second = SECONDARY_SKILL()

PRIMARY = (prim.get_skillname(),)
SECONDARY = (second.get_skillname(),)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = LIGHT, HEAVY, PRIMARY,JUMP_FORWARD, JUMP_FORWARD, BLOCK, BLOCK,
moves_iter = iter(moves)


def init_player_skills():
    return PRIMARY_SKILL, SECONDARY_SKILL
 
#MAIN FUNCTION that returns a single move to the game manager
def get_move(player, enemy, player_projectiles, enemy_projectiles):

    try:
        return next(moves_iter)
    except StopIteration:
        return NOMOVE
    
    
def get_hp(player):
    return player.get_hp()

def get_pos(player):
    return player.get_pos()

def get_last_move(player):
    return player.get_last_move()

def get_stun_duration(player):
    return player.get_stun()

def get_block_status(player):
    return player.get_block()

def get_proj_pos(proj):
    return proj.get_pos()

# things to pass into get move to decide next move:
# positions of both players
# enemy projectile position
# player last move
# current skills and cooldowns