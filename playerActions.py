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
        if validMove(action[1], player, enemy) and not player.midair:
            player.blocking = False
            player.block.regenShield() 
            player.moves.append(action)
            player.xCoord += player.direction * action[1][0]
            player.yCoord += action[1][1]
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
def attackHit(player, target, damage, atk_range, blockable, knockback, stun):
    # This is fine if we only allow horizontal attacks
    if (abs(player.xCoord-target.xCoord) <= atk_range and player.yCoord == target.yCoord):
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

valid_actions = {"attack": attack, "block": block, "move": move, "dash_attack": dash_atk}