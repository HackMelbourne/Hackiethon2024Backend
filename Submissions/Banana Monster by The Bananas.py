# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport (6 cd, 10 hor), Super Saiyan* (str++, 40 cd, lasts 20 ticks), Meditate (heals 20 hp, 20 cd), Dash Attack (moves 5 towards enemy, 7 cd, 5 dmg), Uppercut (5 cd, 7 dmg, 1 hor, 1 ver), One Punch* (10 cd, 20 dmg, 1 hor)
# SECONDARY CAN BE : Hadoken (10 cd, 10 dmg, 7 hor), Grenade (12 cd, 20 dmg, 3 hor, 1 vert), Boomerang* (14 cd, 8 dmg, 5 hor), Bear Trap (15 cd, 10 dmg, 1 hor)
# super armor* (strong armour, 20 ticks, 40 cd), super jump* (jump higher, 20 ticks, 30 cd)
# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = Meditate
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
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        # heal when health is less than or equal to 80 
        hp = get_hp(player)
        if hp <= 80 and not primary_on_cooldown(player):
            return PRIMARY
         
        # when y pos is same and abs(distance) is one
        if get_pos(player)[1] == get_pos(enemy)[1] and abs(get_pos(player)[0] - get_pos(enemy)[0]) == 1:
            # when within range and not on cd, use skill
            if not secondary_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= seco_range(player):
                return SECONDARY
            # when not on cd and distance is less than or equal to 1
            if not heavy_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= 1:
                return HEAVY
            if secondary_on_cooldown and get_pos(player)[0] - get_pos(enemy)[0] > 0: # if skill is on cd and player is on the right of enemy
                return FORWARD
            elif secondary_on_cooldown and get_pos(player)[0] - get_pos(enemy)[0] < 0: # if skill is on cd and player is on the left of enemy
                return BACK
            else:
                return LIGHT
        
        # when player's health is higher, decrease distance
        if get_hp(player) > get_hp(enemy):
            if abs(get_pos(player)[0] - get_pos(enemy)[0]) > 1:
                if get_pos(player)[0] < get_pos(enemy)[0]:
                    return FORWARD
                else:
                    return BACK
            else:
                return SECONDARY
         
        # if shield no longer exists, block
        block_hp = get_block_status(player)
        if block_hp == 0:
            return BLOCK
        else: 
            return SECONDARY