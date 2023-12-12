#checks if a "move" is valid
def validMove(moveset, player, enemy):
    valid_moves = [-1,0,1]
    #TODO prevent double jumps
    if moveset[0] not in valid_moves or moveset[1] not in valid_moves:
        return False
    # check if out of bound 
    # *assuming the screen is 0-30
    elif (player.xCoord - moveset[0] <0 or player.xCoord + moveset[0] >30):
        return False
    #UPDATE: invalid if next to each other and moving towards the other
    elif (abs(player.xCoord - enemy.xCoord) == moveset[0]):
        return False
    return True

#returns if player1 or player2 switch sides
def checkOrientation(player1, player2):
    if player1.xCoord > player2.xCoord:
        # should flip orientations if they switch sides
        return True
    return False

#for testing: prints player info
def playerInfo(player, playerName, action):
    print(f"{playerName}: {action}, {player.xCoord, player.yCoord}, {player.hp}, 
          midair: {player.midair}, blocking: {player.blocking, player.block.shieldHp}, 
          stun: {player.stun}")
    
def pathInvalid(path1, path2):
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    return False