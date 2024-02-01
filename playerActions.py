from test import validMove

# used to correct position of player if they move offscreen
def correctPos(player):
    if player._xCoord < 0:
        player._xCoord = 0
    elif player._xCoord > 30:
        player._xCoord = 30
    return

def move(player, enemy, action):
    if (action[0] == "move"):
        moveAction = player._move.activateSkill(action[1])[1]
        if validMove(moveAction, player, enemy) and not player._midair:
            player._blocking = False
            player._block.regenShield() 
            player._moves.append(action)
            player._xCoord += player._direction * moveAction[0]
            player._yCoord += moveAction[1]
            if player._yCoord > 0:
                player._midair = True
            if moveAction[0] and moveAction[1]:
                # this is diagonal jump
                player._velocity += player._direction * moveAction[0]
        else:    
            print("Invalid movement")
    return None, None

def block(player, target, action):
    if (action[0] == "block"):
        player._moves.append(action)
        player._blocking = True
    return None, None

#returns the action if not on cooldown or mid-startup.
# if on cd, return current cd, or -1 if mid startup
def fetchAttack(player, attackType):
    if attackType == "light":
        return player._lightAtk.activateSkill()
    elif attackType == "heavy":
        return player._heavyAtk.activateSkill()
    else:
        raise Exception("Invalid attack type!")


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
    if (action[0] == "attack"):
        player._blocking = False
        player._block.regenShield() 

        # 2 types of attack, light and heavy
        # action should be like ("attack", "light/heavy")
        attack = fetchAttack(player, action[1])

        
        # no action if attack is on cooldown or previous attack is still in startup
        if isinstance(attack, int):
            return 0, 0
        # gets only the attack info, doesn't include "light"/"heavy"
        attack = attack[1:]
        player._moves.append(action)
        
        # performs the actual attack using fetched attack info
        return attackHit(player, target, *attack)
    return 0, 0

# helper function for all skills
# return cooldown/startup if on cooldown/startup
# else return skill type and related attributes
def fetchSkill(player, skillClass):
    if player._primarySkill.skillType == skillClass:
        return player._primarySkill.activateSkill()
    elif player._secondarySkill.skillType == skillClass:
        return player._secondarySkill.activateSkill()
    else:
        raise Exception("Player does not have this skill!")
    
def changeSpeed(player, speed):
    player._primarySkill.startup -= speed
    player._secondarySkill.startup -= speed
    player._lightAtk.startup -= speed
    player._heavyAtk.startup -= speed
    player._block.startup -= speed
    if player._primarySkill.startup < 0:
        player._primarySkill.startup = 0
    if player._secondarySkill.startup < 0:
        player._secondarySkill.startup = 0
    if player._lightAtk.startup < 0:
        player._lightAtk.startup = 0
    if player._heavyAtk.startup < 0:
        player._heavyAtk.startup = 0
    if player._block.startup < 0:
        player._block.startup = 0

def changeDamage(player, buffValue):
    if player._primarySkill.skillType in attack_actions:
        player._primarySkill.damageBuff(buffValue)
    if player._secondarySkill.skillType in attack_actions:
        player._secondarySkill.damageBuff(buffValue)
    player._lightAtk.damageBuff(buffValue)
    player._heavyAtk.damageBuff(buffValue)

# dashes towards target, deals damage along the way
def dash_atk(player, target, action):
    knockback = stun = 0
    if (action[0] == "dash_attack"):
        skillInfo = fetchSkill(player, "dash_attack")
        # if skill on cooldown or in startup
        if isinstance(skillInfo, int):
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
    if (action[0] == "uppercut"):
        skillInfo = fetchSkill(player, "uppercut")
        # if skill on cooldown or in startup
        if isinstance(skillInfo, int):
            return 0, 0
        
        # so now, skillInfo = damage, 
        skillInfo = skillInfo[1:]
        player._moves.append(action)

        knockback, stun = attackHit(player, target, *skillInfo)
        correctPos(player)
    return knockback, stun

# teleport skill, use ("teleport", 1) to teleport towards target, -1 to teleport away
def teleport(player, target, action):
    if (action[0] == "teleport"):
        skillInfo = fetchSkill(player, "teleport")
        if isinstance(skillInfo, int):
            return 0, 0

        distance = skillInfo[1]
        player._moves.append(action)

        player._xCoord += distance * action[1] * player._direction
        correctPos(player)
    return None

# buffs damage and speed for player
def super_saiyan(player, target, action):
    if (action[0] == "super_saiyan"):
        skillInfo = fetchSkill(player, "super_saiyan")
        if isinstance(skillInfo, int):
            return 0, 0
        
        speedBuff = skillInfo[1][0]
        atkBuff = skillInfo[1][1]
        player._moves.append(action)
        changeSpeed(player, speedBuff)
        changeDamage(player, atkBuff)
        
    return None
    

# heals player for given amount of hp
def meditate(player, target, action):
    if (action[0] == "heal"):
        skillInfo = fetchSkill(player, "heal")
        if isinstance(skillInfo, int):
            return 0, 0
        
        healVal = skillInfo[1]
        player._moves.append(action)
        
        player._hp += healVal
    return None    
    
# similar layout to dash_atk
# TODO : has startup, add function to manage startups
# powerful punch that takes time to charge up
def one_punch(player, target, action):
    if (action[0] == "one_punch"):
        skillInfo = fetchSkill(player, "one_punch")
        if isinstance(skillInfo, int):
            return 0, 0
        
        skillInfo = skillInfo[1:]
        player._moves.append(action)

        knockback, stun = attackHit(player, target, *skillInfo)
    return knockback, stun
        
def hadoken(player, target, action):
    return fetchProjectileSkill(player, "hadoken", action)
        
def lasso(player, target, action):
    return fetchProjectileSkill(player, "lasso", action)

def fetchProjectileSkill(player, projectileName, action):
    if (action[0] == "hadoken"):
        skillInfo = fetchSkill(player, projectileName)
        if not isinstance(skillInfo, int):
            # returns dictionary containing projectile info
            skillInfo = skillInfo[-1]
            return skillInfo
    return None

# for actions that do not deal damage
defense_actions = {"block": block, "move": move, "teleport": teleport, 
                   "super_saiyan": super_saiyan, "meditate": meditate}

# for actions that deal damage
attack_actions = {"attack": attack, "dash_attack": dash_atk,
                  "uppercut": uppercut, "one_punch": one_punch
                  }

# for projectile actions
projectile_actions = {"hadoken":hadoken, "lasso":lasso}

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