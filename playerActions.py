from test import validMove, correctPos
from math import ceil

def move(player, enemy, action):
    moveAction = player._move._activateSkill(action[1])[1]
    player._blocking = False
    player._block._regenShield()
    if validMove(moveAction, player, enemy) and not player._midair:
        # has vertical logic
        if moveAction[1]:
            player._midair = True
            if moveAction[0]:
                # this is diagonal jump
                player._velocity = player._direction * moveAction[0] * player._speed
                player._jumpHeight = 1 * player._speed
        else:
            # no vertical logic, simple horizontal movement 
            print(player._direction, moveAction)
            player._xCoord += player._direction * moveAction[0] * player._speed   
        player._moves.append(action)
    else:
        player._moves.append(("NoMove", None))
        
def reset_block(player):
    player._block._regenShield()
    player._blocking = False
    
def block(player, target, action):
    player._moves.append(action)
    player._blocking = True

#returns the action if not on cooldown or mid-startup.
# if on cd, return current cd, or -1 if mid startup
def fetchAttack(player, attackType):
    returnVal = None
    if attackType == "light":
        returnVal = player._lightAtk._activateSkill()
        if not isinstance(returnVal, int):
            # casted skill successfully, so put into recovery
            player._recovery += player._primarySkill._recovery
    elif attackType == "heavy":
        returnVal = player._heavyAtk._activateSkill()
        if not isinstance(returnVal, int):
            # casted skill successfully, so put into recovery
            player._recovery += player._primarySkill._recovery
    return returnVal

# todo fix this, based on relative moves, not absolute
def check_atk_combo(player, attack):
    if attack == "light":
        # go to previous move before heavy startup
        prev_move_pos = go_to_prev_atk(player, ("light", "startup"), -1)
        if player._moves[prev_move_pos][0] == "light":
            # go to previous move before light startup
            prev_move_pos -= 1
            prev_move_pos = go_to_prev_atk(player, ("light", "startup"), prev_move_pos)
            if player._moves[prev_move_pos][0] == "light":
                return True
    elif attack == "heavy":
        # go to previous move before heavy startup
        prev_move_pos = go_to_prev_atk(player, ("heavy", "startup"), -1)
        if player._moves[prev_move_pos][0] == "light":
            # go to previous move before light startup
            prev_move_pos -= 1
            prev_move_pos = go_to_prev_atk(player, ("light", "startup"), prev_move_pos)
            if player._moves[prev_move_pos][0] == "light":
                return True
    return False           
 
# goes to previous move that isnt startup       
def go_to_prev_atk(player, move, start):
    while player._moves[start] == move:
        start -= 1
    return start

# Helper function for all attack types and attack skills    
def attackHit(player, target, damage, atk_range, vertical, blockable, knockback, stun, surehit=False):
    # checks if target is within the horizontal and vertical attack range
    player_x, player_y = player.get_pos()
    target_x, target_y = target.get_pos()
    # surehit is for projectiles, bcs checking for collision alr done 
    if (surehit or (abs(player_x-target_x) <= atk_range) and 
        (abs(target_y - player_y) <= vertical) and (target_y >= player_y)):
        # if target is blocking
        if(target._blocking and blockable):
            #parry if block is frame perfect: the target blocks as attack comes out
            if target._moves[-1][0] == "block" and target._moves[-2][0] != "block":
                player._stun = 2
            elif target._blocking:
                #target is stunned if their shield breaks from damage taken
                target._stun += target._block._shieldDmg(damage)
            return 0, 0
        else:
            damage = damage - target._defense
            if damage < 0:
                damage = 0
            target._hp -= damage
            target._velocity = 0
            print(f"player {player._id} hit player {target._id}")
            return knockback * player._direction, stun
    return 0, 0

# Light and heavy attacks
def attack(player,target, action):
    player._blocking = False
    player._block._regenShield() 
    attack = fetchAttack(player, action[0])
    if attack:
        if not (isinstance(attack, int)):
            # gets only the attack info, doesn't include "light"/"heavy"
            attack = list(attack[1:])
            player._midStartup = False
        
            # performs the actual attack using fetched attack info
            if check_atk_combo(player, action[0]):
                # buffs damage and knockback for this hit
                # damage buff
                print("combo")
                attack[0] = int(attack[0] * 1.5 + 1)
                # knockback buff
                attack[4] += 2
                
            player._moves.append((action[0], ))
            return attackHit(player, target, *attack)
        elif attack == -1:
            player._midStartup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", None))
    else:
        player._moves.append(("NoMove", None))
    return 0, 0

