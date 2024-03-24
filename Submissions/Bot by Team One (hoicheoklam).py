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
CANCEL = ("skill_cancel", )

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = Meditate
        self.secondary = Hadoken
    
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager  
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        primary_skill = get_primary_skill(enemy)
        if get_last_move(enemy) == None:
            return BLOCK
        
        if get_hp(player) < 80 and not primary_on_cooldown(player):
            return PRIMARY
        #DEFENSIVE FUNCTION AGANIST SKILLS
        if get_primary_skill(enemy) == "dash_attack":
            if get_last_move(enemy) == (('dash_attack', 'startup')):
                if get_distance(player,enemy) == 5:
                   return BACK
                elif 1 < get_distance(player,enemy) < 5 and primary_skill != "uppercut" and not primary_on_cooldown(enemy):
                    return JUMP_BACKWARD
                elif get_distance(player,enemy) == 1:
                    return HEAVY
                elif not secondary_on_cooldown(player):
                    return SECONDARY
                elif get_distance(player,enemy) == 6:
                    return BACK
                else:
                    return None
                
            #ONE PUNCH
        if get_primary_skill(enemy) == "onepunch":
            if get_last_move(enemy) == (('onepunch', 'startup')):
                if get_distance(player, enemy) == 2:
                    return BACK
                #jump 
                elif get_distance(player, enemy) == 1 and primary_skill != "uppercut" and not primary_on_cooldown(enemy):
                    return JUMP_BACKWARD
                #hadoken
                elif 2 < get_distance(player, enemy) < 8 and not secondary_on_cooldown(player):
                    return SECONDARY
                else:
                    return FORWARD
                
            #BEAR TRAP
        if get_secondary_skill(enemy) == "beartrap":
            if get_last_move(enemy) == (('beartrap', 'activate')):
                if get_distance(player, enemy) <= 2 and primary_skill != "uppercut" and not primary_on_cooldown(enemy):
                    return JUMP_BACKWARD
                elif 3 <= get_distance(player, enemy) < 8 and not secondary_on_cooldown(player):
                    return SECONDARY
                else:
                    return FORWARD
                
        #Grenade
        if get_secondary_skill(enemy) == "grenade":
            if get_last_move(enemy) == (('grenade', 'activate')):  
                if get_distance(player, enemy) == 3:
                    return JUMP_BACKWARD
                elif get_distance(player, enemy) == 4:
                    return BACK
                elif get_distance(player, enemy) == 2 and primary_skill != "uppercut" and not primary_on_cooldown(enemy):
                    return JUMP_FORWARD
                elif 5 <= get_distance(player, enemy) < 8 and not secondary_on_cooldown(player):
                    return SECONDARY
                else:
                    return FORWARD
                
        if get_distance(player, enemy) < 8:
           if not secondary_on_cooldown(player):
               return SECONDARY
           else:
               if get_distance(player, enemy) > 1:
                   return FORWARD
               else:
                   return LIGHT
        elif get_distance(player, enemy) >= 8:
            return FORWARD
        