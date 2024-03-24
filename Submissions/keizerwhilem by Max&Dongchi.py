# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN
import random

PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = Grenade
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)
PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)
NOMOVE = "NoMove"


player_hp = []
enemy_hp = []
tic = -1


#begging sets
imobileBegginingMoveSet = [SECONDARY,PRIMARY,NOMOVE,FORWARD,FORWARD,LIGHT,LIGHT,HEAVY]
imobileBegginingMoveConditions = [666,666,666,666,666,0,0,0]
uppercut_grenade = [SECONDARY, PRIMARY, NOMOVE, HEAVY, LIGHT, LIGHT, HEAVY]
uppercut_grenadeConditions = [666,666,666,0,0,0,0,0]

dashAndBombMoveSet = [PRIMARY,NOMOVE,BACK,SECONDARY]
dashAndBombMoveConditions = [666,666,666,3]

meditate_hadoken = [SECONDARY, PRIMARY, NOMOVE]
meditate_hadokenConditions = [666,666,666]
meditate_grenade = [SECONDARY, PRIMARY, NOMOVE, HEAVY, LIGHT, LIGHT, HEAVY]
meditate_grenadeConditions = [666,666,666,0,0,0,0]

dashEscapeMoveSet = [PRIMARY,NOMOVE,FORWARD,FORWARD,SECONDARY]
dashEscapeMoveConditions = [666,666,666,666,3]

fleeBackwardsMoveSet = [BLOCK,BLOCK,BLOCK,BACK,BACK,BACK]
fleeBackwardsMoveConditions = [666,666,666,666,666,666]

fleeForwardsMoveSet = [PRIMARY,NOMOVE,FORWARD,FORWARD,FORWARD]
fleeForwardsMoveConditions = [666,666,666,666,666,666]

fullDashMoveSet = [PRIMARY,NOMOVE,FORWARD]
fullDashMoveConditions = [666,666,666]

forwardAndBombMoveSet = [FORWARD,FORWARD,SECONDARY]
forwardAndBombMoveConditions =  [666,666,3]

meleComboMoveSet =[HEAVY,LIGHT,LIGHT,HEAVY]
meleComboMoveConditions = [0,0,0,0]



distance = 0

counterMoveSet = [BLOCK, LIGHT, LIGHT, HEAVY, BACK]
counterMoveConditions = [1, 1, 1, 1, 666]
def ATTACK():
    if heavy_on_cooldown == False:
        return HEAVY
    else:
        return LIGHT
dashAndAttackSet = [PRIMARY, NOMOVE, ATTACK()]
dashAndAttackConditions = [666, 666, 666]

QuickV1Set = [FORWARD, BLOCK, ATTACK(), BACK,BACK]
QuickV1Conditions = [666, 1, 1, 666,666]

QuickV2Set = [BACK, SECONDARY, BACK,BACK]
QuickV2Conditions = [666, 3, 666, 666]

attackTeleporterDashSet = [PRIMARY,NOMOVE,LIGHT]
attackTeleporterDashConditions = [666,666,666]


currentMoveSet = [NOMOVE,NOMOVE]
currentMoveCondtions = [666,666]

openingMove = False
moveSetIndex = -1
ExecuteSet = [BACK, SECONDARY]
ExecuteConditions = [666, 3]
enemyPrimary = ""
enemySecondary = ""

enemyProjectilePositions = {"projectileTemplate": [0]*130}  #keeps track of the positions of enemy projectiles



def right(player,enemy):      #Returns true if the player is facing left, false if facing right. 
    if (get_pos(enemy)[0] - get_pos(player)[0]) >=0:
        return True
    return False

def dodge_or_block(player,enemy):       #A very basic function (to be expanded) that decides wether to dodge or block when being projectile attcaked
    return JUMP

