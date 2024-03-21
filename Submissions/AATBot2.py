# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions

# primary skill can be defensive or offensive
# secondary skills involve summoning a projectile

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# currently unsure how to enforce this...
#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
SECONDARY_SKILL = Boomerang

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


        ## for the second bot, teleporting away and throwing boomerangs... 
        ## and then also blocking if on cooldown

        ## if the enemy is going attack
        if get_landed(player):
            if self.get_x_distance(player, enemy) == 1:
                return BLOCK

        ## this is boomerang... if within range... 
        if self.get_x_distance(player, enemy) >= 1 and self.get_x_distance(player, enemy) <= 5:
            if not secondary_on_cooldown(player):
                return SECONDARY

        ## if the enemy is close then teleport away
        if self.get_x_distance(player, enemy) <= 1:
            if not primary_on_cooldown(player):
                return PRIMARY

            # move backwards away from the enemy if can't teleport
            else:
                return BLOCK

        ## code for projectiles... (thanks Ash) if oncoming then block em 
        if (len(enemy_projectiles) and abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) < 3): #incoming projectile
            return BLOCK
        
        ## if you are close to the enemy... and have gone through all of these above then move away while waiting for 
        ## skills to come back 
        if self.get_x_distance(player, enemy) <= 2:
            return BACK





    def get_x_distance(self, player, enemy):
        return abs(get_pos(player)[0] - get_pos(enemy)[0]) 
    
    
    def check_dodge_proj(self, player, enemy, projobj):
        if ((get_pos(player)[0] < get_pos(projobj)[0] < get_pos(enemy)[0]) or
            (get_pos(player)[0] > get_pos(projobj)[0] > get_pos(enemy)[0])):
            # projectile is in the way of the player to enemy
            return get_pos(player)[1] == get_pos(projobj)[1]
        return False