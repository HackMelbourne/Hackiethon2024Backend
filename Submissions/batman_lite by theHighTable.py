# bot code goes here brothaaaa
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN

# Constants for easier move return
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# Attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

# Get skill objects
PRIMARY_SKILL = Meditate
SECONDARY_SKILL = Grenade
PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

# No move, aka no input
NOMOVE = "NoMove"

class Script:
    def __init__(self):
        pass

    # DO NOT TOUCH
    def init_player_skills(self):
        return PRIMARY_SKILL, SECONDARY_SKILL

    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        # Get distance between player and enemy
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

        # Use primary skill when health is low
        if get_hp(player) <=90 and not primary_on_cooldown(player):
            return PRIMARY
        if (1 < distance <5) and  not secondary_on_cooldown(player):
            return SECONDARY
        if( get_last_move(enemy) == "heavy" or get_last_move(enemy) ==  "light"  ) and distance <=1 :
            return BLOCK
        if distance <= 1 and get_stun_duration(enemy) != 0:
            return LIGHT
        elif distance <= 1 and not heavy_on_cooldown(player):
            return HEAVY
        while get_hp(player)<45:
            if not primary_on_cooldown(player):
                return PRIMARY
            elif 2<distance<5 and get_secondary_skill(enemy) in ['grenade','hadoken','boomerang'] and get_primary_skill(enemy) in ['dash_attack','uppercut','onepunch']:
                if secondary_on_cooldown(enemy) and primary_on_cooldown(enemy):
                    return SECONDARY
                else:
                    JUMP_BACKWARD
            else:
                return BLOCK

        # Use secondary skill at medium range if available


        # If enemy is close, bait and punish
        if distance <= 2 and get_last_move(player) != BLOCK:
            return HEAVY

        # Dodge incoming projectiles
        for proj in enemy_projectiles:
            proj_pos = get_proj_pos(proj)
            if get_secondary_skill(enemy) == "hadoken" and proj_pos[0] - get_pos(player)[0] < 5 and not secondary_on_cooldown(enemy):
                return BLOCK
            if proj_pos[1] == 0 and proj_pos[0] - get_pos(player)[0] < 2:
                return JUMP_BACKWARD

        # If enemy is at close range, attack or block
        if distance < 2:
            if get_block_status(enemy) > 0:
                return HEAVY
            else:
                return LIGHT

        # If enemy is far, move forward to engage
        else:
            return FORWARD