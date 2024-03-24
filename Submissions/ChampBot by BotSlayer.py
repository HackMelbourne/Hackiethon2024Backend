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
        self.skill_blockable_mapping = {
            "hadoken": True,
            "boomerang": True,
            "grenade": False,
            "beartrap": False,
        }
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        distance = get_distance(player, enemy)

        # When player is under attack from coming projectiles
        for proj in enemy_projectiles:
            proj_pos = get_proj_pos(proj)
            player_pos = get_pos(player)

            # Calculate the distance between the projectile and the player
            proj_distance = ((proj_pos[0] - player_pos[0]) ** 2 + (proj_pos[1] - player_pos[1]) ** 2) ** 0.5
            if proj_distance < 3:
                if self.skill_blockable_mapping.get(proj.get_type(), False):
                    return BLOCK
                else:
                    return JUMP_FORWARD

        # THE AVOIDS
        # run awayyyy from one punch
        if (get_primary_skill(enemy) == "onepunch"):
            return BACK
        # and combos :')
        if ((get_past_move(enemy, 2) == LIGHT) and (get_past_move(enemy, 1) == LIGHT)):
            return BACK
        
        # ATTACK!
        # use dash to move away from enemy
        if (distance <= 4 and not primary_on_cooldown(player)):
            return PRIMARY
        
        # use grenade whenever possible
        if ((not secondary_on_cooldown(player)) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= seco_range(player) + 3):
            return SECONDARY
        
        # use heavy whenever possible
        if not heavy_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= 1:
            return HEAVY
        
        # if next atk is combo prefer heavy
        if ((get_past_move(player, 2) == LIGHT) and (get_past_move(player, 1) == LIGHT)):
            if not heavy_on_cooldown(player):
                return HEAVY
            
        # AGGRESIVE
        if (distance > 4):
            return FORWARD

        return LIGHT
        
