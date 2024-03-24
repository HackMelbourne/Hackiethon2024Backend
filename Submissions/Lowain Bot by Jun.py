# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = Meditate
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
# Zoning Bot
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
        self.hazard_pos = None
        self.defensive_mode = False
        self.offensive_mode = False

        self.opponent_cornered = False
        self.opponent_jumps_corners = False
        self.combo_counter = False
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        position = get_pos(player)
        enemy_pos = get_pos(enemy)
        enemy_side = get_pos(player)[0] < enemy_pos[0]
        # True = Player on left side, False = Player on right side

        distance_to_projectile = 100
        if(enemy_projectiles):
            distance_to_projectile = abs(get_pos(player)[0] - get_proj_pos(enemy_projectiles[0])[0])
            print(distance_to_projectile)

        # If heal skill is not on cooldown and hp < 80 then heal
        # If far distance throw fireball (3+)
        # If close range block then heavy punch then move back (1)
        # If backed into a corner jump forward
        # If mid range back away (2)
        # Enemy skill counters: 
        """
        Dash: If dash is not on cooldown and we are within dash range, jump backwards (Done)
        Grenade: If grenade is thrown, mark current position and move away from it
        Bear Trap: Avoid bear trap position 
        Super Armor: Run and avoid until duration is over (Done)
        One Punch: never get in range? (never will get into range)
        Projectile/Healing (How to beat our same strategy?) Rushdown into corner, hit while jumping out (DOESNT WORK, OFFENSE SUCKS IN THIS GAME)
        """

        # Enemy dash skill counter
        if (get_primary_skill(enemy) == "dash_attack"):
            if (not primary_on_cooldown(enemy)):
                if (distance <= 5):
                    return BLOCK
        #Countering super armor and super saiyan
        if (get_secondary_skill(enemy) == "super_armor" or get_secondary_skill(enemy) == "super_saiyan"):
            if (get_secondary_cooldown(enemy) > 20):
                self.defensive_mode = True
            else:
                self.defensive_mode = False

        # If they use the same strategy as we do, rushdown into corner, either light combo them in the corner or catch them as they land if they jump overhead.
        if (get_primary_skill(enemy) == "meditate" and (get_secondary_skill(enemy) == "hadoken" or get_secondary_skill(enemy) == "beartrap")):
            if (get_hp(player) >= 60): 
                self.offensive_mode = True
            else:
                self.offensive_mode = False

        if (not self.offensive_mode):
        # If stuck in corner jump out
            if (distance <= 2 and (position[0] == 0 or position[0] == 15)):
                return JUMP_FORWARD
            elif (distance >= 3):
                if (get_primary_cooldown(player) <= 1 and get_hp(player) <= 90):
                    return PRIMARY
                return SECONDARY
            elif (distance == 2):
                # If enemy is chasing, throw a heavy attack to stun them then move away
                if (not self.defensive_mode):
                    if (get_past_move(enemy, 1) and get_past_move(enemy, 2)):
                        if (get_past_move(enemy, 1)[0] == 'move' and get_past_move(enemy, 2)[0] == 'move' and distance == 2):
                            return HEAVY
                    if (get_last_move(player)[0] == 'heavy' and not secondary_on_cooldown(player)):
                        return SECONDARY
                return BACK
            
            # If in short range, block (for lights) then retreat
            elif (distance == 1):
                if (get_last_move(player)[0] != 'block'):
                    return BLOCK
                else:
                    return BACK

        else:
            if (self.opponent_cornered == True and get_last_move(enemy) == ('move', (1,1))):
                self.opponent_jumps_corners = True
                
            if (distance > 2):
                if (get_primary_cooldown(player) <= 1 and get_hp(player) <= 90):
                    return PRIMARY
                if (distance_to_projectile <= 2):
                    return BLOCK
                else:
                    return FORWARD
            if (distance == 2):
                # If enemy is in corner
                if (enemy_pos[0] == 0 or enemy_pos[0] == 15):
                    self.opponent_cornered = True
                else:
                    self.opponent_cornered = False
                return SECONDARY
            else:
                return FORWARD