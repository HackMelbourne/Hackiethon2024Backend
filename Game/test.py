#checks if a "move" is valid
from Game.gameSettings import GOLEFT, GORIGHT, LEFTBORDER, RIGHTBORDER
def validMove(moveset, player, enemy):
    valid_moves = [-1,0,1]
    #TODO prevent double jumps
    if moveset[0] not in valid_moves or moveset[1] not in valid_moves:
        return False
    # check if out of bound 
    # *assuming the screen is 0-10
    elif (player._xCoord + player._direction * moveset[0] < LEFTBORDER or 
          player._xCoord + player._direction * moveset[0] > RIGHTBORDER):
        if moveset[1]:
            return True
        else:
            return False
    #UPDATE: invalid if next to each other and moving towards the other
    elif (abs(player._xCoord - enemy._xCoord) == moveset[0] and 
          (player._yCoord + moveset[1]) == enemy._yCoord):
        return False
    return True

def correct_orientation(p1, p2):
    #flips orientation if player jumps over each other
    if p1._xCoord > p2._xCoord:
        p1._direction = GOLEFT
        p2._direction = GORIGHT
    else:
        p1._direction = GORIGHT
        p2._direction = GOLEFT      

# used to correct position of player if they move offscreen
def correctPos(player):
    if player._xCoord < LEFTBORDER:
        player._xCoord = LEFTBORDER
    elif player._xCoord > RIGHTBORDER:
        player._xCoord = RIGHTBORDER
    return None

def correctOverlap(p1, p2, knock1, knock2):
    if p1.get_pos() == p2.get_pos():
        print("Overlapping")
        # if p2 caused the knockback, move p1 1 xcoord away in p2 direction
        print(knock2, knock1) 
        if knock2:
            p1._xCoord += p2._direction
        elif knock1:
            p2._xCoord += p1._direction
        else:
            # rare overlap caused by air movement, move both away from each other
            p1._xCoord += p2._direction
            p2._xCoord += p1._direction
        return True
    return False
       
# returns if player collision occured       
def correct_dir_pos(player1, player2, knock1, knock2):
    correctPos(player1)
    correctPos(player2)
    
    correct_orientation(player1, player2)
    return correctOverlap(player1, player2, knock1, knock2)

#for testing: prints player info
def playerInfo(player, playerName, action):
    print(f"{playerName} POS: {player._xCoord, player._yCoord}, {player._hp}, midair: {player._midair}, blocking: {player._blocking, player._block._shieldHp}, stun: {player._stun}, facing: {player._direction}, airvelo:{player._velocity}")
    print(f"             SPEED: {player._speed}, ATKBUFF: {player._atkbuff}, DURATION: {player._currentBuffDuration}")
    print(f"INPUT ACTION: {action}")
    print(f"ACTUAL ACTION: {player._moves[player._moveNum - 1]}")