class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        self.enemy_hp = []
        self.tick_count = 0
    
    def init_player_skills(self):
        return self.primary, self.secondary
    
    
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        global tic, moveSetIndex,enemyPrimary,enemySecondary, imobileBegginingMoveSet
        global currentMoveSet, currentMoveCondtions
        global dashAndBombMoveSet, dashAndBombMoveConditions,dashEscapeMoveSet,dashEscapeMoveConditions,fleeBackwardsMoveSet,fleeBackwardsMoveConditions,fullDashMoveSet,fullDashMoveConditions
        global enemyProjectilePositions
        global openingMove
        global enemy_hp, distance
        tic = tic +1
        player_hp.append(get_hp(player))
        enemy_hp.append(get_hp(enemy))
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        #system to track projectile positions
        if tic <120:
            for proj in enemy_projectiles:
                if enemySecondary == "beartrap":
                    if str(proj)[-12:-1] not in list(enemyProjectilePositions.keys()):
                        enemyProjectilePositions[str(proj)[-12:-1]] = [0]*130
                        lst = enemyProjectilePositions[str(proj)[-12:-1]]
                        lst[tic] = get_proj_pos(proj)
                        lst[tic+1] = get_proj_pos(proj)
                        lst[tic+2] = get_proj_pos(proj)
                        lst[tic+3] = get_proj_pos(proj)
                        lst[tic+4] = get_proj_pos(proj)
                        lst[tic+5] = get_proj_pos(proj)
                        lst[tic+6] = get_proj_pos(proj)
                        lst[tic+7] = get_proj_pos(proj)             #append the position of the bear trap for the next 10 tics
                        lst[tic+8] = get_proj_pos(proj)
                        lst[tic+9] = get_proj_pos(proj)
                        enemyProjectilePositions[str(proj)[-12:-1]] = lst
                else:
                    if str(proj)[-12:-1] not in list(enemyProjectilePositions.keys()):
                        enemyProjectilePositions[str(proj)[-12:-1]] = [0]*130
                    else:
                        lst = enemyProjectilePositions[str(proj)[-12:-1]]
                        lst[tic] = get_proj_pos(proj)
                        enemyProjectilePositions[str(proj)[-12:-1]] = lst
        imobileBegginingMoveSet = [SECONDARY,PRIMARY,NOMOVE,FORWARD,FORWARD,LIGHT,LIGHT,HEAVY]
        print(currentMoveSet)
        #system to assign our attack for the first tick based on the type of enemy
        if(tic == 0):
            enemyPrimary = get_primary_skill(enemy)
            enemySecondary = get_secondary_skill(enemy)
            currentMoveSet = imobileBegginingMoveSet
            currentMoveCondtions = imobileBegginingMoveConditions
            if(enemyPrimary == "uppercut" and enemySecondary == "grenade"):
                currentMoveSet = uppercut_grenade
                currentMoveCondtions = uppercut_grenadeConditions
            if(enemyPrimary == "meditate" and enemySecondary == "hadoken"):
                currentMoveSet = meditate_hadoken
                currentMoveCondtions = meditate_hadokenConditions
            if(enemyPrimary == "meditate" and enemySecondary == "grenade"):
                currentMoveSet = meditate_grenade
                currentMoveCondtions = meditate_grenadeConditions
            if (enemyPrimary not in {"dash_attack","teleport"}):   #the opponent is not a 'mobile' character.
                currentMoveSet = imobileBegginingMoveSet
                currentMoveCondtions = imobileBegginingMoveConditions
            else:                                           #the opponent is a 'mobile' character. 
                if (enemyPrimary  == "dash_attack"):                   #if the opponent can dash we have a nunber of options.
                    currentMoveSet = imobileBegginingMoveSet
                    currentMoveCondtions = imobileBegginingMoveConditions
                else:
                    print("boob")

        #print(f"tick:{tic-1}  movement:{get_last_move(player)}   enemy hp:{get_hp(enemy)}   enemy stun:{get_stun_duration(enemy)}") #print current stas

        # System to attack
                    
        ###OVERIDE FUNCTION FOR IF NO PROGRESS IS BEING MADE



        if not currentMoveSet:
            currentMoveSet = dashAndBombMoveSet
            currentMoveCondtions = dashAndBombMoveConditions


        if abs(get_pos(player)[0] - get_pos(enemy)[0]) == 1:
            currentMoveSet = meleComboMoveSet
            currentMoveCondtions = meleComboMoveConditions







        #system to dodge projectiles
        if openingMove:
            if enemySecondary == "hadoken":
                for key in enemyProjectilePositions:
                    positionValues = enemyProjectilePositions[key]
                    if len(positionValues) <= tic:
                        if positionValues[tic-1]:   #if the thing has actualy got a position value (it is travelling)
                            if positionValues[tic-1][1] == get_pos(player)[1] or positionValues[tic-1][1] == get_pos(player)[1] +1 :#if its in the players vertical range
                                if right(player,enemy):                   #if we facing the front (left)
                                    if positionValues[tic-1][0] <= get_pos(player)[0] + 2:
                                        del enemyProjectilePositions[key]
                                        return JUMP
                                else:                           #if we facing the back (right)
                                    if positionValues[tic-1][0] >= get_pos(player)[0] - 2 and positionValues[tic-1][0] != 0:
                                        del enemyProjectilePositions[key]
                                        return JUMP    
                                
            elif enemySecondary == "beartrap":
                for key in enemyProjectilePositions:
                    positionValues = enemyProjectilePositions[key]
                    if len(positionValues) <= tic:
                        if positionValues[tic]:     #if the beartrap is alive currently
                            if get_pos(player)[0] == positionValues[tic][0]:
                                currentMoveSet = fleeBackwardsMoveSet
                                currentMoveCondtions =fleeBackwardsMoveConditions
                                print("fleeing")

            elif enemySecondary == "boomerang":
                for key in enemyProjectilePositions:
                    positionValues = enemyProjectilePositions[key]
                    if len(positionValues) <= tic:
                        if positionValues[tic-1]:   #if the thing has actualy got a position value (it is travelling)
                            if positionValues[tic-1][1] == get_pos(player)[1] or positionValues[tic-1][1] == get_pos(player)[1] + 1 :#if its in the players vertical range
                                if positionValues[tic-1][0] == get_pos(player)[0] + 2 or positionValues[tic-1][0] == get_pos(player)[0] - 2:
                                    del enemyProjectilePositions[key]
                                    return dodge_or_block(player,enemy)
                        

            elif get_last_move(enemy) == ("grenade","activate"):       #if a grenade is thrown we literally just run away. 
                if(right(player,enemy)):
                    if get_pos(player)[0] >4 :
                        currentMoveSet = fleeBackwardsMoveSet
                        currentMoveCondtions =fleeBackwardsMoveConditions
                        print("fleeing backwards")
                    else:
                        if enemy_projectiles:
                            if get_proj_pos(enemy_projectiles[-1])[0] >= get_pos(player)[0] +4:
                                print("safe")
                        else:
                            currentMoveSet = fleeForwardsMoveSet
                            currentMoveCondtions =fleeForwardsMoveConditions
                            print("fleeing forwards")
                else:
                    if get_pos(player)[0] < 11 :
                        currentMoveSet = fleeBackwardsMoveSet
                        currentMoveCondtions =fleeBackwardsMoveConditions
                        print("fleeing backwards")
                    else:
                        if(enemy_projectiles):
                            if get_proj_pos(enemy_projectiles[-1])[0] <= get_pos(player)[0] -4:
                                print("safe")
                        else:
                            currentMoveSet = fullDashMoveSet
                            currentMoveCondtions =fullDashMoveConditions
                            print("fleeing forwards")
            
            if get_last_move(enemy) == ("dash_attack","activate"): 
                    currentMoveSet = fleeBackwardsMoveSet
                    currentMoveCondtions =fleeBackwardsMoveConditions
                    
            if get_last_move(enemy) == ("teleport","activate"): 
                    if not primary_on_cooldown:
                        currentMoveSet = attackTeleporterDashSet
                        currentMoveCondtions =attackTeleporterDashConditions
                    else:
                        currentMoveSet = fleeBackwardsMoveSet
                        currentMoveCondtions =fleeForwardsMoveConditions
            if skill_cancellable(enemy) and enemyPrimary == "onepunch":
                if get_pos(player)[0] >= 3 and get_pos(player)[0] <= 12:
                    return JUMP_BACKWARD
                else:
                    if primary_on_cooldown(player):
                        return JUMP_FORWARD
                    else:
                        return PRIMARY
            

        if enemyPrimary == "uppercut" and distance < 2:
            if get_pos(player)[0] > 2 and  get_pos(player)[0] < 13:
                if random.randint(1, 10) > 2:
                    return BLOCK
                return BACK
            else:
                if not primary_on_cooldown(player):
                    return PRIMARY
            
    
        if tic >20:
            if enemy_hp[tic] == enemy_hp[tic-10]:
                currentMoveSet =  dashAndBombMoveSet
                currentMoveCondtions = dashAndBombMoveConditions
                if not secondary_on_cooldown(player):
                    return SECONDARY
                elif not primary_on_cooldown(player):
                    return PRIMARY
                else:
                    return FORWARD

        if get_pos(player)[0] <= 2 or get_pos(player)[0] >= 13:
            if get_primary_cooldown(player) == 0:
                currentMoveSet = dashEscapeMoveSet
                currentMoveCondtions = dashEscapeMoveConditions
            else:
                if not currentMoveSet:
                        return JUMP_FORWARD




        if abs(get_pos(player)[0] - get_pos(enemy)[0]) >3 and abs(get_pos(player)[0] - get_pos(enemy)[0]) <7:
            if not get_primary_cooldown(player):
                currentMoveSet = dashEscapeMoveSet
                currentMoveCondtions = dashEscapeMoveConditions
            else:
                return FORWARD
        elif abs(get_pos(player)[0] - get_pos(enemy)[0]) >1 and abs(get_pos(player)[0] - get_pos(enemy)[0]) <3:
            if not get_primary_cooldown(player):
                currentMoveSet = QuickV1Set
                currentMoveCondtions = QuickV1Conditions
            else:
                currentMoveSet = dashAndAttackSet
                currentMoveCondtions = dashAndAttackConditions
        if enemy_hp[tic] <= 20:
            currentMoveSet = ExecuteSet
            counterMoveConditions = ExecuteConditions
        if abs(get_pos(player)[0] - get_pos(enemy)[0]) <= 1:
            currentMoveSet = QuickV1Set
            currentMoveCondtions = QuickV1Conditions
        if abs(get_pos(player)[0] == get_pos(enemy)[0]):
            if random.choice([True,False]):
                return BLOCK
            return LIGHT
        




        if not currentMoveSet:    
            """
            if enemyPrimary == "meditate" and enemySecondary == "hadoken":
                currentMoveSet = meditate_hadoken
                currentMoveCondtions = meditate_hadokenConditions
            if enemyPrimary == "meditate" and enemySecondary == "grenade":
                currentMoveSet = meditate_grenade
                currentMoveCondtions = meditate_grenadeConditions
            """
            if abs(get_pos(player)[0] - get_pos(enemy)[0]) < 6 and abs(get_pos(player)[0] - get_pos(enemy)[0]) > 4: 
                if not primary_on_cooldown(player):
                    currentMoveSet = dashAndBombMoveSet
                    currentMoveCondtions = dashAndBombMoveConditions
                else:
                    currentMoveSet = forwardAndBombMoveSet
                    currentMoveCondtions = forwardAndBombMoveConditions
            elif abs(get_pos(player)[0] - get_pos(enemy)[0]) <= 4 and abs(get_pos(player)[0] - get_pos(enemy)[0]) > 1 and not secondary_on_cooldown(player) and get_pos(player)[1] == 0: 
                return SECONDARY
            else:
                if primary_on_cooldown(player):
                    return BLOCK
                return PRIMARY
        
        """
        if tic > 1 and ((get_last_move(enemy)[0] == 'NoMove' and distance <= 1) or (get_last_move(enemy)[0] == 'light' and distance <= 1)):
            currentMoveSet = counterMoveSet
            currentMoveCondtions = counterMoveConditions
        elif distance >= 2 and distance <= 4:
            currentMoveSet = dashAndAttackSet
            currentMoveCondtions = dashAndAttackConditions

        if tic >= 11:
            recent_hp = player_hp[tic - 10: tic]
            if all(hp == player_hp[tic] for hp in recent_hp):
                currentMoveSet = dashAndAttackSet
                currentMoveCondtions = dashAndAttackConditions
        """





        #system to execute the current move set.
        if currentMoveSet:                        #if we have a current move set
            moveSetIndex = moveSetIndex + 1                 #increase the index value for the set (each frame)
            if(moveSetIndex >= len(currentMoveSet)):        #if we are going to finish the move set
                currentMoveSet = []                             #reset the moveset
                currentMoveCondtions = []
                moveSetIndex = -1                               #rest the moveset index
                openingMove = True
            else:
                if currentMoveCondtions:
                    if currentMoveCondtions[moveSetIndex] != 666:
                        if get_pos(player)[0] - (get_pos(enemy)[0] + 1) == currentMoveCondtions[moveSetIndex] or get_pos(player)[0] - (get_pos(enemy)[0] - 1) == currentMoveCondtions[moveSetIndex]: #if we meet the condition to continue
                            return currentMoveSet[moveSetIndex]         #execute the current move from the set
                        else:
                            if not openingMove:
                                currentMoveSet = fleeBackwardsMoveSet                           #exxit the moveset.
                                currentMoveCondtions = fleeBackwardsMoveConditions
                                return currentMoveSet[moveSetIndex]
                            else:
                                currentMoveSet = []                             #exxit the moveset.
                                currentMoveCondtions = []
                                moveSetIndex = -1 
                            openingMove = True
                    else:
                        return currentMoveSet[moveSetIndex]
                    

        if abs(get_pos(player)[0] - get_pos(enemy)[0]) <= 1:
            return ATTACK()
        else:
            if primary_on_cooldown(player):
                return BACK
            return PRIMARY

                    
