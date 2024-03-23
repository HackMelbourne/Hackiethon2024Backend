from Game.playerActions import attackHit, changeDamage
from Game.gameSettings import *
GRAVITY = 1
MAX_JUMP_HEIGHT = 2
def projKnockback(proj, player):
    knockback = 1
    # checking physics for projectiles that can hit from behind
    if proj._type == "grenade":
        proj._direction = 1
        if player._xCoord < proj._xCoord:
            knockback = -1
        elif player._xCoord > proj._xCoord:
            knockback = 1
        else:
            # same xcoord = no knockback
            knockback = 0
    return knockback

# Reduces cooldown for all actions per turn
def updateCooldown(player):
    player._light_atk._reduceCd(1)
    player._heavy_atk._reduceCd(1)
    player._primary_skill._reduceCd(1)
    player._secondary_skill._reduceCd(1)
    player._move._reduceCd(1)
    
# Updates current position of player if they are midair or started jumping
def updateMidair(player):
    # Check if player should be falling
    if not player._falling:
        player._falling = (player._yCoord >= player._jump_height * player._speed)
    # Not yet at apex of jump
    if player._midair:
        if player._falling: 
            # Specifically to check for diagonal jumps, ensure jump arc
            check_point = player._jump_height
            if ((player.get_past_move(check_point)[1] not in ((0,1), (1,1), (-1,1))) or
                                                    player._airvelo == 0):
                player._yCoord -= GRAVITY
        else:
            player._yCoord += 1 * player._speed
        player._xCoord += player._velocity * player._speed

    # player has landed, reset midair attributes
    if player._yCoord == 0 and player._falling: 
        player._midair = player._falling = False
        # set a movestun to the player so that they cant jump away right after
        player._move._movestun_on_fall(2)
    
    if not player._midair:
        player._velocity = 0
        player._airvelo = 0

def playerToJson(player, jsonDict, fill=False, start=False, checkHurt=False):
    jsonDict['hp'].append(player._hp)
    jsonDict['xCoord'].append(player._xCoord)
    jsonDict['yCoord'].append(player._yCoord)
    jsonDict['direction'].append(player._direction)
    if not fill:

        jsonDict['state'].append(player._moves[-1][0])
        jsonDict['actionType'].append(player._moves[-1][1])
    else:
        if start:
            jsonDict['state'].append("NoMove")
            jsonDict['actionType'].append("NoMove")
        elif checkHurt and ifHurt(jsonDict):
            jsonDict['state'].append("Hurt")
            jsonDict['actionType'].append("Hurt")
        else:
            jsonDict['state'].append(player._moves[-1][0])
            jsonDict['actionType'].append("Fill")
    jsonDict['stun'].append(player._stun)
    jsonDict['midair'].append(player._midair)
    jsonDict['falling'].append(player._falling)
    
def proj_json_record(jsonDict, projectile, travelling):
    if travelling and projectile:
        jsonDict['ProjectileType'] = projectile._type
        jsonDict['projXCoord'].append(projectile._xCoord)
        jsonDict['projYCoord'].append(projectile._yCoord)
    else:
        jsonDict['projXCoord'].append(-1)
        jsonDict['projYCoord'].append(-1) 
    
# change fill to True if double
def projectileToJson(projectile, jsonDict, travelling, fill=False, midtickhit=False):
    proj_json_record(jsonDict, projectile, travelling)
    if not fill:
        if midtickhit:
            proj_json_record(jsonDict, projectile, False)
        else:
            proj_json_record(jsonDict, projectile, travelling)
        
