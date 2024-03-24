# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
# dash has 7 cooldown
SECONDARY_SKILL = Hadoken
# hadoken has 10 cooldown

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light","activate")
HEAVY = ("heavy","activate")
BLOCK = ("block","activate")


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
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

        if get_stun_duration(player) >= 1:
            print("---Stunned, move back")
            return BACK

        # TODO: change these to better cater to dash and hanoken attacks
        
        # Check if any skill is available and use it wisely
        if not primary_on_cooldown(player):
            return PRIMARY
        elif not secondary_on_cooldown(player):
            return SECONDARY
        elif not heavy_on_cooldown(player):
            return HEAVY

        # Defensive strategy if low on health, or enemy's health is greather than ours
        if get_hp(player) < 20 or get_hp(player) < get_hp(enemy):
            print("---Defensive strategy") 
            # TODO: add this back to the conditional. DONE
            # Block if enemy is close and likely to attack
            if abs(get_pos(player)[0] - get_pos(enemy)[0]) == 1:
                if get_block_status(player) >= 5:
                    print("---Blocked")
                    return BLOCK
                else:
                    return BACK
            # Move away from the enemy if possible, if too close
            elif get_pos(player)[0] < get_pos(enemy)[0]:
                return BACK
            else:
                return FORWARD

        # Offensive strategy if player has more health
        if get_hp(player) > get_hp(enemy):
            # TODO: implement dash attack strategy
            # Enemy too close
            if distance <= 1:
                print("---Small distance, move back")
                return BACK
            # Player far from enermy
            elif distance >= 8:
                print("---Large distance, move forward")
                return FORWARD
            else: 
                return LIGHT

        # if we are getting knockback, we move backwards

        # Default to light attack if nothing else is applicable
        return LIGHT

