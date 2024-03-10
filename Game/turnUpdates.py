from Game.playerActions import attackHit, changeDamage, changeSpeed, encumber
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

def updateCooldown(player):
    player._lightAtk._reduceCd(1)
    player._heavyAtk._reduceCd(1)
    player._primarySkill._reduceCd(1)
    player._secondarySkill._reduceCd(1)
    player._move._reduceCd(1)
    
# updates current position of player if they are midair or started jumping
def updateMidair(player):
    # check if player should be falling
    collided = False
    if not player._falling:
        player._falling = (player._yCoord >= player._jumpHeight * player._speed)
    # not yet at apex of jump
    if player._midair:
        print(player.get_pos())
        if player._falling: 
            # specifically to check for diagonal jumps, ensure jump arc
            # like _ - - _
            check_point = player._jumpHeight
            print(player.get_past_move(check_point))
            if ((player.get_past_move(check_point)[1] not in ((1,1), (-1,1))) or
                                                    player._airvelo == 0):
                player._yCoord -= GRAVITY
        else:
            player._yCoord += 1 * player._speed
        player._xCoord += player._velocity * player._speed
        updated = True
        print(player.get_pos())

    # player has landed, reset midair attributes
    if player._yCoord <= 0 and player._falling: 
        player._midair = player._falling = False
        # set a movestun to the player so that they cant jump away right after
        player._move._movestun_on_fall(1)
    
    if not player._midair:
        player._velocity = 0
        player._airvelo = 0
        player._jumpheight = MAX_JUMP_HEIGHT
        
    return collided

def playerToJson(player, jsonDict, fill=False, start=False, checkHurt=False):
    jsonDict['hp'].append(player._hp)
    jsonDict['xCoord'].append(player._xCoord)
    jsonDict['yCoord'].append(player._yCoord)
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
    

# change fill to True if double
def projectileToJson(projectile, jsonDict, travelling, fill=JSONFILL):
    reps = 1
    if fill:
        reps = 2
    for i in range(reps):
        if travelling and projectile:
            jsonDict['ProjectileType'] = projectile._type
            jsonDict['projXCoord'].append(projectile._xCoord)
            jsonDict['projYCoord'].append(projectile._yCoord)
        else:
            jsonDict['projXCoord'].append(-1)
            jsonDict['projYCoord'].append(-1) 
        
def projectile_move(projectiles, knock1, stun1, knock2, stun2, player1, player2,
                    p1_dict, p2_dict):
    #TODO add None for no projectiles, even when not yet casted
    
    # check if no projectiles by player1 and player2
    exist_proj_1 = exist_proj_2 = True
    curr_proj_ids = [proj["projectile"]._player._id for proj in projectiles]
    if 1 not in curr_proj_ids:
        projectileToJson(None, p1_dict, False)
        check_json_updated("p1")
    if 2 not in curr_proj_ids:
        projectileToJson(None, p2_dict, False)
        check_json_updated("p2")
    
    num_proj = len(projectiles)  
    # now check for existing projectiles
    for proj_index in range(num_proj):
        proj_info = projectiles[proj_index]
        if proj_info == None:
            continue
        proj_obj = proj_info["projectile"]
        proj_knock1 = proj_knock2 = proj_stun1 = proj_stun2 = 0
        
        if proj_obj._player._id == 1:
            proj_json_dict = p1_dict
            enemy_proj_dict = p2_dict
            name = "p1"
        else:
            proj_json_dict = p2_dict
            enemy_proj_dict = p1_dict
            name = "p2"
        
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
            #print("hit player")
            projectiles[proj_index] = None # to set destroyed projectiles
            projectileToJson(proj_obj, proj_json_dict, False)
            check_json_updated(name)
            if proj_knock1:
                player1._skill_state = False
            if proj_knock2:
                player2._skill_state = False
            # uncomment if make nomove if walk into projectile
            '''
            if proj_knock1:
                print(player2._moves[-1])
                player2._moves[-1] = ("NoMove", None)
            
            if proj_knock2:
                print(player1._moves[-1])
                player1._moves[-1] = ("NoMove", None)
            '''
            continue
        # if exists, then travel
        #print("Pre travel")
        proj_obj._travel()
        #print(proj_obj._size)
        # first check if the projectile already travelled its range or offscreen
        if (proj_obj._size == (0,0) or (proj_info["self_stun"] and 
                            proj_obj._player._moves[-1][0] == "skill_cancel")):
            # remove projectile from array
            projectiles[proj_index] = None
            projectileToJson(proj_obj, proj_json_dict, False)
            check_json_updated(name)
            proj_obj._player._skill_state = False
            continue
        #print(f"Here at {proj_obj.get_pos()}")
        # if still existst then log
        #print(f"PROJ {proj_obj.get_pos()}")
        # check for projectiles colliding with each other
        cont = False
        for nextProjNum in range(len(projectiles)):
            nextProj = projectiles[nextProjNum]
            if nextProj:
                nextproj_obj = nextProj["projectile"]
                if (nextproj_obj._id != proj_obj._id and 
                    proj_obj._checkProjCollision(nextproj_obj)):
                        projectiles[proj_index] = None
                        projectiles[nextProjNum] = None
                        print("pop both")
                        projectileToJson(proj_obj, proj_json_dict, False)
                        projectileToJson(nextproj_obj, enemy_proj_dict, False)
                        proj_obj._player._skill_state = False
                        nextproj_obj._player._skill_state = False
                        cont = True
                        break
        if cont:
            continue

        # check if this projectile still exists
        if projectiles[proj_index]:
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
                check_json_updated(name)
                projectiles[proj_index] = None
                # then unstun caster if the projectile skill has self stun
                proj_obj._player._skill_state = False
            else:
                projectileToJson(proj_obj, proj_json_dict, True)
                check_json_updated(name)
        current_proj(projectiles)
        
    #after final calculation, remove all destroyed projectiles
    projectiles = [proj for proj in projectiles if proj]
      
    print(f"P1: {player1.get_pos()}, P2: {player2.get_pos()}")
    if knock1:
        print("hit p2")
        print(knock1)
    if knock2:
        print("hit p1")
        print(knock2)      
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
                                proj["stun"],
                                surehit=True)
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
