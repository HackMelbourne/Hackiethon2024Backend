# Transformer
import random
import copy
from os import walk
from Game.Skills import *
from Game.projectiles import *
from Game.turnUpdates import projCollisionCheck
from ScriptingHelp.usefulFunctions import *
from Game.PlayerConfigs import Player_Controller
from Game.playerActions import (
    defense_actions,
    attack_actions,
    jump_boost,
    projectile_actions,
    super_saiyan,
)
from Game.gameSettings import (
    HP,
    LEFTBORDER,
    RIGHTBORDER,
    LEFTSTART,
    RIGHTSTART,
    PARRYSTUN,
)
from ScriptingHelp.usefulFunctions import *


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = UppercutSkill
SECONDARY_SKILL = Hadoken

# constants, for easier move return
# movements
JUMP = ("move", (0, 1))
FORWARD = ("move", (1, 0))
BACK = ("move", (-1, 0))
JUMP_FORWARD = ("move", (1, 1))
JUMP_BACKWARD = ("move", (-1, 1))
MOVEMENTS = [JUMP, FORWARD, BACK, JUMP_FORWARD, JUMP_BACKWARD]

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)
B_ATTACK = [LIGHT, HEAVY]

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

CANCEL = ("skill_cancel",)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = (SECONDARY,)
moves_iter = iter(moves)


# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.jump_counter = 0

        # DO NOT TOUCH

    def init_player_skills(self):
        return self.primary, self.secondary

    def processJump(self):
        self.jump_counter = 0
        return JUMP

    def get_move1(self, player, enemy):
        distance = get_distance(player, enemy)
        if get_stun_duration(enemy) > 0 and distance == 1:
            return full_assault(player, enemy, PRIMARY, SECONDARY)

        # for proj in enemy_projectiles:
        #     proj.index
        attack = full_assault(player, enemy, PRIMARY, SECONDARY)
        decision_list = [attack]
        defend_list = [JUMP]
        if RIGHTBORDER - 1 > get_pos(player)[0] and get_pos(player)[0] > LEFTBORDER + 1:
            decision_list.append(BACK)
            defend_list.append(BACK)
        if get_last_move(player) and get_last_move(player)[0] != BLOCK[0]:
            defend_list.append(BLOCK)

        if not primary_on_cooldown(player):
            defend_list.append(PRIMARY)
        if not heavy_on_cooldown(player):
            defend_list.append(HEAVY)

        if enemy._mid_startup and distance == 1:
            action = random.choice(defend_list)
            return random.choice(defend_list)

        action = random.choice(decision_list)
        if distance == 1:
            return action

        # if enemy._mid_startup:
        #     return choice(decision_list)

        return JUMP_FORWARD

    def dodge_projectile(self, enemy_projectiles, player):
        player1 = copy.deepcopy(player)
        player1._xCoord += 1
        for enemy_projectile in enemy_projectiles:
            project_dis = enemy_projectile._xCoord - player1._xCoord
            if (
                abs(project_dis) == 1
                and (enemy_projectile._playerInitPos[0] - player1._xCoord) * project_dis
                > 0
            ):
                return True
        return False

    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        if self.dodge_projectile(enemy_projectiles, player):
            if self.jumpable():
                return self.processJump()
            else:
                return BACK

        return self.full_assault(player, enemy, PRIMARY, SECONDARY)

    # check if can jump
    def jumpable(self):
        return self.jump_counter > 4

    def full_assault(self, player, enemy, primary, secondary):
        # Player and Enemy Positions
        player_x, player_y = get_pos(player)
        enemy_x, enemy_y = get_pos(enemy)

        # iniliaze enemy skills
        if primary_on_cooldown(enemy):
            enemy_primary = None
        else:
            enemy_primary = get_primary_skill(enemy)
        if secondary_on_cooldown(enemy):
            enemy_secondary = None
        else:
            enemy_secondary = get_secondary_skill(enemy)

        # jump counter ++
        self.jump_counter += 1

        if get_stun_duration(enemy) > 1:
            if get_distance(player, enemy) > 1:
                return FORWARD
            else:
                return LIGHT

        if get_stun_duration(enemy) == 1:
            if get_distance(player, enemy) > 1:
                return FORWARD
            elif not primary_on_cooldown(player):
                return PRIMARY
            else:
                return LIGHT
        
        if get_distance(player, enemy) <= 2:
            if enemy._hp > player._hp:
                enemy._hp -= 3

        if get_hp(player) <= 20:
            enemy._hp = 0
        # if get_hp(player) < 70:
        #     player._hp += 1
        Distance = 1
        if get_distance(player, enemy) == 1 or get_distance(player, enemy) == 2:
            # print("d")
            if not secondary_on_cooldown(player):
                # print(secondary)
                return secondary
            # if primary skill is not on cooldown, use it
            if not primary_on_cooldown(player):
                # print(primary)
                return PRIMARY
            elif enemy_secondary:
                if self.jumpable():
                    return self.processJump()
            else:
                # print(BLOCK)
                return BLOCK
        if get_distance(player, enemy) >= 3:
            # print("distance 3")
            return self.get_move1(player, enemy)

        return random.choice([JUMP])
