# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
# primary skill can be defensive or offensive
# secondary skills involve summoning a projectile

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

# currently unsure how to enforce this...
#TODO FOR USER: Set primary and secondary skill here
'''
# for actions that do not deal damage
defense_actions = {"block": block, "move": move, "teleport": teleport, 
                   "super_saiyan": super_saiyan, "meditate": meditate,
                   "skill_cancel":skill_cancel}

# for actions that deal damage
attack_actions = {"light": attack, "heavy":attack, "dash_attack": dash_atk,
                  "uppercut": uppercut, "onepunch": one_punch
                  }

# for projectile actions
projectile_actions = {"hadoken":hadoken, "lasso":lasso, "boomerang":boomerang,
                      "grenade":grenade, "beartrap":beartrap, "icewall":icewall}

'''
# skill swap order: non-dmg, dmg, proj
# tp, meditate, dash_attack, uppercut, onepunch, hadoken, lasso, boomerang, grenade, beartrap, icewall, super_saiyan
PRIMARY_SKILL = TeleportSkill
SECONDARY_SKILL = Meditate

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

class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.skillNum = 1
        # list of next skills to switch to
        self.nextskills = ((DashAttackSkill, UppercutSkill), (OnePunchSkill, Hadoken), (Lasso, Boomerang), (Grenade, BearTrap), (IceWall, SuperSaiyanSkill))
        self.next_skills_iter = iter(self.nextskills)
        self.noswaps = False
        self.othertest = (JUMP, JUMP_BACKWARD, JUMP_FORWARD, BLOCK, LIGHT, HEAVY)
        self.newiter = iter(self.othertest)
    def request_swap(self):
        try:
            return ("swap", *next(self.next_skills_iter))
        except StopIteration:
            self.noswaps = True
            return NOMOVE
    
    def init_player_skills(self):
        return self.primary, self.secondary
    
    #MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):

        # uncomment below for scripted moves
        #return scripted_moves()    
        # uncomment below for calculated moves
        #return full_assault(player, enemy)
        #return eric_func(player, enemy)
        #return leo_func(player, enemy)
        #return spam_second()
        #return winning_strategy(player, enemy)
        # check that no toher projectile on screen at the moment
        return NOMOVE
        if get_stun_duration(player) or get_recovery(player):
            #cant do anth, early return
            return NOMOVE
        can_cast_p = can_cast_s = True
        if player_projectiles:
            if player._primarySkill._skillType in projectile_actions:
                can_cast_p = False
            if player._secondarySkill._skillType in projectile_actions:
                can_cast_s = False
        if not self.noswaps:  
            if self.skillNum == 1 and can_cast_p:
                self.skillNum = 2
                return (player._primarySkill._skillType, )
            elif self.skillNum == 2 and can_cast_s:
                self.skillNum = 3
                return (player._secondarySkill._skillType, )
            else:
                if not can_cast_s and not can_cast_p:
                    # both skills were projectiles, just gotta wait
                    return NOMOVE
                self.skillNum = 1
                return self.request_swap()
        else:
            # do the other stuff
            if not player._midair:
                try:
                    return next(self.newiter)
                except StopIteration:
                    return NOMOVE
            else:
                return NOMOVE
        
        # return eric_func2()
        