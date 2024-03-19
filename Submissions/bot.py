# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from random import random

# primary skill can be defensive or offensive
# secondary skills involve summoning a projectile

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

# currently unsure how to enforce this...
#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = Hadoken

#constants, for easier move return
# movements
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

class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    def init_player_skills(self):
        return self.primary, self.secondary
    
    #MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        return BLOCK
        # there is a projectile
        if len(enemy_projectiles) > 0:
            # print("THIS RAN")
            # print("player", get_pos(player))
            # print("enemy", get_pos(enemy))

            enemy_projectile = enemy_projectiles[0]

            # print("proj", get_proj_pos(enemy_projectile))
            # print("enemy projectile", enemy_projectile)
            # print("distance from proj", abs(get_proj_pos(enemy_projectile)[0] - get_pos(player)[0]))

            if (abs(get_proj_pos(enemy_projectile)[0] - get_pos(player)[0]) < 3):
                # print("I WILL BLOCK")
                return BLOCK
            
        # there is no projectile / it is not immediately close
            
        # if get_distance(player, enemy) < prim_range(enemy):
        #     # within primary distance of enemy
        #     if get_primary_cooldown(enemy) < 2:

        # if get_distance(player, enemy) < seco_range(enemy):

        # if get_distance(player, enemy) < prim_range(player):
            
        # return NOMOVE

def get_distance(player1, player2):
    return abs(get_pos(player1)[0] - get_pos(player2)[0])

# def get_proj_type(proj):
#     return proj.get_skillname()