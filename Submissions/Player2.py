# bot code goes here
from Skills import *
from projectiles import *


#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = UppercutSkill
SECONDARY_SKILL = Hadoken

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
prim = PRIMARY_SKILL(None)
second = SECONDARY_SKILL(None)

PRIMARY = (prim.get_skillname(),)
SECONDARY = (second.get_skillname(),)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)


def init_player_skills():
    return PRIMARY_SKILL, SECONDARY_SKILL
 
#MAIN FUNCTION that returns a single move to the game manager
def get_move(player, enemy, player_projectiles, enemy_projectiles):

    # uncomment below for scripted moves
    # return scripted_moves()    
    # uncomment below for calculated moves
    #return full_assault(player, enemy)
    return full_parry(player, enemy)
    
    
# helpful functions
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

def primary_on_cooldown(player):
    return player.primary_on_cd()

def secondary_on_cooldown(player):
    return player.secondary_on_cd()

def heavy_on_cooldown(player):
    return player.heavy_on_cd()

# tactics below
# get close to enemy and use skills and attacks
def full_assault(player, enemy):
    player_x, player_y = get_pos(player)
    enemy_x, enemy_y = get_pos(enemy)
    if player_y == enemy_y and abs(player_x - enemy_x) == 1:
        if not primary_on_cooldown(player):
            return PRIMARY
        if not secondary_on_cooldown(player):
            return SECONDARY 
        if not heavy_on_cooldown(player):
            return HEAVY
        return LIGHT
    else:
        return FORWARD

# try to parry as much as possible   
def full_parry(player, enemy):
    player_x, player_y = get_pos(player)
    enemy_x, enemy_y = get_pos(enemy)
    if get_last_move(enemy) == FORWARD:
        # hmm, they're trying to close in for an attack,
        if player_y == enemy_y and abs(player_x - enemy_x) == 1:
            # they are within attack range, time to parry
            return BLOCK
    elif get_stun_duration(enemy) != 0 and (player_y == enemy_y and abs(player_x - enemy_x) == 1):
        # enemy is stunned and within attack range, counterattack
        if not heavy_on_cooldown(player):
            return HEAVY
        return LIGHT
    # they werent moving forward last turn, what to do...
    return NOMOVE

def scripted_moves():
    try:
        return next(moves_iter)
    except StopIteration:
        return NOMOVE
    
    