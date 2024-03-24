# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = BearTrap

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
        self.time = 0
        self.counter = 0
        self.enemyBlocks = 0
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    

    def tryBack(self, player, enemy, enemy_projectiles):
        if get_pos(player)[0] == 0 or get_pos(player)[0] == 15:
            if get_pos(player)[1] >= 1:
                return PRIMARY
            if not primary_on_cooldown(player):
                return JUMP
            return BLOCK
        
        if get_past_move(player, 1) == BACK and get_past_move(player, 2) == BACK and get_past_move(player, 3) == BACK:
            if not secondary_on_cooldown(player):
                return SECONDARY

        if get_secondary_skill(enemy) == "beartrap":
            try:
                if abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) <= 1 and get_proj_pos(enemy_projectiles[0])[1] == get_pos(player)[1]:
                    return JUMP_BACKWARD
            except:
                return BACK
        else:
            return BACK
        

    def tryForward(self, player, enemy, enemy_projectiles):
        if get_secondary_skill(enemy) == "beartrap":
            try:
                if abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) <= 1 and get_proj_pos(enemy_projectiles[0])[1] == get_pos(player)[1]:
                    return JUMP_FORWARD
            except:
                return FORWARD
        else:
            return FORWARD
        
    def tryDash(self, player, enemy, enemy_projectiles):
        if get_secondary_skill(enemy) == "bear_trap":
            try:
                if abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) <= 5 and get_proj_pos(enemy_projectiles[0])[1] == get_pos(player)[1]:
                    return JUMP
            except:
                return PRIMARY
        else:   
            return PRIMARY
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        self.time += 1
        if get_secondary_skill(enemy) == "hadoken":
            try:
                if abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) <= 2:
                    # check for onepunch
                    if get_primary_skill(enemy) == "onepunch":
                        return JUMP
                    return JUMP_FORWARD
                
            except IndexError as e:
                # print(e)
                pass

        if get_secondary_skill(enemy) == "grenade":
            try:
                if abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) <= 3:
                    return BACK
                
            except IndexError as e:
                # print(e)
                pass
            
        if get_secondary_skill(enemy) == "boomerang":
            try:
                if abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) <= 2:
                    # check for onepunch
                    if get_primary_skill(enemy) == "onepunch":
                        return JUMP
                    return JUMP_FORWARD
                
            except IndexError as e:
                # print(e)
                pass
        
        
        if get_stun_duration(enemy) > 0:
            if get_distance(player, enemy) > 1:
                return self.tryForward(player, enemy, enemy_projectiles)
            return heavy_combo(player, enemy)

        if get_primary_skill(enemy) == "onepunch":
            if get_pos(player)[0] == 0 or get_pos(player)[0] == 15:
                if get_pos(player)[1] >= 0 and not primary_on_cooldown(player) and get_distance(player, enemy) < 3:
                    return PRIMARY
                # if not primary_on_cooldown(player):
                #     return JUMP_FORWARD
                return BLOCK
            
            if get_distance(player, enemy) < 2:
                return self.tryBack(player, enemy, enemy_projectiles)
            if get_distance(player, enemy) > 2:
                return self.tryForward(player, enemy, enemy_projectiles)
            if get_distance(player, enemy) == 2:
                if not primary_on_cooldown(player):
                    return PRIMARY
                return self.tryBack(player, enemy, enemy_projectiles)
        
        if get_distance(player, enemy) <= 1:
            if get_pos(player)[0] == 0 or get_pos(player)[0] == 15:
                if get_primary_skill(enemy) == "uppercut":
                    return BLOCK
                if get_pos(player)[1] >= 0 and not primary_on_cooldown(player):
                    return PRIMARY
                # if not primary_on_cooldown(player):
                #     return JUMP_FORWARD
                return BLOCK

            if self.counter < 3:
                self.counter += 1
                # print("Blocking")
                return BLOCK
            elif self.counter >= 3:
                self.counter = 0

                if get_past_move(enemy, 1)[0] == 'block':
                    self.enemyBlocks = 1
                
                if not secondary_on_cooldown(player) and get_pos(player)[1] == get_pos(enemy)[1]:
                    return SECONDARY
                
                if self.enemyBlocks == 1:
                    return self.tryBack(player, enemy, enemy_projectiles)
                
                return heavy_combo(player, enemy)
            
        self.counter = 0

        if get_distance(player, enemy) < 3:
            return self.tryBack(player, enemy, enemy_projectiles)

        if get_distance(player, enemy) <= 4:
            if not primary_on_cooldown(player):
                return self.tryDash(player, enemy, enemy_projectiles)
            return self.tryBack(player, enemy, enemy_projectiles)

        if get_distance(player, enemy) < 8:
            return self.tryForward(player, enemy, enemy_projectiles)
        
        return JUMP_FORWARD


        



        
