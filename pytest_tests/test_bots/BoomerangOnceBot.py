# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *

# primary skill can be defensive or offensive
# secondary skills involve summoning a projectile

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

# currently unsure how to enforce this...
#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
SECONDARY_SKILL = Boomerang

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
CANCEL = ('skill_cancel',)
# for testing
moves = SECONDARY,
moves_iter = iter(moves)

SECONDARYREV = (SECONDARY[0], True)

class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.hasWalked = False
        self.hasUsedSkill = False
        self.moves = [BACK, SECONDARY, NOMOVE, NOMOVE, SECONDARY, BACK, BACK, BACK, SECONDARY]
        self.itermoves = iter(self.moves)
        
    def init_player_skills(self):
        return self.primary, self.secondary
    
    #MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        try:
            return next(self.itermoves)
        except StopIteration:
            return NOMOVE
        if not self.hasWalked:
            self.hasWalked = True
            return FORWARD 
        if not self.hasUsedSkill:
            self.hasUsedSkill = True
            return SECONDARY
        return NOMOVE     