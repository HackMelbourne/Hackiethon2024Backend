from test import validMove

# used to correct position of player if they move offscreen
def correctPos(player):
    if player.xCoord < 0:
        player.xCoord = 0
    elif player.xCoord > 30:
        player.xCoord = 30
    return

def move(player, enemy, action):
    if (action[0] == "move"):
        moveAction = player.move.activateSkill(action[1])[1]
        if validMove(moveAction, player, enemy) and not player.midair:
            player.blocking = False
            player.block.regenShield() 
            player.moves.append(action)
            player.xCoord += player.direction * moveAction[0]
            player.yCoord += moveAction[1]
            if player.yCoord > 0:
                player.midair = True
        else:    
            print("Invalid movement")
    return None, None

def block(player, target, action):
    if (action[0] == "block"):
        player.moves.append(action)
        player.blocking = True
    return None, None

#returns the action if not on cooldown or mid-startup.
# if on cd, return current cd, or -1 if mid startup
def fetchAttack(player, attackType):
    if attackType == "light":
        return player.lightAtk.activateSkill()
    elif attackType == "heavy":
        return player.heavyAtk.activateSkill()
    else:
        raise Exception("Invalid attack type!")


# Helper function for all attack types and attack skills    
def attackHit(player, target, damage, atk_range, vertical, blockable, knockback, stun):
    # checks if target is within the horizontal and vertical attack range
    if (abs(player.xCoord-target.xCoord) <= atk_range and 
        player.yCoord + vertical >= target.yCoord):
        # can be changed later : no knockback if block or stunned
        if target.blocking or target.stun:
            knockback = 0
        # if target is blocking
        if(target.blocking and blockable):
            #parry if block is frame perfect: the target blocks as attack comes out
            if target.moves[-1] == "block" and target.moves[-2] != "block":
                player.stun = 2
            elif target.blocking:
                #target is stunned if their shield breaks from damage taken
                target.stun += target.block.shieldDmg(damage)
            return 0, 0
        else:
            target.hp -= damage
            return knockback, stun
    return 0, 0

# Light and heavy attacks
def attack(player,target, action):
    if (action[0] == "attack"):
        player.blocking = False
        player.block.regenShield() 

        # 2 types of attack, light and heavy
        # action should be like ("attack", "light/heavy")
        attack = fetchAttack(player, action[1])

        
        # no action if attack is on cooldown or previous attack is still in startup
        if isinstance(attack, int):
            return 0, 0
        # gets only the attack info, doesn't include "light"/"heavy"
        attack = attack[1:]
        player.moves.append(action)
        
        # performs the actual attack using fetched attack info
        return attackHit(player, target, *attack)
    return 0, 0

# helper function for all skills
# return cooldown/startup if on cooldown/startup
# else return skill type and related attributes
def fetchSkill(player, skillClass):
    if player.primarySkill.skillType == skillClass:
        return player.primarySkill.activateSkill()
    elif player.secondarySkill.skillType == skillClass:
        return player.secondarySkill.activateSkill()
    else:
        raise Exception("Player does not have this skill!")
    
def changeSpeed(player, speed):
    player.primarySkill.startup += speed
    player.secondarySkill.startup += speed
    player.lightAtk.startup += speed
    player.heavyAtk.startup += speed
    player.block.startup += speed
    if player.primarySkill.startup < 0:
        player.primarySkill.startup = 0
    if player.secondarySkill.startup < 0:
        player.secondarySkill.startup = 0
    if player.lightAtk.startup < 0:
        player.lightAtk.startup = 0
    if player.heavyAtk.startup < 0:
        player.heavyAtk.startup = 0
    if player.block.startup < 0:
        player.block.startup = 0

def changeDamage(player, buffValue):
    if player.primarySkill.skillType in attack_actions:
        player.primarySkill.damageBuff(buffValue)
    if player.secondarySkill.skillType in attack_actions:
        player.secondarySkill.damageBuff(buffValue)
    player.lightAtk.damageBuff(buffValue)
    player.heavyAtk.damageBuff(buffValue)

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
        player.moves.append(action)

        knockback, stun = attackHit(player, target, *skillInfo)
        player.xCoord += player.direction * skillInfo[1]
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
        player.moves.append(action)

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
        player.moves.append(action)

        player.xCoord += distance * action[1] * player.direction
        correctPos(player)
    return None

# buffs damage and speed for player
def super_saiyan(player, target, action):
    if (action[0] == "super_saiyan"):
        skillInfo = fetchSkill(player, "super_saiyan")
        if isinstance(skillInfo, int):
            return 0, 0
        
    # todo add logic
    return None
    

# heals player for given amount of hp
def meditate(player, target, action):
    if (action[0] == "heal"):
        skillInfo = fetchSkill(player, "heal")
        if isinstance(skillInfo, int):
            return 0, 0
        
        healVal = skillInfo[1]
        player.moves.append(action)
        
        player.hp += healVal
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
        player.moves.append(action)

        knockback, stun = attackHit(player, target, *skillInfo)
    return knockback, stun
        

# for actions that do not deal damage
defense_actions = {"block": block, "move": move, "teleport": teleport, 
                   "super_saiyan": super_saiyan, "meditate": meditate}

# for actions that deal damage
attack_actions = {"attack": attack, "dash_attack": dash_atk,
                  "uppercut": uppercut, "one_punch": one_punch}


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