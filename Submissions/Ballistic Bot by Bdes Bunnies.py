# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN

PRIMARY_SKILL = OnePunchSkill
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
CANCEL = ("skill_cancel", )

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)

class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary

    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):

        # calculate distance between enemy and player
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        grenade_range = 7

        # go offensive
        if get_hp(player) > 35:
            if not secondary_on_cooldown(player): # attack strategy based on grenade
                if distance > 1:
                    if distance < grenade_range:
                        return SECONDARY 
                    elif distance > grenade_range:
                        return FORWARD # getting into range of grenade
                    elif distance > 1 and not primary_on_cooldown(player):
                        return FORWARD # goes in for a primary attack
                elif distance == 1 or distance == 0:
                    if primary_on_cooldown(player):
                        return BACK
                    elif not primary_on_cooldown(player):
                        return PRIMARY
            elif secondary_on_cooldown(player): # when grenade is cooldown
                if distance > 2:
                    if primary_on_cooldown(player):
                        return BACK
                    elif not primary_on_cooldown(player):
                        return FORWARD
                elif distance == 1 or distance == 0:
                    if not primary_on_cooldown(player) and not heavy_on_cooldown(player):
                        return PRIMARY
                    elif not primary_on_cooldown(player) and heavy_on_cooldown(player):
                        return PRIMARY
                    elif primary_on_cooldown(player) and not heavy_on_cooldown(player):
                        return HEAVY
                    elif primary_on_cooldown(player) and heavy_on_cooldown(player):
                        return LIGHT
                elif distance == 2:
                    return LIGHT
        
        # go defensive when low health
        elif get_hp(player) <= 35:
            if distance == 1 or distance == 0:
                if not primary_on_cooldown(player):
                    return PRIMARY
                elif primary_on_cooldown(player) and not heavy_on_cooldown(player):
                    return HEAVY
                elif primary_on_cooldown(player) and heavy_on_cooldown(player):
                    return LIGHT
            elif distance > 1:
                if not secondary_on_cooldown(player):
                    if distance < ((grenade_range // 2) + 1):
                        return BACK
                    else:
                        return SECONDARY
                                             
        return BLOCK
