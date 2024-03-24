# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN

# Set primary and secondary skills
PRIMARY_SKILL = DashAttackSkill
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
CANCEL = ("skill_cancel", )

# no move, aka no input
NOMOVE = "NoMove"

class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
    
        # If primary attack is available and in range, use it
        if not primary_on_cooldown(player) and get_distance(player, enemy) <= prim_range(player):
            return PRIMARY
        # If secondary attack is available and in range, use it
        elif not secondary_on_cooldown(player) and get_distance(player, enemy) <= seco_range(player):
            return SECONDARY
        # If primary attack is on cooldown and enemy is not using primary or secondary, block
        elif primary_on_cooldown(player) and not (primary_on_cooldown(enemy) or secondary_on_cooldown(enemy)) and get_distance(player, enemy) <= seco_range(player):
            return BLOCK
        # If secondary attack is on cooldown and enemy is not using secondary, block
        elif secondary_on_cooldown(player) and not secondary_on_cooldown(enemy) and get_distance(player, enemy) <= seco_range(enemy):
            return BLOCK

        # Check if the previous two moves were light attacks and within range
        if (get_last_move(player) == LIGHT and get_past_move(player, 2) == LIGHT and
            get_distance(player, enemy) <= 1):
            # Combo detected, return heavy attack
            return HEAVY

        # if they're out of range
        elif get_distance(player, enemy) >= 7:
            if get_pos(enemy)[0] > get_pos(player)[0]:  # Enemy is on the right
                return BACK
            else:  # Enemy is on the left
                return BACK
        
        
        return LIGHT