# helper function for all skills
# return cooldown/startup if on cooldown/startup
# else return skill type and related attributes
def fetchSkill(player, skillClass):
    returnVal = -2
    # if using a skill correctly, reset the startup of every other action 
    if player._primarySkill._skillType == skillClass:
        player._secondarySkill._resetStartup()
        player._heavyAtk._resetStartup()
        player._lightAtk._resetStartup()
        player._block._resetStartup()
        player._move._resetStartup()
        returnVal = player._primarySkill._activateSkill()
        
        if not isinstance(returnVal, int):
            # casted skill successfully, so put into recovery
            player._recovery += player._primarySkill._recovery
            
    elif player._secondarySkill._skillType == skillClass:
        player._primarySkill._resetStartup()
        player._heavyAtk._resetStartup()
        player._lightAtk._resetStartup()
        player._block._resetStartup()
        player._move._resetStartup()
        returnVal = player._secondarySkill._activateSkill()
        
        if not isinstance(returnVal, int):
            # casted skill successfully, so put into recovery
            player._recovery += player._primarySkill._recovery
        
    if returnVal == -2:
        print("Player does not have this skill")
    return returnVal
    
    
def changeSpeed(player, speed):
    # if speed == 0, reset startups back to default
    player._primarySkill._reduceMaxStartup(speed)
    player._secondarySkill._reduceMaxStartup(speed)
    player._lightAtk._reduceMaxStartup(speed)
    player._heavyAtk._reduceMaxStartup(speed)
    player._block._reduceMaxStartup(speed)
    player._move._reduceMaxStartup(speed)
    player._speed = ceil(player._speed * speed)
    # when resetting back to normal speed, set player speed to 1 and use 
    # resetMaxStartup method

def changeDamage(player, buffValue):
    if player._primarySkill._skillType in (attack_actions | projectile_actions):
        player._primarySkill._damageBuff(buffValue)
    if player._secondarySkill._skillType in (attack_actions | projectile_actions):
        player._secondarySkill._damageBuff(buffValue)
    
    player._lightAtk._damageBuff(buffValue)
    player._heavyAtk._damageBuff(buffValue)
    player._atkbuff += buffValue

# dashes towards target, deals damage along the way
def dash_atk(player, target, action):
    knockback = stun = 0
    skillInfo = fetchSkill(player, "dash_attack")
    # if skill on cooldown or in startup
    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._midStartup = True
            player._moves.append(action)
        else:
            player._moves.append(("NoMove", None))
        return 0, 0
    
    player._midStartup = False
    
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
        if skillInfo == -1:
            player._midStartup = True
            player._moves.append(action)
        else:
            player._moves.append(("NoMove", None))
        return 0, 0
    
    player._midStartup = False
    # so now, skillInfo = damage, 
    skillInfo = skillInfo[1:]
    player._moves.append(action)
    print(f"My : {player.get_pos()} enemy: {target.get_pos()}")
    knockback, stun = attackHit(player, target, *skillInfo)
    correctPos(player)
    return knockback, stun

# teleport skill, use ("teleport", 1) to teleport towards target, -1 to teleport away
def teleport(player, target, action):
    skillInfo = fetchSkill(player, "teleport")
    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._midStartup = True
            player._moves.append(action)
        else:
            player._moves.append(("NoMove", None))
        return 0, 0
    
    player._midStartup = False

    distance = skillInfo[1]
    #tp_direction = action[1]  // can change later, this means input = "teleport", int
    tp_direction = -1
    player._moves.append(action)

    player._xCoord += distance * tp_direction * player._direction
    correctPos(player)
    return None

# buffs damage and speed for player
def super_saiyan(player, target, action):
    skillInfo = fetchSkill(player, "super_saiyan")

    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._midStartup = True
            player._moves.append(action)
        else:
            player._moves.append(("NoMove", None))
        return 0, 0
    
    player._midStartup = False
    
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
        if skillInfo == -1:
            player._midStartup = True
            player._moves.append(action)
        else:
            player._moves.append(("NoMove", None))
        return 0, 0
    
    player._midStartup = False
    
    healVal = skillInfo[1]
    player._moves.append(action)
    player._hp += healVal

    return None    
    
# similar layout to dash_atk
# TODO : has startup, add function to manage startups
# powerful punch that takes time to charge up
def one_punch(player, target, action):
    knockback = stun = 0
    skillInfo = fetchSkill(player, "onepunch")

    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._midStartup = True
            player._moves.append(action)
        else:
            player._moves.append(("NoMove", None))
        return 0, 0
    
    player._midStartup = False
    
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
            player._midStartup = False
            return skillInfo
        else:
            if skillInfo == -1:
                player._midStartup = True
                player._moves.append(action)
            else:
                player._moves.append(("NoMove", None))
    return None


def encumber(player):
    # special state for player after super saiyan duration finishes
    print("START ENCUMBER")
    player._encumberedDuration = 5
    player._encumbered = True
    changeSpeed(player, 1/2)
         
def skill_cancel(player, target, action):
    player._skill_state = False
    player._midStartup = False
    player._moves[player._moveNum] = action
    return None
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