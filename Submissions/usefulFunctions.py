
# helpful functions
def get_hp(player):
    return player.get_hp()

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
    return player.primary_on_cd()

def secondary_on_cooldown(player):
    return player.secondary_on_cd()

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
    return player.get_secondary_name