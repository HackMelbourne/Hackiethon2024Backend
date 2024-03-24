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
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        if get_primary_skill(enemy) == "onepunch" and (get_secondary_skill(enemy) == "super_armor" or get_secondary_skill(enemy) == "super_saiyan"):
            if get_stun_duration(enemy) != 0:
                return LIGHT
            if not secondary_on_cooldown(player):
                return SECONDARY  
            if not primary_on_cooldown(player) and get_hp(player) < 100:
                return PRIMARY
            if distance <= 1 and get_primary_skill(enemy) == "onepunch" and get_primary_cooldown(enemy) == 0:

                return JUMP_FORWARD
            if distance <= 1 and get_last_move(player) != BLOCK and get_past_move(player, 2) != BLOCK and get_past_move(player, 3) != BLOCK and get_past_move(player, 4) != BLOCK and get_past_move(player, 5) != BLOCK:
                return BLOCK
            if distance <= 1 and not heavy_on_cooldown(player):
                return HEAVY 

            if distance <= 6:
                return BACK
            else:
                return FORWARD
        if distance <= 4 and get_primary_skill(enemy) == "dash_attack" and get_primary_cooldown(enemy) == 0 and get_last_move(player) != JUMP and get_past_move(player,2) != JUMP and get_past_move(player,3) != JUMP and get_past_move(player,4) != JUMP and get_past_move(player,5) != JUMP  and get_past_move(player,6) != JUMP:
            return JUMP
        if get_secondary_skill(enemy) == "hadoken":
           if enemy_projectiles != []:   
            for i in enemy_projectiles:
                haduken_pos = get_proj_pos(i)
                if haduken_pos[0] - get_pos(player)[0] <2:
                    return JUMP_FORWARD
        if get_stun_duration(enemy) != 0:
            return LIGHT
        if distance <= 1 and get_primary_skill(enemy) == "onepunch" and get_primary_cooldown(enemy) == 0:
            return JUMP_FORWARD
        if not secondary_on_cooldown(player):
            return SECONDARY  
        if not primary_on_cooldown(player) and get_hp(player) < 100:
            return PRIMARY
        if distance <= 1 and get_last_move(player) != BLOCK and get_past_move(player, 2) != BLOCK and get_past_move(player, 3) != BLOCK and get_past_move(player, 4) != BLOCK and get_past_move(player, 5) != BLOCK:
            return BLOCK
        if distance <= 1 and not heavy_on_cooldown(player):
            return HEAVY 


        return FORWARD


        
