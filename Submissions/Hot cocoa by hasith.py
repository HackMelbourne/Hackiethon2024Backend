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
        player_pos = get_pos(player)[0]
        player_hp = get_hp(player)
        enemy_hp = get_hp(enemy)
        health_difference = abs(player_hp - enemy_hp)

        distance_to_projectile = 100
        if len(enemy_projectiles) != 0:
            distance_to_projectile = abs(get_proj_pos(enemy_projectiles[0])[0] - player_pos)

        if distance_to_projectile < 3:
            if not primary_on_cooldown(player):
                return PRIMARY
            else:
                return BLOCK
        
        if (player_pos == 15 or player_pos == 0) and distance < 4:
            return PRIMARY

        if not primary_on_cooldown(player) and distance <= prim_range(player) and get_secondary_skill(enemy) != "grenade":
            return PRIMARY

        if distance < 2:
            if not heavy_on_cooldown(player):
                return HEAVY
            else:
                return LIGHT
        
        if not secondary_on_cooldown(player):
            return SECONDARY

        if player_hp <= enemy_hp:
            return FORWARD
        
        elif player_hp > enemy_hp:
            return BACK
    

        
        
        
        
        
        
        
        
        
                
        
