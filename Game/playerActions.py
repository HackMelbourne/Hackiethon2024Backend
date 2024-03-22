from Game.test import validMove, correctPos
from Game.gameSettings import HP, PARRYSTUN

# To use an action, use activateSkill to get a movevalue
# Checks if it is on cooldown or not
# If on cooldown or in startup, returns an integer value: -1 if in startup
# Then appends to actual movelist 

# For basic movement actions - action = ("move", moveval)
# moveval can be (1,0), (1,1), (0,1), (-1,0), (-1,1)
def move(player, enemy, action):
    moveAction = player._move._activateSkill(action[1])
    if isinstance(moveAction, int):
        # weird, but is on cooldown or startup
        if moveAction == -1:
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            # cooldown
            player._moves.append(("NoMove", "cooldown"))
        return True      
    
    player._blocking = False
    player._block._regenShield()
    moveAction = moveAction[1]
    # Don't actually move until reach outside function
    cached_move = [0,0]
    # Can only move if not midair
    if validMove(moveAction, player) and not player._midair:
        # has vertical logic
        if moveAction[1]:
            player._midair = True
            cached_move[1] += 1
            if moveAction[0]:
                # This is a diagonal jump
                # Calculate midair horizontal velocity based on speed and direction
                player._velocity = player._direction * moveAction[0] * player._speed
                cached_move[0] += player._velocity
            player._jump_height *= player._speed
            player._airvelo = player._jump_height
        else:
            # No vertical logic, simple horizontal movement 
            cached_move[0] += player._direction * moveAction[0] * player._speed   
        player._moves.append(action)
    else:
        player._moves.append(("NoMove", None))
    return cached_move
        
# Resets block to default values
def reset_block(player):
    player._block._regenShield()
    player._blocking = False
    
# Do block: no reason to use activate skill
def block(player, target, action):
    player._moves.append((action[0], "activate"))
    player._blocking = True
    return True

# Get normal attack info
def fetchAttack(player, attackType):
    returnVal = None
    if attackType == "light":
        returnVal = player._light_atk._activateSkill()
        if not isinstance(returnVal, int):
            # casted skill successfully, so put into recovery
            player._recovery += player._light_atk._recovery
    elif attackType == "heavy":
        returnVal = player._heavy_atk._activateSkill()
        if not isinstance(returnVal, int):
            # casted skill successfully, so put into recovery
            player._recovery += player._heavy_atk._recovery
    return returnVal

# Check if a normal attack combo was casted successfully
def check_atk_combo(player, attack):
    if len(player._inputs) < 3:
        return False
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
 
# Goes to previous move that isnt startup       
def go_to_prev_atk(player, move, start):
    while player._moves[start] == move:
        start -= 1
    return start

# Helper function for all attack types and attack skills    
def attackHit(player, target, damage, atk_range, vertical, blockable, knockback, stun, surehit=False):
    # Checks if target is within the horizontal and vertical attack range
    player_x, player_y = player.get_pos()
    target_x, target_y = target.get_pos()
    # Surehit is for projectiles since collision check is already done
    if (surehit or (target_x - player_x <= atk_range*player._direction) and 
        (abs(target_y - player_y) <= vertical) and (target_y >= player_y)):
        # If target is blocking
        if(target._blocking and blockable):
            # Parry if block is frame perfect: the target blocks as attack comes out
            if target._moves[-1][0] == "block" and (target.get_past_move(2) != ("block","activate") or len(target._moves) == 1):
                # Can only parry player attacks, not projectiles
                if player._entity_type == "player":
                    player._stun = PARRYSTUN
            elif target._blocking:
                # Target is stunned if their shield breaks from damage taken
                target._stun += target._block._shieldDmg(damage)
            return 0, 0
        else: # If attack actually lands
            damage = int(damage / target._defense)
            if damage < 0:
                damage = 0
            target._hp -= damage
            target._velocity = 0
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
            player._mid_startup = False
        
            # performs the actual attack using fetched attack info
            if check_atk_combo(player, action[0]):
                # buffs damage and knockback for this hit
                # damage buff
                attack[0] = int(attack[0] * 1.5 + 1)
                # knockback buff
                attack[4] += 1
            
            player._moves.append((action[0], "activate"))
            return attackHit(player, target, *attack)
        elif attack == -1:
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", "cooldown"))
    else:
        player._moves.append(("NoMove", None))
    return 0, 0

# helper function for all skills
# return cooldown/startup if on cooldown/startup
# else return skill type and related attributes
def fetchSkill(player, skillClass):
    returnVal = -2
    # if using a skill correctly, reset the startup of every other action 
    if player._primary_skill._skillType == skillClass:
        player._secondary_skill._resetStartup()
        player._heavy_atk._resetStartup()
        player._light_atk._resetStartup()
        player._block._resetStartup()
        player._move._resetStartup()
        returnVal = player._primary_skill._activateSkill()
        
        if not isinstance(returnVal, int):
            # casted skill successfully, so put into recovery
            player._recovery += player._primary_skill._recovery
            
    elif player._secondary_skill._skillType == skillClass:
        player._primary_skill._resetStartup()
        player._heavy_atk._resetStartup()
        player._light_atk._resetStartup()
        player._block._resetStartup()
        player._move._resetStartup()
        returnVal = player._secondary_skill._activateSkill()
        
        if not isinstance(returnVal, int):
            # casted skill successfully, so put into recovery
            player._recovery += player._secondary_skill._recovery
        
    if returnVal == -2:
        raise Exception("Player does not have this skill")
    return returnVal
    
