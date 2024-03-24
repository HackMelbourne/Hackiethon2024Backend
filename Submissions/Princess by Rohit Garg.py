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

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.hp_tracker = 100
        self.enemy_last_known_pos = 0

    def init_player_skills(self):
        return self.primary, self.secondary

    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        current_hp = get_hp(player)
        distance = get_distance(player, enemy)
        my_pos = get_pos(player)[0]
        enemy_pos = get_pos(enemy)[0]
        getting_close = (self.enemy_last_known_pos < my_pos) or (enemy_pos < my_pos)

        action = LIGHT
        
        if (current_hp < self.hp_tracker - 10 or getting_close) and not primary_on_cooldown(player):
            self.hp_tracker = current_hp
            action = PRIMARY
        elif distance <= 4 and not secondary_on_cooldown(player):
            action = SECONDARY
        elif distance == 1 and not heavy_on_cooldown(player):
            action = HEAVY
        else:
            action = LIGHT

        self.enemy_last_known_pos = enemy_pos
        self.my_last_pos = my_pos
        return action