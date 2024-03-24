# bot code goes here
import random

from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import (
    HP,
    LEFTBORDER,
    RIGHTBORDER,
    LEFTSTART,
    RIGHTSTART,
    PARRYSTUN,
)

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = Meditate
SECONDARY_SKILL = SuperSaiyanSkill

# constants, for easier move return
# movements
JUMP = ("move", (0, 1))
FORWARD = ("move", (1, 0))
BACK = ("move", (-1, 0))
JUMP_FORWARD = ("move", (1, 1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

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
        self.clock = 0
        self.timing = 0
        self.enemy_buff = -1

    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary

    def dogde_from_projectile(self, player_pos, enemy_projectiles):
        if enemy_projectiles is not None:
            for enemy_projectile in enemy_projectiles:
                dist_danger = abs(player_pos[0] - get_proj_pos(enemy_projectile)[0])
                if dist_danger <= 2 and get_proj_pos(enemy_projectile)[1] == 0:
                    return True
        return False

    def combo(self, player, enemy):
        if get_stun_duration(enemy) == 0 and get_last_move(player)[0] != "block":
            point = 1
            if self.enemy_buff > 0:
                point += 3
            if get_hp(player) > 80:
                point -= 4
            if not heavy_on_cooldown(enemy):
                point += 3
            if get_primary_skill(enemy) == "uppercut" and not primary_on_cooldown(
                enemy
            ):
                point += 4
            if get_secondary_skill(enemy) == "grenade" and not secondary_on_cooldown(
                enemy
            ):
                point -= 4
            if get_past_move(enemy, 1)[0] == "light":
                point += 4
            if random.randint(0, 6) < point:
                return BLOCK
        if not heavy_on_cooldown(player):
            return HEAVY
        return LIGHT

    # Use buff: meditate and supersyran
    def strategy(self, player, enemy, enemy_projectiles):
        player_hp = get_hp(player)
        player_pos = get_pos(player)
        enemy_pos = get_pos(enemy)
        enemy_last_move = get_last_move(enemy)
        distance = abs(player_pos[0] - enemy_pos[0])

        if enemy_projectiles is not None:
            for enemy_projectile in enemy_projectiles:
                dist_danger = abs(player_pos[0] - get_proj_pos(enemy_projectile)[0])
                if dist_danger <= 1 and get_proj_pos(enemy_projectile)[1] == 0:
                    return (
                        JUMP if get_primary_skill(enemy) != "onepunch" else JUMP_FORWARD
                    )
        if enemy_last_move and enemy_last_move[0] == "grenade":
            return JUMP_FORWARD

        if not primary_on_cooldown(player) and (player_hp <= 80 or self.clock > 110):
            return PRIMARY
        else:
            if distance < 2:
                if get_secondary_skill(enemy) == "boomerang":
                    if not primary_on_cooldown(enemy) and not heavy_on_cooldown(player):
                        return HEAVY
                if (
                    enemy_last_move[0] == "onepunch"
                    and get_past_move(enemy, 1)[1] == "startup"
                ):
                    return JUMP
                if self.timing:
                    self.timing -= 1
                    return BLOCK
                if not secondary_on_cooldown(player):
                    return SECONDARY
                else:
                    return self.combo(player, enemy)
            if distance >= 2:
                if distance == 2:
                    if enemy_last_move[0] == "move":
                        return LIGHT
                    self.timing = 1
                if (
                    enemy_last_move
                    and enemy_last_move[0] == "onepunch"
                    and get_past_move(enemy, 1)[1] == "startup"
                ):
                    return BACK
                return FORWARD

    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        self.clock += 1
        if get_last_move(enemy) and get_last_move(enemy)[0] == "super_saiyan":
            self.enemy_buff = 0
        if 0 <= self.enemy_buff < 20:
            self.enemy_buff += 1
        else:
            self.enemy_buff = -1
        return self.strategy(player, enemy, enemy_projectiles)