# for super saiyan, increases damage dealt
def changeDamage(player, buffValue):
    if player._primary_skill._skillType in (attack_actions | projectile_actions):
        player._primary_skill._damageBuff(buffValue)
    if player._secondary_skill._skillType in (attack_actions | projectile_actions):
        player._secondary_skill._damageBuff(buffValue)
    
    player._light_atk._damageBuff(buffValue)
    player._heavy_atk._damageBuff(buffValue)
    player._atkbuff += buffValue

# dashes towards target, deals damage along the way
def dash_atk(player, target, action):
    knockback = stun = 0
    skillInfo = fetchSkill(player, "dash_attack")
    # if skill on cooldown or in startup
    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", "cooldown"))
        return 0, 0
    
    player._mid_startup = False
    
    # so now, skillInfo = damage, 
    skillInfo = skillInfo[1:]
    player._moves.append((action[0], "activate"))

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
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", "cooldown"))
        return 0, 0
    
    player._mid_startup = False
    # so now, skillInfo = damage, 
    skillInfo = skillInfo[1:]
    player._moves.append((action[0], "activate"))
    knockback, stun = attackHit(player, target, *skillInfo)
    correctPos(player)
    return knockback, stun

# teleport skill, use ("teleport", 1) to teleport towards target, -1 to teleport away
def teleport(player, target, action):
    skillInfo = fetchSkill(player, "teleport")
    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", "cooldown"))
        return True
    
    player._mid_startup = False

    distance = skillInfo[1]
    # default teleport is backwards
    if action[1] and action[1] == 1:
        tp_direction = 1
    else:
        tp_direction = -1
    #tp_direction = -1
    player._moves.append((action[0], "activate"))
    player._xCoord += distance * tp_direction * player._direction
    correctPos(player)
    return True

# buffs damage and speed for player
def super_saiyan(player, target, action):
    skillInfo = fetchSkill(player, "super_saiyan")

    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", "cooldown"))
        return True
    
    player._mid_startup = False
    
    atkBuff = skillInfo[1][0]
    duration = skillInfo[1][1]
    player._moves.append((action[0], "activate"))
    # turned off for now since startup and recovery so wack with super saiyan
    changeDamage(player, atkBuff)
    player._curr_buff_duration = duration
    return True
    
# heals player for given amount of hp
def meditate(player, target, action):
    skillInfo = fetchSkill(player, "meditate")

    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", "cooldown"))
        return True
    
    player._mid_startup = False
    
    healVal = skillInfo[1]
    player._moves.append((action[0], "activate"))
    player._hp = min(player._hp + healVal, HP)

    return True   
    
def super_armor(player, target, action):
    skillInfo = fetchSkill(player, "super_armor")

    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", "cooldown"))
        return True
    
    player._mid_startup = False
    
    defBuff = skillInfo[1][0]
    duration = skillInfo[1][1]
    player._moves.append((action[0], "activate"))
    # turned off for now since startup and recovery so wack with super saiyan
    player._defense += defBuff
    player._curr_buff_duration = duration
    player._superarmor = True
    return True

def jump_boost(player, target, action):
    skillInfo = fetchSkill(player, "jump_boost")

    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", "cooldown"))
        return True
    
    player._mid_startup = False
    
    player._jump_height = skillInfo[1][0]
    duration = skillInfo[1][1]
    player._moves.append((action[0], "activate"))
    # turned off for now since startup and recovery so wack with super saiyan
    player._curr_buff_duration = duration
    return True
    
# powerful punch that takes time to charge up
def one_punch(player, target, action):
    knockback = stun = 0
    skillInfo = fetchSkill(player, "onepunch")

    if isinstance(skillInfo, int):
        if skillInfo == -1:
            player._mid_startup = True
            player._moves.append((action[0], "startup"))
        else:
            player._moves.append(("NoMove", "cooldown"))
        return 0, 0
    
    player._mid_startup = False
    
    skillInfo = skillInfo[1:]
    player._moves.append((action[0], "activate"))
    knockback, stun = attackHit(player, target, *skillInfo)
    return knockback, stun
        
def hadoken(player, target, action):
    return fetchProjectileSkill(player, "hadoken", action)

def boomerang(player, target, action):
    return fetchProjectileSkill(player, "boomerang", action)

def grenade(player, target, action):
    return fetchProjectileSkill(player, "grenade", action)

def beartrap(player, target, action):
    return fetchProjectileSkill(player, "beartrap", action)


def fetchProjectileSkill(player, projectileName, action):
    if (action[0] == projectileName):
        skillInfo = fetchSkill(player, projectileName)
        if not isinstance(skillInfo, int):
            # returns dictionary containing projectile info
            skillInfo = skillInfo[-1]
            player._moves.append((action[0], "activate"))
            player._mid_startup = False
            return skillInfo
        else:
            if skillInfo == -1:
                player._mid_startup = True
                player._moves.append((action[0], "startup"))
            else:
                player._moves.append(("NoMove", "cooldown"))
    return None
         
# null function
def nullDef(player, target, action):
    return False

def nullAtk(player, target, action):
    return 0,0

def nullProj(player, target, action):
    return None

# Function dictionaries
# For actions that do not deal damage and auras
defense_actions = {"block": block, "move": move, "teleport": teleport, 
                   "super_saiyan": super_saiyan, "meditate": meditate,
                    "super_armor":super_armor, "jump_boost":jump_boost}

# For actions that deal damage
attack_actions = {"light": attack, "heavy":attack, "dash_attack": dash_atk,
                  "uppercut": uppercut, "onepunch": one_punch}

# For projectile actions : TODO remove lasso and icewall
projectile_actions = {"hadoken":hadoken, "boomerang":boomerang,
                      "grenade":grenade, "beartrap":beartrap}
