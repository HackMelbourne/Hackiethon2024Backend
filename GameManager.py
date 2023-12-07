import random
from test import *
import importlib

#game settings
timeLimit = 60
movesPerSecond =2

#move how many unit per tick
gravity = 2

#direction constants

GORIGHT = 1
GOLEFT = -1

#player variables

def setupGame(path1, path2):
    
    p1Import = importlib.import_module("Submissions." + path1)
    p2Import = importlib.import_module("Submissions." + path2)
    player1 = p1Import.Player_Controller(1,0,50,GORIGHT)
    player2 = p2Import.Player_Controller(4,0,50,GOLEFT)
    return player1,player2



def move(player, enemy, action):
    if (action[0] == "move"):
        if validMove(action[1], player, enemy) and not player.midair:
            player.moves.append(action)
            player.xCoord += player.direction * action[1][0]
            player.yCoord += action[1][1]
            if player.yCoord > 0:
                player.midair = True
        elif player.midair:
            player.yCoord -= 1
            if player.yCoord == 0:
                player.midair = False
        else:    
            raise Exception("Invalid movement direction")

def block(player, action):
    if (action[0] == "block"):
        player.moves.append(action)
        if player.blocking:
            player.blocking =True

#returns the action if not on cooldown or mid-startup.
# if on cd, return current cd, or -1 if mid startup
def fetchAttack(player, attackType):
    if attackType == "light":
        return player.lightAtk.activateSkill()
    elif attackType == "heavy":
        return player.heavyAtk.activateSkill()
    else:
        raise Exception("Invalid attack type!")


def attack(player,target, action):
    if (action[0] == "attack"):

        #TODO attack variations such as heavy and light
        # 2 types of attack, light and heavy
        # action should be like ("attack", "light/heavy")
        attack = fetchAttack(player, action[1])
        
        # no action if attack is on cooldown or previous attack is still in startup
        if isinstance(attack, int):
            return
        
        player.moves.append(action)

        # check if attack lands
        damage = attack[1]
        atk_range = attack[2]
        blockable = attack[3]
        
        # This is fine if we only allow horizontal attacks
        if (abs(player.xCoord-target.xCoord) == atk_range and player.yCoord == target.yCoord):
            #check for blocks
            if(target.blocking and blockable):
                #parry if block is frame perfect
                if target.moves[-1] != "block":
                    player.stun = 2
            else:
                target.hp -= damage
                

def updateCooldown(player):
    #TODO : once primary and secondary skills complete, add reduceCd
    
    player.lightAtk.reduceCd(1)
    player.heavyAtk.reduceCd(1)
                

def startGame(path1, path2):
    print(path1,path2)
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    player1, player2 = setupGame(path1,path2)


    for tick in range(timeLimit *movesPerSecond):
        
        # print(f"P1 : {player1.xCoord, player1.yCoord}")
        # print(f"P2 : {player2.xCoord, player2.yCoord}")

        #flips orientation if player jumps over each other
        if flip_orientation(player1, player2):
            player1.direction = GOLEFT
            player2.direction = GORIGHT
        else:
            player1.direction = GORIGHT
            player2.direction = GOLEFT
            
        act1 = player1.action()
        act2 = player2.action()
        
        if not player1.stun:
            move(player1, player2, act1)
            block(player1, act1)
            attack(player1, player2, act1)
            player1.moveNum += 1
        else:
            player1.stun -= 1
            
        if not player2.stun:
            move(player2, player1, act2)
            block(player2, act2)
            attack(player2, player1, act2)
            player2.moveNum += 1
        else:
            player2.stun -= 1

        updateCooldown(player1)
        updateCooldown(player2)
        #TODO update current startup every tick

    if player1.hp == player2.hp:
        print('match won by: ', path1)
        return path1
    return max(player1.hp, player2.hp)
