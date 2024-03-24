# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = SuperSaiyanSkill

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
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        if len(enemy_projectiles) > 0: 
            first_proj_pos = get_proj_pos(enemy_projectiles[0])
            proj_distance = abs(get_pos(player)[0] - first_proj_pos[0])
            if proj_distance < 4:
                if not primary_on_cooldown(player):
                    return PRIMARY
                if proj_distance < 2:
                    return BLOCK
                return BACK
           
        if not secondary_on_cooldown(player):
            return SECONDARY
        if not primary_on_cooldown(player) and distance < prim_range(player):
            return PRIMARY
        
        if distance == 1:
            if not heavy_on_cooldown(player):
                return HEAVY
            
            return LIGHT
        
        if get_hp(player) <= get_hp(enemy):
            return FORWARD
        
        if distance > prim_range(player) - 1:
            return FORWARD
        elif  distance == prim_range(player):
            return NOMOVE
        return BACK
