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
        for projectile in enemy_projectiles:
            projtype = get_projectile_type(projectile)
            if (projtype == Grenade):
                if get_distance(player,projectile) < 4:
                    return BACK
                else:
                    return JUMP
            elif (projtype == Hadoken):
                if get_distance(player,projectile) <= 2:
                    return JUMP_FORWARD
                else: 
                    NOMOVE
            else:
                NOMOVE



       #offense
        if primary_on_cooldown(enemy) == True and secondary_on_cooldown (enemy) == True:
            return SECONDARY_SKILL
        if get_primary_skill(enemy) == UppercutSkill and secondary_on_cooldown (enemy) == True:
            return JUMP_BACKWARD
        if get_primary_skill(enemy) == DashAttackSkill and secondary_on_cooldown (enemy) == True:
            return JUMP
        if get_primary_skill(enemy) == TeleportSkill and secondary_on_cooldown (enemy) == True:
            get_distance < 3
            return LIGHT
        if get_primary_skill(enemy) == Meditate and secondary_on_cooldown (enemy) == True:
            return LIGHT
        check_self = get_hp(player)
        if check_self < 30:
            return BACK
       
       #defence
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        print ("distance", distance)
        if distance < 3:
            return LIGHT 
        if get_hp(player) < 20 or abs(get_pos(player)[0] - get_pos(enemy)[0]) < 2:
        # Block if enemy is close and likely to attack
            if abs(get_pos(player)[0] - get_pos(enemy)[0]) == 1:
                return BLOCK
        # Move away from the enemy if possible
        elif get_pos(player)[0] < get_pos(enemy)[0]:
            return BACK
        else:
            return LIGHT

# HAVE a basic attack, special attack, basic defence, projectile defence