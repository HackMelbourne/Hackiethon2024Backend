#checks if a "move" is valid
def validMove(moveset, player, enemy):
    valid_moves = [-1,0,1]
    #TODO prevent double jumps
    if moveset[0] not in valid_moves or moveset[1] not in valid_moves:
        return False
    # check if out of bound 
    # *assuming the screen is 0-30
    elif (player._xCoord + player.direction * moveset[0] <0 or 
          player._xCoord + player.direction * moveset[0] >30):
        return False
    #UPDATE: invalid if next to each other and moving towards the other
    elif (abs(player._xCoord - enemy._xCoord) == moveset[0]):
        return False
    return True

#returns if player1 or player2 switch sides
def flip_orientation(player1, player2):
    player1_x = player1.get_pos()[0]
    player2_x = player2.get_pos()[0]
    if player1_x > player2_x:
        # should flip orientations if they switch sides
        return True
    return False

#for testing: prints player info
def playerInfo(player, playerName, action):
    print(f"{playerName} POS: {player._xCoord, player._yCoord}, {player._hp}, midair: {player.midair}, blocking: {player._blocking, player.block.shieldHp}, stun: {player._stun}, facing: {player.direction}")
    print(f"NEXT ACTION: {action}")