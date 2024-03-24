# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN
import random

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = Grenade

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

        # GokuBot fighting style
        if get_secondary_skill(enemy) == "hadoken" or get_secondary_skill(enemy) == "boomerang":
            player_pos = get_pos(player)
            enemy_pos = get_pos(enemy)

            distance_x = abs(get_pos(player)[0] - get_pos(enemy)[0])
            distance = abs(player_pos[0] - enemy_pos[0])

            # Jump back when enemy uses One Punch
            if get_last_move(enemy) is not None:
                if get_last_move(enemy)[0] == "onepunch":
                    return JUMP_BACKWARD

            # Projectile counters
            for i in enemy_projectiles:
                # Jump forward when hadoken is near
                if get_projectile_type(i) == "hadoken":
                    return JUMP_FORWARD
                # Move forward when grenade is launched
                elif get_projectile_type(i) == "grenade" and abs(get_pos(player)[0] - get_proj_pos(i)[0]) < 3:
                    return FORWARD
                # Block when boomerang is near
                elif get_projectile_type(i) == "boomerang" and abs(get_pos(player)[0] - get_proj_pos(i)[0]) == 1:
                    return BLOCK
                # Jump back when bear-trap is placed
                elif get_projectile_type(i) == "beartrap" and abs(get_pos(player)[0] - get_proj_pos(i)[0]) == 1:
                    return JUMP_BACKWARD

            # Spam grenades off cd
            if not secondary_on_cooldown(player):
                return SECONDARY

            # Dash attack when off cd and enemy within dash distance
            if not primary_on_cooldown(player) and distance_x <= 2:
                return PRIMARY

            # Light attack when enemy is stunned and within range
            if get_stun_duration(enemy) > 0 and distance <= 1:
                return LIGHT

            # Heavy attack when possible
            if distance <= 1:
                if not heavy_on_cooldown(player):
                    return HEAVY
                return LIGHT

            # Only throw grenade when player is not in air
            if get_last_move(player) is not None:
                if not secondary_on_cooldown(player) and not get_last_move(player) == JUMP:  # player not jumping
                    if distance_x != 1:
                        return SECONDARY
                    return LIGHT
                if get_last_move(enemy)[0] == "uppercut" and distance < 2:
                    return BLOCK

            # Move forward if distance is too far...
            if distance > 2 and get_secondary_skill(enemy) == "hadoken":
                return FORWARD

            # ...Otherwise, move back
            return BACK
        else:
            # WatermelonBot fighting style
            distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
            # Projectile counters
            for i in enemy_projectiles:
                # Jump forward when hadoken is near
                if get_projectile_type(i) == "hadoken":
                    return JUMP_FORWARD
                # Dash forward if grenade is near, move back if on cd
                elif (get_projectile_type(i) == "grenade") and (abs(get_pos(player)[0] - get_proj_pos(i)[0]) < 4):
                    if not get_primary_cooldown(player):
                        return PRIMARY
                    else:
                        return BACK
                # Jump to dodge boomerang
                elif (get_projectile_type(i) == "boomerang") and abs(get_pos(player)[0] - get_proj_pos(i)[0]) == 2:
                    return JUMP
                # Jump back when bear-trap is placed
                elif get_projectile_type(i) == "beartrap" and abs(get_pos(player)[0] - get_proj_pos(i)[0]) == 1:
                    return JUMP_BACKWARD

            # Specific enemy last move counters
            if get_last_move(enemy) is not None:
                if get_last_move(enemy)[0] == "dash_attack" and distance < 5:
                    return BLOCK
                if get_last_move(enemy)[0] == "onepunch" and distance < 2:
                    return JUMP_BACKWARD
                if get_last_move(enemy)[0] == "uppercut" and distance < 2:
                    return BLOCK

            # Heavy attack when possible
            if distance <= 1:
                if not heavy_on_cooldown(player):
                    return HEAVY
                return LIGHT

            # Dash attack when off cd and enemy within dash distance
            if (not primary_on_cooldown(player)) and (distance <= 2):
                return PRIMARY

            # Throw grenade when in range
            if distance < 7:
                if not secondary_on_cooldown(player):
                    return SECONDARY

            # Move forward if distance is too far...
            if distance > 2:
                return FORWARD

            # ...Otherwise, move back
            return BACK
