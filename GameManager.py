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


def move(player, action):
    if (action[0] == "move"):
        if validMove(action[1]):
            player.moves.append(action)
            player.xCoord += action[1][0]
            player.yCoord += action[1][1]
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
            



