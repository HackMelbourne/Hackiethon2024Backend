from test import validMove, correctPos
from math import ceil

def move(player, enemy, action):
    moveAction = player._move.activateSkill(action[1])[1]
    if validMove(moveAction, player, enemy) and not player._midair:
        # has vertical logic
        if moveAction[1]:
            player._midair = True
            if moveAction[0]:
                # this is diagonal jump
                player._velocity += player._direction * moveAction[0] * player._speed
                player._jumpHeight = 1 * player._speed
        else:
            # no vertical logic, simple horizontal movement
            player._blocking = False
            player._block.regenShield() 
            player._moves.append(action)
            player._xCoord += player._direction * moveAction[0] * player._speed
            
        player._moves.append(action)    

def block(player, target, action):
    player._moves.append(action)
    player._blocking = True

#returns the action if not on cooldown or mid-startup.
# if on cd, return current cd, or -1 if mid startup
def fetchAttack(player, attackType):
    if attackType == "light":
        return player._lightAtk.activateSkill()
    elif attackType == "heavy":
        return player._heavyAtk.activateSkill()
    return None

# Helper function for all attack types and attack skills    
def attackHit(player, target, damage, atk_range, vertical, blockable, knockback, stun):
    # checks if target is within the horizontal and vertical attack range
    player_x, player_y = player.get_pos()
    target_x, target_y = target.get_pos()
    if (abs(player_x-target_x) <= atk_range and 
        player_y + vertical >= target_y):
        # can be changed later : no knockback if block or stunned
        if target._blocking or target._stun:
            knockback = 0
        # if target is blocking
        if(target._blocking and blockable):
            #parry if block is frame perfect: the target blocks as attack comes out
            if target._moves[-1] == "block" and target._moves[-2] != "block":
                player._stun = 2
            elif target._blocking:
                #target is stunned if their shield breaks from damage taken
                target._stun += target._block.shieldDmg(damage)
            return 0, 0
        else:
            damage = damage - target._defense
            if damage < 0:
                damage = 0
            target._hp -= damage
            target._velocity -= knockback
            return knockback * player._direction, stun
    return 0, 0

# Light and heavy attacks
def attack(player,target, action):
    attack = fetchAttack(player, action[0])
    if attack:
        if not (isinstance(attack, int)):
            player._blocking = False
            player._block.regenShield() 
            # gets only the attack info, doesn't include "light"/"heavy"
            attack = attack[1:]
            player._moves.append(action)
        
            # performs the actual attack using fetched attack info
            return attackHit(player, target, *attack)
        else:
            # mid startup
            doStartup(player, action)
            print("startup")
    player._moves.append(("NoMove", None))
    return 0, 0

# helper function for all skills
# return cooldown/startup if on cooldown/startup
# else return skill type and related attributes
def fetchSkill(player, skillClass):
    returnVal = -2
    # if using a skill correctly, reset the startup of every other action 
    if player._primarySkill.skillType == skillClass:
        player._secondarySkill.resetStartup()
        player._heavyAtk.resetStartup()
        player._lightAtk.resetStartup()
        player._block.resetStartup()
        player._move.resetStartup()
        returnVal = player._primarySkill.activateSkill()
    elif player._secondarySkill.skillType == skillClass:
        player._primarySkill.resetStartup()
        player._heavyAtk.resetStartup()
        player._lightAtk.resetStartup()
        player._block.resetStartup()
        player._move.resetStartup()
        returnVal = player._secondarySkill.activateSkill()
        
    if returnVal == -2:
        print("Player does not have this skill")
    return returnVal
    
    
def changeSpeed(player, speed):
    # if speed == 0, reset startups back to default
    player._primarySkill.reduceMaxStartup(speed)
    player._secondarySkill.reduceMaxStartup(speed)
    player._lightAtk.reduceMaxStartup(speed)
    player._heavyAtk.reduceMaxStartup(speed)
    player._block.reduceMaxStartup(speed)
    player._move.reduceMaxStartup(speed)
    player._speed = ceil(player._speed * speed)
    # when resetting back to normal speed, set player speed to 1 and use 
    # resetMaxStartup method

def changeDamage(player, buffValue):
    if player._primarySkill.skillType in (attack_actions | projectile_actions):
        player._primarySkill.damageBuff(buffValue)
    if player._secondarySkill.skillType in (attack_actions | projectile_actions):
        player._secondarySkill.damageBuff(buffValue)
    
    player._lightAtk.damageBuff(buffValue)
    player._heavyAtk.damageBuff(buffValue)
    player._atkbuff += buffValue

# dashes towards target, deals damage along the way
def dash_atk(player, target, action):
    knockback = stun = 0
    skillInfo = fetchSkill(player, "dash_attack")
    # if skill on cooldown or in startup
    if isinstance(skillInfo, int):
        player._moves.append(("NoMove", None))
        return 0, 0
    
    # so now, skillInfo = damage, 
    skillInfo = skillInfo[1:]
    player._moves.append(action)

    knockback, stun = attackHit(player, target, *skillInfo)
    player._xCoord += player._direction * skillInfo[1]
    correctPos(player)
    return knockback, stun

