from playerActions import attackHit, changeDamage, changeSpeed, encumber

GRAVITY = 1
MAX_JUMP_HEIGHT = 2
def proj_knockback(proj, player):
    if proj._xCoord < player._xCoord:
        return -1
    return 1

def updateCooldown(player):
    player._lightAtk._reduceCd(1)
    player._heavyAtk._reduceCd(1)
    player._primarySkill._reduceCd(1)
    player._secondarySkill._reduceCd(1)
    
# updates current position of player if they are midair or started jumping
def updateMidair(player):
    # check if player should be falling
    if not player._falling:
        player._falling = (player._yCoord >= player._jumpHeight * player._speed)
    # not yet at apex of jump
    if player._midair:
        if player._falling: 
            # specifically to check for diagonal jumps, ensure jump arc
            # like _ - - _
            if player._moves[-2] != ("move",(1,1)):
                player._yCoord -= GRAVITY
        else:
            player._yCoord += 1 * player._speed
        player._xCoord += player._velocity * player._speed

    # player has landed, reset midair attributes
    if player._yCoord <= 0 and player._falling: 
        player._midair = player._falling = False
        player._velocity = 0
        player._jumpheight = MAX_JUMP_HEIGHT

def playerToJson(player, jsonDict):
    jsonDict['hp'].append(player._hp)
    jsonDict['xCoord'].append(player._xCoord)
    jsonDict['yCoord'].append(player._yCoord)
    jsonDict['state'].append(player._moves[-1][0])
    jsonDict['stun'].append(player._stun)
    jsonDict['midair'].append(player._midair)
    jsonDict['falling'].append(player._falling)

def projectileToJson(projectile, jsonDict, travelling):
    if travelling:
        jsonDict['ProjectileType'] = projectile._type
        jsonDict['projXCoord'].append(projectile._xCoord)
        jsonDict['projYCoord'].append(projectile._yCoord)
    else:
        jsonDict['projXCoord'].append(None)
        jsonDict['projYCoord'].append(None) 
        
def projectile_move(projectiles, knock1, stun1, knock2, stun2, player1, player2,
                    p1_dict, p2_dict):
    for projectileNum in range(len(projectiles)):
        proj_info = projectiles[projectileNum]
        proj_obj = proj_info["projectile"]
        proj_knock1 = proj_knock2 = proj_stun1 = proj_stun2 = 0
        
        if proj_obj._player._id == 1:
            proj_json_dict = p1_dict
        else:
            proj_json_dict = p2_dict
        
        # a bit finicky, but this part checks if enemy moves into projectile before travelling
        proj_knock2, proj_stun2 = proj_collision_check(proj_info, player1)
        proj_knock1, proj_stun1 = proj_collision_check(proj_info, player2)
        knock1 += proj_knock1
        stun1 = max(stun1, proj_stun1)
        knock2 += proj_knock2
        stun2 = max(stun2, proj_stun2)
        if proj_knock1 or proj_knock2:
            # player got hit, so remove projectile
            projectiles.pop(projectileNum)
            projectileToJson(proj_obj, proj_json_dict, False)
            continue
        
        # if exists, then travel
        proj_obj._travel()
        
        # first check if the projectile already travelled its range or offscreen
        if (proj_obj._size == (0,0) or (proj_info["self_stun"] and 
                            proj_obj.player._moves[-1][0] == "skill_cancel")):
            # remove projectile from array
            projectiles.pop(projectileNum)
            projectileToJson(proj_obj, proj_json_dict, False)
            continue
        
        # if still existst then log
        projectileToJson(proj_obj, proj_json_dict, True)
        #print(f"PROJ {proj_obj.get_pos()}")
        
        # check for projectiles colliding with each other
        for nextProjNum in range(len(projectiles)):
            nextproj_obj = projectiles[nextProjNum]["projectile"]
            if (nextProjNum != projectileNum and 
                proj_obj._checkProjCollision(nextproj_obj)):
                    projectiles.pop(projectileNum)
                    projectiles.pop(nextproj_obj)
                    break
        
        # list of ids of projectiles currently on screen
        projectile_ids = [projectile_obj["projectile"]._id for projectile_obj in projectiles]
        # check if this projectile still exists
        if proj_obj._id in projectile_ids:
            # collision checks and attack checks
            proj_knock2, proj_stun2 = proj_collision_check(proj_info, player1)
            proj_knock1, proj_stun1 = proj_collision_check(proj_info, player2)
            # if attack and projectile hits target at same time, use
            # total knockback and highest stun
            
        # this is if the projectile explodes
        if proj_obj._trait == "explode":
            proj_obj._size = (0,0)
        
        # recalculate knockbacks and stuns
        knock1 += proj_knock1
        stun1 = max(stun1, proj_stun1)
        knock2 += proj_knock2
        stun2 = max(stun2, proj_stun2)
            
        # then pop the projectile if it hit or expires, else continue travel
        if proj_knock1 or proj_knock2 or proj_obj._size == (0,0):
            projectileToJson(proj_obj, proj_json_dict, False)
            projectiles.pop(projectileNum)
            # then unstun caster if the projectile skill has self stun
            if proj_info["self_stun"]:
                proj_obj._player._skill_state = False
              
    return projectiles, knock1, stun1, knock2, stun2  

def proj_collision_check(proj, player):
    proj_obj = proj["projectile"]
    knockback = stun = 0
    if proj_obj._checkCollision(player):
        knockback = proj["knockback"] * proj_knockback(proj_obj, player)
        knockback, stun = attackHit(proj_obj, player,
                                proj["damage"],
                                proj_obj._size[0],
                                proj_obj._size[1],
                                proj["blockable"],
                                knockback,
                                proj["stun"])
    return knockback, stun
        
def updateBuffs(player):
    if player._currentBuffDuration > 0:
        player._currentBuffDuration -= 1
    elif player._currentBuffDuration == 0:
        # check if any buffs active, if they are, remove them
        if player._atkbuff or (player._speed != 1) :
            encumber(player)
        if player._atkbuff:
            changeDamage(player, 0)
            player._atkbuff = 0
        if player._speed != 1:
            changeSpeed(player, 0)
            player._speed = 1
        
    if player._encumbered:
        print(f"Duration: {player._encumberedDuration}")
        if player._encumberedDuration > 0 :
            player._encumberedDuration -= 1
        else:
            print("stop encumbered")
            changeDamage(player, 0)
            player._atkbuff = 0  
            changeSpeed(player, 0)
            player._speed = 1
            player._encumbered = False
            
def check_death(player):
    if player.get_hp() <= 0:
        player._hp = 0
        return True
    return False