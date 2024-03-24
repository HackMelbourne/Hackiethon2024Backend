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
SECONDARY_SKILL = SuperSaiyanSkill

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
        #parrying 
        player_x, player_y = get_pos(player)
        enemy_x, enemy_y = get_pos(enemy)
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        print(get_past_move(player, 1), get_past_move(enemy, 1), distance)
        print(get_hp(player), get_hp(enemy), "hp")
        print(player_x, enemy_x, "pos")
        print(secondary_on_cooldown(player))
        print(get_secondary_skill(enemy))
        if (player._curr_buff_duration > 0):
            #bumrush

            if get_stun_duration(enemy) > 0:
                print("parried")

                if player_y == enemy_y and abs(player_x - enemy_x) < 2:
                    if get_past_move(player, 1) == ('light', 'activate'):
                        if get_past_move(player, 2) == ('light', 'activate'):
                            return HEAVY
                        else:
                            return LIGHT
                    else:
                        return LIGHT
                return FORWARD
            
            if enemy_projectiles:
                if not primary_on_cooldown(player):
                    return PRIMARY
                if get_proj_pos(enemy_projectiles[0])[0] - 1 <= get_pos(player)[0] <= \
                    get_proj_pos(enemy_projectiles[0])[0] + 1:
                    return JUMP_FORWARD
            if not primary_on_cooldown(player):
                return PRIMARY
            if get_stun_duration(player):
                print("i'm stunned", get_stun_duration(player))
            if distance >= 2:
                print("movingforward")
                return FORWARD
            
            #following up the parry
            
            if get_last_move(player) == ('block', 'activate'):
                if enemy_x == 0 or enemy_x == 15:
                    if get_past_move(player, 1) == ('light', 'activate'):
                        if get_past_move(player, 2) == ('light', 'activate'):
                            return HEAVY
                        else:
                            return LIGHT
                    else:
                        return LIGHT
                return HEAVY
            # try for parry
            if distance < 2:
                return BLOCK
            
            
        else:
            if get_last_move(enemy) == (get_secondary_skill(enemy), 'activate'):
                return PRIMARY
            if distance <= 3 and not secondary_on_cooldown(player):
                return SECONDARY
            if player_x == 0 or player_x == 15:
                if enemy_projectiles:
                    if get_proj_pos(enemy_projectiles[0])[0] - 1 <= get_pos(player)[0] <= \
                        get_proj_pos(enemy_projectiles[0])[0] + 1:
                        return JUMP
                if get_stun_duration(enemy) > 0:
                    if player_y == enemy_y and abs(player_x - enemy_x) < 2:
                        if get_past_move(player, 1) == ('light', 'activate'):
                            if get_past_move(player, 2) == ('light', 'activate'):
                                return HEAVY
                            else:
                                return LIGHT
                        else:
                            return LIGHT
                    return FORWARD
                if distance < 2:
                    return BLOCK 

            if distance < 5:
                    return BACK
            if enemy_projectiles:
                if get_proj_pos(enemy_projectiles[0])[0] - 1 <= get_pos(player)[0] <= \
                    get_proj_pos(enemy_projectiles[0])[0] + 1:
                    return JUMP
            if distance > 5:
                return FORWARD
            
        #check if we can bum rush       
        if not primary_on_cooldown(player):
            #check that they used skill and rush through
            if get_last_move(enemy) == (get_secondary_skill(enemy), 'activate'):
                return PRIMARY
            else:
                # space them
                if distance < 5:
                    return BACK
                if enemy_projectiles:
                    if get_proj_pos(enemy_projectiles[0])[0] - 1 <= get_pos(player)[0] <= \
                        get_proj_pos(enemy_projectiles[0])[0] + 1:
                        return JUMP
                if distance > 5:
                    return FORWARD