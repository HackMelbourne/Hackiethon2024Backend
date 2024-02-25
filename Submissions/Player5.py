# bot code goes here
from Skills import *
from projectiles import *

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = UppercutSkill
SECONDARY_SKILL = Lasso

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
PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

# no move, aka no input
NOMOVE = "NoMove"

# Don't touch
def init_player_skills():
    return PRIMARY_SKILL, SECONDARY_SKILL


#MAIN FUNCTION that returns a single move to the game manager
def get_move(player, enemy, player_projectiles, enemy_projectiles):
    # PRIMARY_SKILL is UppercutSkill
    # SECONDARY SKILL is IceWall
    distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

    if prim_range(player) <= distance:
        if not primary_on_cooldown(player):
            return PRIMARY

    if not secondary_on_cooldown(player):
        return SECONDARY

    if distance == 1:
        if not heavy_on_cooldown(player):
            return HEAVY
        return LIGHT

    return FORWARD



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