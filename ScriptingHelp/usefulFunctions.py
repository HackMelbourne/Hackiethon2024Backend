#constants, for easier move return
#movements

JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

NOMOVE = "NoMove"


# helpful functions
def get_hp(player):
    return player.get_hp()

def get_distance(player, enemy):
    return abs(get_pos(player)[0] - get_pos(enemy)[0])

def get_pos(player):
    return player.get_pos()

def get_last_move(player):
    return player.get_last_move()

def get_stun_duration(player):
    return player.get_stun()

def get_block_status(player):
    return player.get_block()

def get_proj_pos(proj):
    return proj.get_pos()

def primary_on_cooldown(player):
    return player.primary_on_cd(get_timer=False)

def secondary_on_cooldown(player):
    return player.secondary_on_cd(get_timer=False)

def heavy_on_cooldown(player):
    return player.heavy_on_cd()

def prim_range(player):
    return player.primary_range()

def seco_range(player):
    return player.secondary_range()

def get_past_move(player, turns):
    return player.get_past_move(turns)

def get_recovery(player):
    return player.get_recovery()

def skill_cancellable(player):
    return player.skill_cancellable()

def get_primary_skill(player):
    return player.get_primary_name()

def get_secondary_skill(player):
    return player.get_secondary_name()

def get_projectile_type(proj):
    return proj.get_type()

def get_primary_cooldown(player):
    return player.primary_on_cd(get_timer=True)

def get_secondary_cooldown(player):
    return player.secondary_on_cd(get_timer=True)
    

# checks if the player has landed this turn: cannot make a movement but can still attack or block
def get_landed(player):
    return player.get_landed()

# tactics

def full_assault(player, enemy, primary, secondary):
    player_x, player_y = get_pos(player)
    enemy_x, enemy_y = get_pos(enemy)
    if player_y == enemy_y and abs(player_x - enemy_x) == 1:
        if not primary_on_cooldown(player):
            return primary
        if not secondary_on_cooldown(player):
            return secondary
        if not heavy_on_cooldown(player):
            return HEAVY
        return LIGHT
    else:
        return FORWARD
    
def scripted_moves(moves_iter):
    try:
        return next(moves_iter)
    except StopIteration:
        return NOMOVE
    
def eric_func(player, enemy, primary, secondary):
    if abs(get_pos(player)[0] - get_pos(enemy)[0]) < 5:
        return primary
    return secondary

def leo_func(player, enemy, primary, secondary):
    distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

    if get_pos(player) == 0 or get_pos(player) == 30:
        return JUMP_FORWARD

    if distance > 3:
        if (not secondary_on_cooldown(player)):
            return secondary
        else:
            return BACK
    elif distance > 2:
        return BACK
    else:
        if (not primary_on_cooldown(player)):
            return primary
        else:
            return BLOCK
        
def spam_second(secondary):
    return secondary
        
        
def winning_strategy(player, enemy, primary, secondary):
    # Check if any skill is available and use it wisely
    if not primary_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= prim_range(player):
        return primary
    elif not secondary_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= seco_range(player):
        return secondary
    elif not heavy_on_cooldown(player) and abs(get_pos(player)[0] - get_pos(enemy)[0]) <= 1:
        return HEAVY

    # Defensive strategy if low on health or enemy is too close
    if get_hp(player) < 20 or abs(get_pos(player)[0] - get_pos(enemy)[0]) < 2:
        # Block if enemy is close and likely to attack
        if abs(get_pos(player)[0] - get_pos(enemy)[0]) == 1:
            return BLOCK
        # Move away from the enemy if possible
        elif get_pos(player)[0] < get_pos(enemy)[0]:
            return BACK
        else:
            return FORWARD

    # Offensive strategy if player has more health
    if get_hp(player) > get_hp(enemy):
        # Close in on the enemy if not in attack range
        if abs(get_pos(player)[0] - get_pos(enemy)[0]) > 1:
            if get_pos(player)[0] < get_pos(enemy)[0]:
                return FORWARD
            else:
                return BACK
        # Use light attack if close and other attacks are on cooldown
        else:
            return LIGHT

    # Default to light attack if nothing else is applicable
    return LIGHT

def heavy_combo(player, enemy):
    player_x, player_y = get_pos(player)
    enemy_x, enemy_y = get_pos(enemy)
    if get_stun_duration(player):
        return NOMOVE
    print(get_past_move(player, 1),get_past_move(player, 2))
    if player_y == enemy_y and abs(player_x - enemy_x) == 1:
        if get_past_move(player, 1) == LIGHT:
            if get_past_move(player, 2) == LIGHT:
                return HEAVY
            else:
                return LIGHT
        else:
            return LIGHT
    return FORWARD

# dont think this works as intended
def eric_func2():
    flip = False
    if flip:
        for i in range(20):
            if i % 5 == 0:
                return HEAVY
            if i == 19:
                flip = True
            return FORWARD
    else:
        for i in range(20):
            if i % 5 == 0:
                return HEAVY
            if i == 19:
                flip = False
            return BACK
