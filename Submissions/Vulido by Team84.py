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
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    def get_thanh_strategy(self, player, enemy, player_projectiles, enemy_projectiles):

        distance = abs((get_pos(player)[0] - get_pos(enemy)[0]))

        if get_primary_skill(enemy) == 'meditate':
            hit_limit = 20
        else:
           hit_limit = 10 

        if len(enemy_projectiles) > 0:
            if get_projectile_type(enemy_projectiles[0]) == 'grenade' and abs(enemy_projectiles[0].get_pos()[0] - get_pos(player)[0]) <= 2:
                return BACK
            elif abs(enemy_projectiles[0].get_pos()[0] - get_pos(player)[0]) < 2:
                if enemy_projectiles[0].get_pos()[1] == 0:
                    if distance < 5:
                        return JUMP
                    else:
                        return JUMP_FORWARD
        
        if get_hp(player) < 100 and (not primary_on_cooldown(player)):
            return PRIMARY
        elif abs(get_pos(player)[0] - get_pos(enemy)[0]) <= 7: # and usable + not stunned
            if not secondary_on_cooldown(player):
                if get_last_move(player) and (get_secondary_skill(enemy) in ['hadoken', 'boomerang'] and get_primary_skill(enemy) != 'dash_attack'):
                    if get_last_move(player)[1] == 'cooldown' and get_past_move(player, 2)[0] == 'move' and get_past_move(player, 2)[1][0] == 0 and get_past_move(player, 2)[1][1] == 0:
                        return SECONDARY
                else:
                    return SECONDARY
            elif abs(( get_pos(enemy)[0] - get_pos(player)[0] )) == 1:
                if get_primary_skill(enemy) in ['onepunch', 'uppercut']:
                    return JUMP_BACKWARD
                else:
                    return BLOCK 
            elif (get_hp(player) - get_hp(enemy)) >= hit_limit: 
                return BACK
            else:
                return BACK        
        elif abs((get_pos(enemy)[0] - get_pos(player)[0])) > 7:
            if not secondary_on_cooldown(player) and ((get_hp(player) - get_hp(enemy)) < hit_limit):
                return FORWARD


    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        # return SECONDARY
        return self.get_thanh_strategy(player, enemy, player_projectiles, enemy_projectiles)
       



        