def uppercut(player, target, action):
    # attack hit copied from dash_attack
    knockback = stun = 0
    skillInfo = fetchSkill(player, "uppercut")
    # if skill on cooldown or in startup
    if isinstance(skillInfo, int):
        if (skillInfo == -1):
            # is currently doing startup ticks
            player._moves.append(action[0], "startup")
        else:
            player._moves.append(("NoMove", None))
        return 0, 0
    
    # so now, skillInfo = damage, 
    skillInfo = skillInfo[1:]
    player._moves.append(action)

    knockback, stun = attackHit(player, target, *skillInfo)
    correctPos(player)
    return knockback, stun

# teleport skill, use ("teleport", 1) to teleport towards target, -1 to teleport away
def teleport(player, target, action):
    skillInfo = fetchSkill(player, "teleport")
    if isinstance(skillInfo, int):
        if (skillInfo == -1):
            # is currently doing startup ticks
            player._moves.append(action[0], "startup")
        else:
            player._moves.append(("NoMove", None))
        return 0, 0

    distance = skillInfo[1]
    player._moves.append(action)

    player._xCoord += distance * action[1] * player._direction
    correctPos(player)
    return None

# buffs damage and speed for player
def super_saiyan(player, target, action):
    skillInfo = fetchSkill(player, "super_saiyan")
    if isinstance(skillInfo, int):
        if (skillInfo == -1):
            # is currently doing startup ticks
            player._moves.append(action[0], "startup")
        else:
            player._moves.append(("NoMove", None))
        return 0, 0
    
    speedBuff = skillInfo[1][0]
    atkBuff = skillInfo[1][1]
    duration = skillInfo[1][2]
    player._moves.append(action)
    changeSpeed(player, speedBuff)
    changeDamage(player, atkBuff)
    player._currentBuffDuration = duration
    return None
    
# heals player for given amount of hp
def meditate(player, target, action):
        skillInfo = fetchSkill(player, "meditate")
        if isinstance(skillInfo, int):
            if (skillInfo == -1):
                # is currently doing startup ticks
                player._moves.append(action[0], "startup")
            else:
                player._moves.append(("NoMove", None))
            return 0, 0
        
        healVal = skillInfo[1]
        player._moves.append(action)
        player._hp += healVal

    return None    
    
def skill_cancel(player, target, action):
    player._skill_state = False
    player._moves.append(action)
    return None

# similar layout to dash_atk
# TODO : has startup, add function to manage startups
# powerful punch that takes time to charge up
def one_punch(player, target, action):
    knockback = stun = 0
    skillInfo = fetchSkill(player, "onepunch")
    if isinstance(skillInfo, int):
        if (skillInfo == -1):
            # is currently doing startup ticks
            player._moves.append(action[0], "startup")
        else:
            player._moves.append(("NoMove", None))
        return 0, 0
    
    skillInfo = skillInfo[1:]
    player._moves.append(action)

    knockback, stun = attackHit(player, target, *skillInfo)
    return knockback, stun
        
def hadoken(player, target, action):
    return fetchProjectileSkill(player, "hadoken", action)
        
def lasso(player, target, action):
    player._skill_state = True
    return fetchProjectileSkill(player, "lasso", action)

def boomerang(player, target, action):
    return fetchProjectileSkill(player, "boomerang", action)

def grenade(player, target, action):
    return fetchProjectileSkill(player, "grenade", action)

def beartrap(player, target, action):
    return fetchProjectileSkill(player, "beartrap", action)

def icewall(player, target, action):
    return fetchProjectileSkill(player, "icewall", action)

def fetchProjectileSkill(player, projectileName, action):
    if (action[0] == projectileName):
        skillInfo = fetchSkill(player, projectileName)
        if not isinstance(skillInfo, int):
            # returns dictionary containing projectile info
            skillInfo = skillInfo[-1]
            player._moves.append(action)
            return skillInfo
        else:
            if (skillInfo == -1):
                # is currently doing startup ticks
                player._moves.append(action[0], "startup")
            else:
                player._moves.append(("NoMove", None))
    return None

def encumber(player):
    # special state for player after super saiyan duration finishes
    print("START ENCUMBER")
    player._encumberedDuration = 5
    player._encumbered = True
    changeSpeed(player, 1/2)
    
def doStartup(player, action):
    player._moves.append(action)
    if player._moveNum == len(player._inputs) - 1:
        print("last move")
        player._inputs.append(action)
    elif player._inputs[player._moveNum + 1][0] == "skill_cancel":
        player._primarySkill.resetStartup()
        player._secondarySkill.resetStartup()
        player._heavyAtk.resetStartup()
        player._lightAtk.resetStartup()
        player._block.resetStartup()
        player._move.resetStartup()
    elif player._inputs[player._moveNum + 1] in (action, None):
        player._inputs[player._moveNum + 1] = action
        
     
# null function
def nullFunc(player, target, action):
    return 0,0

def nullProj(player, target, action):
    return None

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
How to add a new skill
- Add the skill class to skills.py
Then use
def skill(player, target, action):
    -- this checks if the skill is on cooldown or startup, use it if not --
    if (action[0] == "skill"):
        skillInfo = fetchSkill(player, "skill")
        if isinstance(skillInfo, int):
            return 0, 0
        
        -- add skill logic here --
    return None
'''