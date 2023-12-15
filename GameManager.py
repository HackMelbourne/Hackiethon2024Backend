# Game manager
import random
import Player1
import Player2
from test import *
#game settings
timeLimit = 60
movesPerSecond =2

#move how many unit per tick
gravity = 2

#player variables


player1 = Player1.Player_Controller(1,0,50)
player2 = Player1.Player_Controller(4,0,50)

<<<<<<< Updated upstream

def move(player, action):
    if (action[0] == "move"):
        if validMove(action[1]):
            player.moves.append(action)
            player.xCoord += action[1][0]
            player.yCoord += action[1][1]
=======
#------------------Adding to player1 and player2 move scripts for test----
def setMoves(player1, player2):    
    p1movelist = ("move", (1,0)), ("attack", "light"), ("attack", "light"), ("attack", "light"),("attack", "light")
    p2movelist = ("block",), ("block",), ("block",), ("block",), ("block",)
    
    player1.moveList += p1movelist
    player2.moveList += p2movelist            

def updateCooldown(player):
    #TODO : once primary and secondary skills complete, add reduceCd
    
    player.lightAtk.reduceCd(1)
    player.heavyAtk.reduceCd(1)
    pass

# updates current position of player if they are midair or started jumping
def updateMidair(player):
    if player.yCoord == player.jumpHeight:
        player.falling = True
        player.yCoord -= gravity
    # not yet at apex of jump
    elif player.midair:
        if player.falling: 
            player.yCoord -= gravity
        else:
            player.yCoord += 1
    if player.yCoord == 0: 
        player.midair = player.falling = False

#im not sure how to make this any more efficient
def performActions(player1, player2, act1, act2, stun1, stun2):
    knock1 = knock2 = 0

    if player1.stun:
        player1.stun -= 1
    else:
        player1.moveNum += 1
    if player2.stun:
        player2.stun -= 1
    else:
        player2.moveNum += 1
        
    # if not player1.stun:
    #     move(player1, player2, act1)
    # if not player2.stun:
    #     move(player2, player1, act2)
    # if not player1.stun:
    #     block(player1, act1)
    # if not player2.stun:
    #     block(player2, act2)
    # if not player1.stun:
    #     knock1, stun1 = attack(player1, player2, act1)
    # if not player2.stun:
    #     knock2, stun2 = attack(player2, player1, act2)

    # all actions have the signature
    # function(player1, player2, act1)
    # and return (knock1, stun1)

    # to specify an action,
    # define an action inside playerActions with the signature above,
    # and then add it to valid_actions (inside playerActions)

    # works under assumption of only 1 action per turn

    # for debug
    # if (act1 != "NoMove"):
    # print(act1, act2)
    
    # movement and defensive actions take priority
    if (act1[0] in ("move", "block") and not player1.stun):
        valid_actions[act1[0]](player1, player2, act1)
    if (act2[0] in ("move", "block") and not player2.stun):
        valid_actions[act2[0]](player2, player1, act2)

    # then attacks and skills take second priority
    if not player1.stun and not act1 == "NoMove":
        knock1, stun1 = valid_actions[act1[0]](player1, player2, act1)
    if not player2.stun and not act2 == "NoMove":
        knock2, stun2 = valid_actions[act2[0]](player2, player1, act2)

    return knock1, stun1, knock2, stun2
                
def startGame(path1, path2):
    print(path1,path2)
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    player1, player2 = setupGame(path1,path2)

    stun1 = stun2 = 0

    #TODO uncomment 
    # setMoves(player1, player2)
    
    for tick in range(timeLimit *movesPerSecond):
        # print(f"\nTURN {tick}\n")
        # print(f"P1 : {player1.xCoord, player1.yCoord}")
        # print(f"P2 : {player2.xCoord, player2.yCoord}")

        #flips orientation if player jumps over each other
        if flip_orientation(player1, player2):
            player1.direction = GOLEFT
            player2.direction = GORIGHT
>>>>>>> Stashed changes
        else:
            Exception

def block(player, action):
    if (action[0] == "block"):
        player.moves.append(action)
        if player.blocking:
            player.blocking =True

def attack(player,target, action):
    if (action[0] == "attack"):
        player.moves.append(action)
        #TODO attack variations such as heavy and light
        # check if attack lands
        if (abs(player.xCoord-target.xCoord) == 1 and player.yCoord == target.yCoord):
            #check for blocks
            if(target.blocking):
                #parry if block is frame perfect
                if target.moves[-2] != "block":
                    player.stun = 2
            else:
                target.hp -=5


def startGame():
    for tick in range(5):
        act1 = player1.action()
        act2 = player2.action()

        move(player1, act1)
        move(player2, act2)

        block(player1, act1)
        block(player2, act2)

        attack(player1, player2, act1)
        attack(player2, player1, act2)
            



