# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
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
        # calculate distance between enemy and player
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        enemy_primary = get_primary_skill(enemy)
        enemy_secondary = get_secondary_skill(enemy)

        if distance == 1 and not primary_on_cooldown(player):
            return PRIMARY
        elif distance == 1 and primary_on_cooldown(player):
            return LIGHT

        if distance > 1 and distance <= 7 and not secondary_on_cooldown(player):
            return SECONDARY
        
        if distance == 1 and primary_on_cooldown(player):
            # if enemy has any skill that attacks within one distance
            if enemy_primary == UppercutSkill and not primary_on_cooldown(enemy):
                return BLOCK
            elif enemy_primary == OnePunchSkill and not primary_on_cooldown(enemy):
                return JUMP_BACKWARD
            

        return FORWARD