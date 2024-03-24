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
        distX = get_pos(player)[0] - get_pos(enemy)[0];
        hp = get_hp(player)
        pos = get_pos(player)
        primaryOnCooldown = primary_on_cooldown(player)
        secondaryOnCooldown = secondary_on_cooldown(player)
        enemySecondary = get_secondary_skill(enemy)
        enemy_hp = get_hp(enemy)
        heavyReady = not heavy_on_cooldown(player)
        yDistance = get_pos(player)[1] - get_pos(enemy)[1];
        
        backAgainstWall = get_pos(player)[0] in {0,1,15,14}
        
        close_range = abs(distX) <= 1 and yDistance == 0
        
        is_blockable = {
            "dash_attack": False,
            "uppercut":True,
            "onepunch":False,
            "hadoken":True,
            "boomerang":True,
            "grenade":False,
            "beartrap":False,
        }
        
        projectile_skills = {"hadoken","grenade","beartrap"}
        
        blockTillPrimaryReady = False;
        
        print(f"Player HP : {hp}; Enemy HP: {enemy_hp}")
        
        def dodgeOrBlockProjs():
            enemyProjPos = ""            
        
            if not enemy_projectiles:
                return False
            else:
                enemyProjType = get_projectile_type(enemy_projectiles[0])
                enemyProjPos = get_proj_pos(enemy_projectiles[0])
                if is_blockable[enemySecondary]:
                    if  abs(enemyProjPos[0] - get_pos(player)[0]) < 1:
                        return BLOCK
                    else:
                        return False
                else:
                    match(enemyProjType):
                        case "grenade":
                            if abs(enemyProjPos[0] - get_pos(player)[0]) <= 1:
                                    if abs(distX) == 1:
                                        return LIGHT
                                    elif abs(distX) == 3 and not backAgainstWall:
                                        return JUMP_BACKWARD
                                    else:
                                        return PRIMARY
                            else:
                                return False
                        case "beartrap":
                            if abs(enemyProjPos[0] - get_pos(player)[0]) == 1:
                                return JUMP_BACKWARD
                            else:
                                return False
                  
        
        def canFireProjectile():
            onCooldown = secondary_on_cooldown(player)
            if not onCooldown:
                match(get_secondary_skill(player)):
                    case "hadoken":
                        if 0 <= abs(distX) <= 7:
                            return True
                        else:
                            return False
                    case "grenade":
                        if 1 < abs(distX) <= 5:
                            return True
                        else:
                            return False
                    case "beartrap":
                        if  1 < abs(distX) <= 8:
                            return True
                        else:
                            return False
            else:
                return False
            
        def rushSyle():
            return FORWARD
    
        if dodgeOrBlockProjs() != False:
            return dodgeOrBlockProjs()
        #Close range attacks take priority
        if abs(distX) <= 5 and primary_on_cooldown(player) == False:
            return PRIMARY
        if close_range:
            if canFireProjectile():
                return SECONDARY
            if heavyReady:
                return HEAVY
            else:
                return LIGHT
        else:
            if canFireProjectile():
                return SECONDARY    
            return rushSyle()

        
            

                
    
