# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = Meditate
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

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):

        distance = get_distance(player, enemy)

        if distance == 1 and get_primary_skill(enemy) == "onepunch" and get_primary_cooldown(enemy) == 0:
            return JUMP

        if 0 <= distance <= 5:
            if (get_secondary_skill(enemy) == Hadoken or get_secondary_skill(enemy) == Boomerang
            ) and not secondary_on_cooldown(enemy):
                return JUMP_FORWARD

            if get_secondary_skill(enemy) == Grenade and not secondary_on_cooldown(enemy):
                if distance == 1:
                    return FORWARD
                if distance >= 2:
                    return BACK

            if not primary_on_cooldown(player):
                return PRIMARY

            if not secondary_on_cooldown(player):
                return SECONDARY
            
            if distance == 1:
                if not primary_on_cooldown(enemy) and (get_primary_skill(enemy) == UppercutSkill):
                    return BLOCK
                if not heavy_on_cooldown(player):
                    return HEAVY
                if not secondary_on_cooldown(enemy):
                    return BLOCK
                else:
                    return LIGHT    

            else:
                if get_primary_skill(enemy) != UppercutSkill:
                    return JUMP_FORWARD
                else:
                    return FORWARD

        if distance > 5:
            if (distance < 8 and get_secondary_skill(enemy) == Boomerang
                and (get_secondary_cooldown(enemy) == compare_moves(get_last_move(enemy), Boomerang))):
                return JUMP_FORWARD
            return FORWARD # when changed to JUMP_FORWARD, it ties with some versions of testingbot 

