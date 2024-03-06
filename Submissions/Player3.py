# bot code goes here
from Skills import *
from projectiles import *
from Submissions.usefulFunctions import *

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
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

# skills
PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

# no move, aka no input
NOMOVE = "NoMove"


class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    def init_player_skills(self):
        return self.primary, self.secondary
    
    #MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        # PRIMARY_SKILL is OnePunchSkill
        # SECONDARY SKILL is Grenade
        
        if get_pos(player)[0] == 0 or get_pos(player)[0] == 15:
            return JUMP_FORWARD

        if not secondary_on_cooldown(player):
            return SECONDARY


        if (len(enemy_projectiles) > 0 and abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) < 3):
            return JUMP

        if abs(get_pos(player)[0] - get_pos(enemy)[0]) <= prim_range(player):
            if not primary_on_cooldown(player):
                return PRIMARY
            return BACK

        if abs(get_pos(player)[0] - get_pos(enemy)[0]) < 5:
            return BACK
        else:
            return FORWARD
    