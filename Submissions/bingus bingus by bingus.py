# bingus bingus
# by bingus




# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


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
        self.ticks = 0
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        self.ticks+=1
        #print(self.ticks)
        dist = get_distance(player, enemy)

        if dist in [0, 1, 2, 3, 4]:
            

            if get_secondary_skill(enemy)=="super_armor" and not primary_on_cooldown(player):
                return PRIMARY
                    
                    
            if (get_hp(player) < 80 or get_hp(enemy)>get_hp(player)) and not primary_on_cooldown(player):
                return PRIMARY
                
            if not secondary_on_cooldown(player):
                if get_primary_skill(enemy) == "meditate" and get_secondary_skill(enemy) == "super_saiyan":
                    if get_hp(player) < 100:
                        return SECONDARY
                else:
                    return SECONDARY

            if 0 < dist < 2:
                if not heavy_on_cooldown(player):
                    return HEAVY
                    
                if secondary_on_cooldown(enemy):
                    return LIGHT
                else:
                    return BLOCK
            else:
                return JUMP_FORWARD
                
        else:
            return FORWARD