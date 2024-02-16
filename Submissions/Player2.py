# bot code goes here
from Skills import *
from projectiles import *


#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = UppercutSkill
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


# skills
prim = PRIMARY_SKILL(None)
second = SECONDARY_SKILL(None)

PRIMARY = (prim.get_skillname(),)
SECONDARY = (second.get_skillname(),)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)


def init_player_skills():
    return PRIMARY_SKILL, SECONDARY_SKILL
 
#MAIN FUNCTION that returns a single move to the game manager
def get_move():
    try:
        return next(moves_iter)
    except StopIteration:
        return NOMOVE
    
    
    