#checks if a "move" is valid
def validMove(moveset, player, enemy):
    valid_moves = [-1,0,1]
    #TODO prevent double jumps
    if moveset[0] not in valid_moves or moveset[1] not in valid_moves:
        return False
    # check if out of bound 
    # *assuming the screen is 0-10
    elif (player._xCoord + player.direction * moveset[0] <0 or 
          player._xCoord + player.direction * moveset[0] >15):
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

# used to correct position of player if they move offscreen
def correctPos(player):
    if player._xCoord < 0:
        player._xCoord = 0
    elif player._xCoord > 15:
        player._xCoord = 15
    return None

def correctOverlap(p1, p2, knock1, knock2):
    if p1.get_pos() == p2.get_pos():
        # if p2 caused the knockback, move p1 1 xcoord away in p2 direction
        if knock2:
            p1._xCoord += p2._direction
        elif knock1:
            p2._xCoord += p1._direction

#for testing: prints player info
def playerInfo(player, playerName, action):
    print(f"{playerName} POS: {player._xCoord, player._yCoord}, {player._hp}, midair: {player._midair}, blocking: {player._blocking, player._block._shieldHp}, stun: {player._stun}, facing: {player._direction}, airvelo:{player._velocity}")
    print(f"             SPEED: {player._speed}, ATKBUFF: {player._atkbuff}, DURATION: {player._currentBuffDuration}")
    print(f"NEXT ACTION: {action}")