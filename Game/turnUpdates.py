from Game.playerActions import attackHit, changeDamage
from Game.gameSettings import *
GRAVITY = 1
MAX_JUMP_HEIGHT = 2
def proj_knockback(proj, player):
    knockback = 1
    # checking physics for projectiles that can hit from behind
    if proj._type == "grenade" or proj._type == "icewall":
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
    player._lightAtk._reduceCd(1)
    player._heavyAtk._reduceCd(1)
    player._primarySkill._reduceCd(1)
    player._secondarySkill._reduceCd(1)
    player._move._reduceCd(1)
    
# Updates current position of player if they are midair or started jumping
def updateMidair(player):
    # Check if player should be falling
    print(f"Player {player._id}, jump: {player._jumpHeight}, airvelo: {player._airvelo}")
    if not player._falling:
        player._falling = (player._yCoord >= player._jumpHeight * player._speed)
    # Not yet at apex of jump
    if player._midair:
        if player._falling: 
            # Specifically to check for diagonal jumps, ensure jump arc
            check_point = player._jumpHeight
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
        player._move._movestun_on_fall(1)
    
    if not player._midair:
        player._velocity = 0
        player._airvelo = 0
    
    print(f"Player {player._id}, jump: {player._jumpHeight}, airvelo: {player._airvelo}")

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
    #print(player._moves)
    
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

    #print(projectiles)
    print(len(p1_dict['projXCoord']),len(p2_dict['projYCoord']))
    # now check for existing projectiles
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
        else:
            proj_json_dict = p2_dict
            enemy_proj_dict = p1_dict
        
        #print(f"Current: {proj_obj._player._id}")
        # a bit finicky, but this part checks if anything moves into projectile before travelling
        proj_knock2, proj_stun2 = proj_collision_check(proj_info, player1)
        proj_knock1, proj_stun1 = proj_collision_check(proj_info, player2)
        knock1 += proj_knock1
        stun1 = max(stun1, proj_stun1)
        knock2 += proj_knock2
        stun2 = max(stun2, proj_stun2)
        if proj_knock1 or proj_knock2:
            # player got hit, so remove projectile
            projectiles[proj_index] = None # to set destroyed projectiles
            projectileToJson(proj_obj, proj_json_dict, True, midtickhit=True)
            proj_obj = None
            #check_json_updated(name)
            if proj_knock1:
                player1._skill_state = False
            if proj_knock2:
                player2._skill_state = False
            print(len(p1_dict['projXCoord']),len(p2_dict['projYCoord']))
            continue
        # if exists, then travel
        proj_obj._travel()
        # first check if the projectile already travelled its range or offscreen
        if (proj_obj._size == (0,0) or 
            (proj_info["self_stun"] and proj_obj._player._skill_state == False)):
            # remove projectile from array
            projectiles[proj_index] = None
            projectileToJson(proj_obj, proj_json_dict, False)
            #check_json_updated(name)
            proj_obj._player._skill_state = False
            proj_obj = None
            continue
        #print(f"Here at {proj_obj.get_pos()}")
        # if still existst then log
        print(f"PROJ {proj_obj.get_pos()}")
        # check for projectiles colliding with each other
        for nextProjNum in range(len(projectiles)):
            nextProj = projectiles[nextProjNum]
            if nextProj:
                nextproj_obj = nextProj["projectile"]
                if (nextproj_obj._id != proj_obj._id and 
                    proj_obj._checkProjCollision(nextproj_obj)):
                        print("collision damage")
                        proj_obj.take_col_dmg(nextproj_obj._collisionHp)
                        nextproj_obj.take_col_dmg(proj_obj._collisionHp)
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
                        # at least one projectile will be destroyed
                        break
        
        # check if this projectile still exists
        if projectiles[proj_index]:
            # collision checks and attack checks
            proj_knock2, proj_stun2 = proj_collision_check(proj_info, player1)
            proj_knock1, proj_stun1 = proj_collision_check(proj_info, player2)
            # if attack and projectile hits target at same time, use
            # total knockback and highest stun
            
            # this is if the projectile explodes
            # all projectiles for sure have a stun on hit
            if proj_obj._trait == "explode" or proj_stun1 or proj_stun2:
                proj_obj._size = (0,0)
            
            # recalculate knockbacks and stuns
            knock1 += proj_knock1
            stun1 = max(stun1, proj_stun1)
            knock2 += proj_knock2
            stun2 = max(stun2, proj_stun2)

            # then pop the projectile if it hit or expires, else continue travel
            if proj_obj._size == (0,0):
                if proj_knock1 or proj_knock2:
                    projectileToJson(proj_obj, proj_json_dict, False, midtickhit=True)
                else:
                    projectileToJson(proj_obj, proj_json_dict, False)
                #check_json_updated(name)
                projectiles[proj_index] = None
                # then unstun caster if the projectile skill has self stun
                proj_obj._player._skill_state = False
                proj_obj = None
                print(len(p1_dict['projXCoord']),len(p2_dict['projYCoord']))
            else:
                projectileToJson(proj_obj, proj_json_dict, True)
                #check_json_updated(name)
            print(len(p1_dict['projXCoord']),len(p2_dict['projYCoord']))
        #current_proj(projectiles)
        
    #after final calculation, remove all destroyed projectiles
    projectiles = [proj for proj in projectiles if proj]
    proj_obj = None
        
    print(len(p1_dict['projXCoord']),len(p2_dict['projYCoord']))
    return projectiles, knock1, stun1, knock2, stun2  

def proj_collision_check(proj, player):
    proj_obj = proj["projectile"]
    if proj_obj._type == "lasso":
        knockback = proj_obj._lasso_range()
    else:
        knockback = proj["knockback"] * proj_knockback(proj_obj, player)
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
    if player._currentBuffDuration > 0:
        player._currentBuffDuration -= 1
    elif player._currentBuffDuration == 0:
        # check if any buffs active, if they are, remove them
        #if player._atkbuff or (player._speed != 1) :
            #encumber(player)
        if player._atkbuff:
            changeDamage(player, 0)
            player._atkbuff = 0
        if player._defense:
            player._defense = 0
            player._superarmor = False
        if player._jumpHeight > player._defaultJumpHeight:
            player._jumpHeight = player._defaultJumpHeight
    '''   
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
    '''
            
def check_death(player):
    if player.get_hp() <= 0:
        player._hp = 0
        return True
    return False

def update_stun(player):
    if player._stun > 0:
        player._stun -= 1
        
def update_recovery(player):
    if player._recovery > 0:
        player._recovery -= 1
        
        
def check_json_updated(name):
    print(f"{name} updated")
    
def ifHurt(playerJson):
    return ((playerJson["hp"][-1] < playerJson["hp"][-3]) or 
            (playerJson["hp"][-1] < playerJson["hp"][-2]))
