# bot code goes here
from Skills import *
from projectiles import *
from Submissions.usefulFunctions import *
from playerActions import defense_actions, attack_actions, projectile_actions

# primary skill can be defensive or offensive
# secondary skills involve summoning a projectile

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

# currently unsure how to enforce this...
#TODO FOR USER: Set primary and secondary skill here
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

        # ken's ai
        # plan
        # landed: cant move, so block : might lead to parry
        # if within range and stunned, heavy
        # if projectile is within one xcoord of player, jump forward: hadoken or lasso
        # if enemy is at least 3 blocks away, move forward
        # if ice wall between player and enemy, destroy with hadoken
        # if bear trap within 2 xcoords of player where theyre facing, jump forward over
        # if enemy is 4 blocks away: dash attack, else move if on cooldown
        # if enemy charging up with heavy, ready to parry
        # if enemy 1 block away, ready to parry
        
        if get_landed(player):
            if self.get_x_distance(player, enemy) == 1:
                # enemy likely to attack, so parry
                return BLOCK
            else:
                return NOMOVE # get ready
            
        # at this point: player can take any action
        if (self.get_x_distance(player, enemy) == 1):
            if get_stun_duration(enemy) > 1:
                # enough ticks for a heavy attack
                return HEAVY
            elif get_stun_duration(enemy) == 1:
                # only 1 tick on stun, so do light
                return LIGHT
            else:
                # no stun, could potentially attack
                if get_past_move(enemy, 1) == BLOCK:
                    # fuck it attack
                    return HEAVY
                return BLOCK
        
        # at this point, player and enemy are at least 2 blocks apart
        if self.get_x_distance(player, enemy) < prim_range(player):
            # move
            # try to dodge projectiles
            if len(enemy_projectiles):
                enem_proj = enemy_projectiles[0]
                if (self.get_x_distance(player, enem_proj) <= 2 and 
                    self.check_dodge_proj(player, enemy, enem_proj)):
                    # should jump over
                    if get_secondary_skill(enemy) == "icewall":
                        # shit, cant jump over it
                        if not secondary_on_cooldown(player):
                            return SECONDARY
                        
                    return JUMP_FORWARD
                else:
                    # proj is a bit far...
                    if not primary_on_cooldown(player):
                        return PRIMARY
            else:
                # no projectiles, just move closer
                return FORWARD
        elif self.get_x_distance(player, enemy) ==  prim_range(player):
            if not primary_on_cooldown(player):
                return PRIMARY
                        
        elif self.get_x_distance(player, enemy) == prim_range(player):
            # dash attack just within range, use it for max efficiency
            return PRIMARY
        
        return HEAVY
        
        
        
    def get_x_distance(self, player, enemy):
        return abs(get_pos(player)[0] - get_pos(enemy)[0]) 
    
    def check_dodge_proj(player, enemy, projobj):
        if ((get_pos(player)[0] < get_pos(projobj)[0] < get_pos(enemy)[0]) or
            (get_pos(player)[0] > get_pos(projobj)[0] > get_pos(enemy)[0])):
            # projectile is in the way of the player to enemy
            return get_pos(player)[1] == get_pos(projobj)[1]
        return False
        
        
