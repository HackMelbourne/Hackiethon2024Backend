def validMove(moveset):
    valid_moves = [-1,0,1]
    if moveset[0] in valid_moves and moveset[1] in valid_moves:
        return True
    return False