def projectile_move(projectiles, knock1, stun1, knock2, stun2, player1, player2,
                    p1_dict, p2_dict):
    #TODO add None for no projectiles, even when not yet casted
    
    # check if no projectiles by player1 and player2
    curr_proj_ids = [proj["projectile"]._player._id for proj in projectiles]
    if 1 not in curr_proj_ids:
        projectileToJson(None, p1_dict, False)
        #check_json_updated("p1")
    if 2 not in curr_proj_ids:
        projectileToJson(None, p2_dict, False)
        #check_json_updated("p2")

    # Iterate over existing projectiles
    for proj_index in range(len(projectiles)):
        proj_info = projectiles[proj_index]
        if proj_info == None:
            continue
        proj_obj = proj_info["projectile"]
        proj_knock1 = proj_knock2 = proj_stun1 = proj_stun2 = 0
        
        # get the projectile dictionary
        if proj_obj._player._id == 1:
            proj_json_dict = p1_dict
            enemy_proj_dict = p2_dict
        else: # player id == 2
            proj_json_dict = p2_dict
            enemy_proj_dict = p1_dict
            
        
        # Checks if the enemy player moves into the projectile before travel
        proj_knock2, proj_stun2 = projCollisionCheck(proj_info, player1)
        proj_knock1, proj_stun1 = projCollisionCheck(proj_info, player2)
        knock1 += proj_knock1
        stun1 = max(stun1, proj_stun1)
        knock2 += proj_knock2
        stun2 = max(stun2, proj_stun2)
        if proj_knock1 or proj_stun1 or proj_knock2 or proj_stun2:
            # Player got hit, so remove projectile
            projectiles[proj_index] = None # to set destroyed projectiles
            projectileToJson(proj_obj, proj_json_dict, True, midtickhit=True)
            proj_obj = None
            #check_json_updated(name)
            if proj_knock1 or proj_stun1:
                player1._skill_state = False
            if proj_knock2 or proj_stun2:
                player2._skill_state = False
            continue
        
        
        # If exists, then travel
        proj_obj._travel()
        
        # First check if the projectile already travelled its range or offscreen
        if (proj_obj._size == (0,0) or 
            (proj_info["self_stun"] and proj_obj._player._skill_state == False)):
            # remove projectile from array
            projectiles[proj_index] = None
            projectileToJson(proj_obj, proj_json_dict, False)
            #check_json_updated(name)
            proj_obj._player._skill_state = False
            proj_obj = None
            continue
        
        # check for projectiles colliding with each other
        for nextProjNum in range(len(projectiles)):
            nextProj = projectiles[nextProjNum]
            if nextProj:
                nextproj_obj = nextProj["projectile"]
                if (nextproj_obj._id != proj_obj._id and 
                    proj_obj._checkProjCollision(nextproj_obj)):
                        # Projectiles take collision damage
                        php = proj_obj._collisionHp
                        nphp = nextproj_obj._collisionHp
                        proj_obj.take_col_dmg(nphp)
                        nextproj_obj.take_col_dmg(php)
                        # Projectiles which take enough collision damage get destroyed
                        if proj_obj._size == (0,0):
                            projectiles[proj_index] = None
                            projectileToJson(proj_obj, proj_json_dict, False)
                            proj_obj._player._skill_state = False
                            proj_obj = None
                        if nextproj_obj._size == (0,0):
                            projectiles[nextProjNum] = None
                            projectileToJson(nextproj_obj, enemy_proj_dict, False)
                            nextproj_obj._player._skill_state = False
                            nextproj_obj = None
                        # At least one projectile will be destroyed
                        break
        
        # Check if this projectile still exists
        if projectiles[proj_index]:
            # collision checks and attack checks
            proj_knock2, proj_stun2 = projCollisionCheck(proj_info, player1)
            proj_knock1, proj_stun1 = projCollisionCheck(proj_info, player2)
            # if attack and projectile hits target at same time, use
            # total knockback and highest stun
            
            # This is if the projectile explodes
            if proj_obj._trait == "explode" or proj_stun1 or proj_stun2:
                proj_obj._size = (0,0)
            
            # Recalculate knockbacks and stuns
            knock1 += proj_knock1
            if not stun1:
                stun1 = proj_stun1
            knock2 += proj_knock2
            if not stun2:
                stun2 = proj_stun2

            # Then pop the projectile if it hit or expires, else continue travel
            if proj_obj._size == (0,0):
                if proj_knock1 or proj_knock2 or proj_stun1 or proj_stun2:
                    projectileToJson(proj_obj, proj_json_dict, False, midtickhit=True)
                else:
                    projectileToJson(proj_obj, proj_json_dict, False)
                #check_json_updated(name)
                projectiles[proj_index] = None
                # then unstun caster if the projectile skill has self stun -- Unused
                proj_obj._player._skill_state = False
                proj_obj = None
            else:
                projectileToJson(proj_obj, proj_json_dict, True)
        
    #after final calculation, remove all destroyed projectiles
    projectiles = [proj for proj in projectiles if proj]
    proj_obj = None
    return projectiles, knock1, stun1, knock2, stun2  

def projCollisionCheck(proj, player):
    proj_obj = proj["projectile"]
    knockback = proj["knockback"] * projKnockback(proj_obj, player)
    if proj_obj._checkCollision(player):
        knockback, stun = attackHit(proj_obj, player,
                                proj["damage"],
                                proj_obj._size[0],
                                proj_obj._size[1],
                                proj["blockable"],
                                knockback,
                                proj["stun"],
                                surehit=True)
    else:
        knockback = stun = 0
    return knockback, stun

def current_proj(projectiles):
    print("Current projectiles: ")
    for proj in projectiles:
        if proj:
            print(proj["projectile"]._player._id) 
        
def updateBuffs(player):
    if player._curr_buff_duration > 0:
        player._curr_buff_duration -= 1
    elif player._curr_buff_duration == 0:
        # check if any buffs active, if they are, remove them
        #if player._atkbuff or (player._speed != 1) :
            #encumber(player)
        if player._atkbuff:
            changeDamage(player, 0)
            player._atkbuff = 0
        if player._defense > 1:
            player._defense = 1
            player._superarmor = False
        if player._jump_height > player._default_jump_height:
            player._jump_height = player._default_jump_height
  
def checkDeath(player):
    if player.get_hp() <= 0:
        player._hp = 0
        return True
    return False

def updateStun(player):
    if player._stun > 0:
        player._stun -= 1
        
def updateRecovery(player):
    if player._recovery > 0:
        player._recovery -= 1
        
        
def check_json_updated(name):
    print(f"{name} updated")
    
def ifHurt(playerJson):
    return ((playerJson["hp"][-1] < playerJson["hp"][-3]) or 
            (playerJson["hp"][-1] < playerJson["hp"][-2]))
