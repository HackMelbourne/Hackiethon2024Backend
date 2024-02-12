from playerActions import attackHit, changeDamage, changeSpeed

GRAVITY = 1
MAX_JUMP_HEIGHT = 2
def proj_knockback(proj, player):
    if proj.xCoord < player._xCoord:
        return -1
    return 1

def updateCooldown(player):
    player._lightAtk.reduceCd(1)
    player._heavyAtk.reduceCd(1)
    player._primarySkill.reduceCd(1)
    player._secondarySkill.reduceCd(1)
    
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
        jsonDict['ProjectileType'] = projectile.type
        jsonDict['projXCoord'].append(projectile.xCoord)
        jsonDict['projYCoord'].append(projectile.yCoord)
    else:
        jsonDict['projXCoord'].append(None)
        jsonDict['projYCoord'].append(None) 
        
def projectile_move(projectiles, knock1, stun1, knock2, stun2, player1, player2,
                    p1_dict, p2_dict):
    for projectileNum in range(len(projectiles)):
        proj_info = projectiles[projectileNum]
        proj_obj = proj_info["projectile"]
        
        if proj_obj.player._id == 1:
            proj_json_dict = p1_dict
        else:
            proj_json_dict = p2_dict
        
        # if exists, then travel
        proj_obj.travel()
        
        # first check if the projectile already travelled its range or offscreen
        if (proj_obj.size == (0,0) or (proj_info["self_stun"] and 
                            proj_obj.player._moves[-1][0] == "skill_cancel")):
            # remove projectile from array
            projectiles.pop(projectileNum)
            projectileToJson(proj_obj, proj_json_dict, False)
            continue
        
        # if still existst then log
        projectileToJson(proj_obj, proj_json_dict, True)
        print(f"PROJ {proj_obj.xCoord, proj_obj.yCoord}")
        
        # check for projectiles colliding with each other
        for nextProjNum in range(len(projectiles)):
            nextproj_obj = projectiles[nextProjNum]["projectile"]
            if (nextProjNum != projectileNum and 
                proj_obj.checkProjCollision(nextproj_obj)):
                    projectiles.pop(projectileNum)
                    projectiles.pop(nextproj_obj)
                    break
        
        # list of ids of projectiles currently on screen
        projectile_ids = [projectile_obj["projectile"].id for projectile_obj in projectiles]
        # check if this projectile still exists
        if proj_obj.id in projectile_ids:
            # get projectile info and initialise
            proj_info = projectiles[projectileNum]
            proj_knock1 = proj_knock2 = proj_stun1 = proj_stun2 = 0
            # collision checks and attack checks
            if proj_obj.checkCollision(player1):
                # if explosive, the knockback depends on where the enemy was
                knockback = proj_info["knockback"] * proj_knockback(proj_obj, player1)
                proj_knock2, proj_stun2 = attackHit(proj_obj, player1,
                                                proj_info["damage"],
                                                proj_obj.size[0],
                                                proj_obj.size[1],
                                                proj_info["blockable"],
                                                knockback,
                                                proj_info["stun"])
            if proj_obj.checkCollision(player2):
                knockback = proj_info["knockback"] * proj_knockback(proj_obj, player2)
                proj_knock1, proj_stun1 = attackHit(proj_obj, player2,
                                                proj_info["damage"],
                                                proj_obj.size[0],
                                                proj_obj.size[1],
                                                proj_info["blockable"],
                                                knockback,
                                                proj_info["stun"])
            # if attack and projectile hits target at same time, use
            # total knockback and highest stun
            
            # this is if the projectile explodes
            if proj_obj.trait == "explode":
                proj_obj.size = (0,0)
            
            knock1 += proj_knock1
            stun1 = max(stun1, proj_stun1)
            knock2 += proj_knock2
            stun2 = max(stun2, proj_stun2)
              
            # then pop the projectile if it hit or expires, else continue travel
            if proj_knock1 or proj_knock2 or proj_obj.size == (0,0):
                projectileToJson(proj_obj, proj_json_dict, False)
                projectiles.pop(projectileNum)
                # then unstun caster if the projectile skill has self stun
                if proj_info["self_stun"]:
                    proj_obj.player._skill_state = False
              
    return projectiles, knock1, stun1, knock2, stun2  

def updateBuffs(player):
    if player._currentBuffDuration > 0:
        player._currentBuffDuration -= 1
    elif player._currentBuffDuration == 0:
        # check if any buffs active, if they are, remove them
        if player._atkbuff:
            changeDamage(player, -player._atkbuff)
            player._atkbuff = 0
        if player._speed != 1:
            changeSpeed(player, 0)
            player._speed = 1
