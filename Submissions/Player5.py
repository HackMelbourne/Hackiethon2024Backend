# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = UppercutSkill
SECONDARY_SKILL = SuperArmorSkill

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

# Don't touch
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    def init_player_skills(self):
        return self.primary, self.secondary
    
    #MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        # PRIMARY_SKILL is UppercutSkill
        # SECONDARY SKILL is IceWall
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

        if prim_range(player) <= distance:
            if not primary_on_cooldown(player):
                return PRIMARY

        if not secondary_on_cooldown(player):
            return SECONDARY

        if distance == 1:
            if not heavy_on_cooldown(player):
                return HEAVY
            return LIGHT

        return FORWARD
