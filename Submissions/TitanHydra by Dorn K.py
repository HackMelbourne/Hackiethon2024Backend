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
SECONDARY_SKILL = SuperArmorSkill

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

SHIELDTIME = 41
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
        self.past_hp_enemy = 100
        self.past_hp_player = 100
        self.working_attack = []
        self.enemy_attack = []
        self.grenade_time = 0
        self.shield_time = SHIELDTIME
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        self.shield_time -= 1

        #print(self.stuck)
        distance = get_distance(player,enemy)
        if(self.get_attack_work(player, enemy)):
            self.working_attack.append(get_last_move(player))

        if(self.get_enemy_attack_work(player, enemy)):
            self.enemy_attack.append(get_last_move(enemy))
        if not primary_on_cooldown(player):
            return PRIMARY
        #if not primary_on_cooldown(player) and abs(distance) <= prim_range(player):
        #    if self.check_one_armor(enemy):
        #        if not (self.shield_time <= 20) and (abs(distance)//2) <= prim_range(player):
        ##            return PRIMARY
        #    else:
        #        return PRIMARY
        if not secondary_on_cooldown(player):
            self.shield_time = SHIELDTIME
            return SECONDARY
        try:
            if (self.working_attack[-2][0] == self.working_attack[-1][0]) and self.working_attack[-1][0] == "light" and not heavy_on_cooldown(player):
                return HEAVY
        except:
            if distance == 1:
                return LIGHT
        if enemy_projectiles:
            distance_proj = get_distance(player,enemy_projectiles[-1])
            return self.movement_proj(distance_proj,enemy_projectiles,distance)
        if distance == 1:
            return HEAVY
        return self.movement(player,enemy,distance)
    def check_one_armor(self,enemy):
        return get_primary_skill(enemy) == "onepunch"
    def one_punch(self, enemy,distance):
        if self.check_one_armor(enemy):
            if self.shield_time <= 20: 
                return self.escape(distance)
        return None
    def upper(self, enemy,distance):
        if self.check_one_armor(enemy):
            if self.shield_time <= 20:
                return self.movement_no_jump(distance)
        return None
    def movement_proj(self,distance_proj,enemy_projectiles,distance): 
        if distance_proj <= 1 and  distance > 0:
            return JUMP_FORWARD
        if distance_proj >= -1 and  distance > 0:
            return JUMP_FORWARD
    
        if distance_proj <= 1 and  distance < 0:
            return JUMP_BACKWARD
        if distance_proj >= -1 and distance < 0:
            return JUMP_BACKWARD
        
    def movement(self,player,enemy,distance):
        move = self.one_punch(enemy,distance)
        if move is not None:
            return move
        if 3 < distance:
            return JUMP_FORWARD
        if 3 >= distance:
            return FORWARD
        if -3 > distance:
            return JUMP_BACKWARD
        if -3 <= distance:
            return BACK
        
    def escape(self,distance):
        if  distance <= 3:
            return JUMP_BACKWARD
        if  distance >= -3:
            return JUMP_FORWARD
        if  distance <= 1:
            return JUMP_FORWARD
        if  distance >= -1:
            return JUMP_BACKWARD
    def get_attack_work(self, player, enemy):
        curr_hp = get_hp(enemy) 
        if curr_hp < self.past_hp_enemy:
            self.past_hp_enemy = curr_hp
            return True
        self.past_hp_enemy = curr_hp
        return False

    def get_enemy_attack_work(self, player, enemy):
      curr_hp = get_hp(player) 
      if curr_hp < self.past_hp_player:
          self.past_hp_player = curr_hp
          return True
      self.past_hp_player = curr_hp
      return False
