# bot code goes here
from Skills import *
from projectiles import *

# primary skill can be defensive or offensive
# secondary skills involve summoning a projectile

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

# currently unsure how to enforce this...
#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
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

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

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
    #return scripted_moves()    
    # uncomment below for calculated moves
    #return full_assault(player, enemy)
    #return eric_func(player, enemy)
    #return leo_func(player, enemy)
    #return spam_second()
    #return winning_strategy(player, enemy)
    return heavy_combo(player, enemy)
    
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

def prim_range(player):
    return player.primary_range()

def seco_range(player):
    return player.secondary_range()

def get_past_move(player, turns):
    return player.get_past_move(turns)

def get_recovery(player):
    return player.get_recovery()

def skill_cancellable(player):
    return player.skill_cancellable()

# tactics below
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
    
def scripted_moves():
    try:
        return next(moves_iter)
    except StopIteration:
        return NOMOVE
    
def eric_func(player, enemy):
    if abs(get_pos(player)[0] - get_pos(enemy)[0]) < 5:
        return PRIMARY
    return SECONDARY

def leo_func(player, enemy):
    distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

    if get_pos(player) == 0 or get_pos(player) == 30:
        return JUMP_FORWARD

    if distance > 3:
        if (not secondary_on_cooldown(player)):
            return SECONDARY
        else:
            return BACK
    elif distance > 2:
        return BACK
    else:
        if (not primary_on_cooldown(player)):
            return PRIMARY
        else:
            return BLOCK
        
def spam_second():
    return SECONDARY
        
        
def winning_strategy(player, enemy):
    # Check if any skill is available and use it wisely
    if not primary_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= prim_range(player):
        return PRIMARY
    elif not secondary_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= seco_range(player):
        return SECONDARY
    elif not heavy_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= 1:
        return HEAVY

    # Defensive strategy if low on health or enemy is too close
    if get_hp(player) < 20 or abs(get_pos(player)[0] - get_pos(enemy)[0]) < 2:
        # Block if enemy is close and likely to attack
        if abs(get_pos(player)[0] - get_pos(enemy)[0]) == 1:
            return BLOCK
        # Move away from the enemy if possible
        elif get_pos(player)[0] < get_pos(enemy)[0]:
            return BACK
        else:
            return FORWARD

    # Offensive strategy if player has more health
    if get_hp(player) > get_hp(enemy):
        # Close in on the enemy if not in attack range
        if abs(get_pos(player)[0] - get_pos(enemy)[0]) > 1:
            if get_pos(player)[0] < get_pos(enemy)[0]:
                return FORWARD
            else:
                return BACK
        # Use light attack if close and other attacks are on cooldown
        else:
            return LIGHT

    # Default to light attack if nothing else is applicable
    return LIGHT

def heavy_combo(player, enemy):
    player_x, player_y = get_pos(player)
    enemy_x, enemy_y = get_pos(enemy)
    if player_y == enemy_y and abs(player_x - enemy_x) == 1:
        if get_past_move(player, 1) == LIGHT:
            if get_past_move(player, 2) == LIGHT:
                return HEAVY
            else:
                return LIGHT
        else:
            return LIGHT
    return FORWARD