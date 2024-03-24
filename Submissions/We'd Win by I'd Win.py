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
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        print(f"player 1 last move is {get_last_move(player)}")

        # get distance between player and enemy at this tick
        distance = get_distance(player, enemy)
        esecondary = get_secondary_skill(enemy)

        # get current move and previous 7 moves to check if projectile active
        last_emove = get_last_move(enemy)
        prev_emoves = []
        for i in [1,8]:
            prev_emoves.append(get_past_move(enemy, i))

        # Dodge projectiles
        if enemy_projectiles:
            eproj_pos = get_proj_pos(enemy_projectiles[0])[0]
            if esecondary == "hadoken":
                if abs(eproj_pos - get_pos(player)[0]) < 2:
                    return JUMP
            elif esecondary == "grenade":
                if abs(eproj_pos - get_pos(player)[0]) < 5:
                    return BACK
            elif esecondary == "boomerang":
                if abs(eproj_pos - get_pos(player)[0]) < 2:
                    return JUMP

        
        # Dodge dash attack
        if (last_emove != None) and (last_emove[0] == "dash_attack"):
            if get_distance(player, enemy) < 6:
                return JUMP
            
        # Dodge One Punch
        if (last_emove != None) and (last_emove[0] == "onepunch"):
            if get_distance(player, enemy) < 2:
                if (get_pos(player)[0] == 0) or (get_pos(player)[0] == 15):
                    return JUMP_FORWARD
                else:
                    return BACK
        
        # Combat Super Armor
        if ((last_emove != None) and (last_emove[0] == "super_armor")):
            return BACK

        # Try close attack combo
        if (get_distance(player, enemy) <= 1):
            if ((get_past_move(player, 1) != None) and (get_past_move(player, 2) != None)):
                past_move1 = get_past_move(player, 1)[0]
                past_move2 = get_past_move(player, 2)[0]
                if (past_move1 == "recover" and (not secondary_on_cooldown(player))):
                    return SECONDARY
                if (past_move1 == past_move2 == "light"):
                    return HEAVY
            return LIGHT
        
        # Check enemy stun status
        if ((get_stun_duration(enemy) == True) and (get_recovery(enemy) == True)):
            return FORWARD

        # Try primary or secondary attack
        if (distance < 6) and (not primary_on_cooldown(player)):
            return PRIMARY
        elif (distance < 5) and (not secondary_on_cooldown(player)):
            return SECONDARY

        # Coward strat
        if (get_hp(player) > get_hp(enemy)):
            return BACK
        else:
            return FORWARD