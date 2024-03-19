# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions

# primary skill can be defensive or offensive
# secondary skills involve summoning a projectile

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

# currently unsure how to enforce this...
#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
SECONDARY_SKILL = Grenade

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
    # perfectly spaces hadokens

    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.go_left = True
        self.proj_end = 0
        self.avoid_proj = False
        
    def init_player_skills(self):
        return self.primary, self.secondary
    
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):

        # triggering avoid projectile (only avoids hadokens) mode
        if len(enemy_projectiles) > 0 and get_projectile_type(enemy_projectile) == "hadoken":
            enemy_projectile = enemy_projectiles[0]
            self.avoid_proj = True

            if get_pos(player)[0] < get_pos(enemy)[0]:
                self.go_left = True
            else:
                self.go_left = False
            if self.go_left:
                
                self.proj_end = get_proj_pos(enemy_projectile) - seco_range(enemy)
            else:
                self.proj_end = get_proj_pos(enemy_projectile) + seco_range(enemy)
        else:
            self.avoid_proj = False

        distance_from_enemy = get_distance(player, enemy)

        if self.avoid_proj:
            # trying to avoid projectile
            if self.go_left and get_pos(player) > self.proj_end and self.proj_end >= 0:
                return BACK
            if not self.go_left and get_pos(player) < self.proj_end and self.proj_end <= 15:
                return BACK
            
            distance_from_proj = abs(get_pos(player)[0] - get_proj_pos(enemy_projectile)[0])
            if distance_from_proj == 1:
                return BLOCK
            
            if distance_from_enemy <= seco_range(player):
                return SECONDARY
            
            if distance_from_enemy == 1:
                return JUMP_FORWARD
            
            return BACK
        else:
            if distance_from_enemy <= seco_range(player):
                return SECONDARY
            return FORWARD

def get_distance(player1, player2):
    return abs(get_pos(player1)[0] - get_pos(player2)[0])