# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
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

# skills
PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

# no move, aka no input
NOMOVE = "NoMove"

class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.moves = FORWARD,LIGHT,
        self.moves_iter = iter(self.moves)
        self.doScripted = True

        
    def init_player_skills(self):
        return self.primary, self.secondary
    
    #MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):

        # PRIMARY_SKILL = OnePunchSkill
        # SECONDARY_SKILL = Grenade
        try:
            return next(self.moves_iter)
        except StopIteration:
            return NOMOVE
  
        if self.doScripted:
            try:
                nxt = next(self.moves_iter)
                print(nxt)
                return nxt
            except StopIteration:
                return NOMOVE

        if get_pos(player)[0] == 0 or get_pos(player)[0] == 30:
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
    
