import test
import importlib
from playerActions import defense_actions, attack_actions, projectile_actions
from Skills import *
from projectiles import *
import json
import os
from turnUpdates import *
#game settings
timeLimit = 6
movesPerSecond = 1

#direction constants
GORIGHT = 1
GOLEFT = -1

#player variables

def setupGame():
    
    p1Import = importlib.import_module("Submissions.PlayerConfigs")
    p2Import = importlib.import_module("Submissions.PlayerConfigs")
    player1 = p1Import.Player_Controller(13,0,50,GORIGHT, OnePunchSkill, UppercutSkill, 1)
    player2 = p2Import.Player_Controller(17,0,50,GOLEFT, Lasso, UppercutSkill, 2)
    return player1,player2

#------------------Adding to player1 and player2 move scripts for test----
def setMoves(player1, player2):    
    p1movelist = ("light", ), ("heavy", ), ("onepunch",)
    p2movelist = None,
    
    player1._inputs += p1movelist
    player2._inputs += p2movelist          

def performActions(player1, player2, act1, act2, stun1, stun2, projectiles):
    knock1 = knock2 = 0

    if player1._stun:
        player1._stun -= 1
    if player2._stun:
        player2._stun -= 1

        
    # all actions have the signature
    # function(player1, player2, act1)
    # and return (knock1, stun1)

    # to specify an action,
    # define an action inside playerActions with the signature above,
    # and then add it to attack_actions or defense_actions (inside playerActions)

    # works under assumption of only 1 action per turn
        
    # movement and defensive actions take priority then attacks and skills 
    if act1 in ("NoMove", ("NoMove", None), None):
        player1._moves.append(("NoMove", None))
    if act2 in ("NoMove", ("NoMove", None), None):
        player2._moves.append(("NoMove", None))
        
    if (act1 and act1[0] in defense_actions and not player1._stun):
        defense_actions[act1[0]](player1, player2, act1)
    if (act2 and act2[0] in defense_actions and not player2._stun):
        defense_actions[act2[0]](player2, player1, act2)

    if act1 and not player1._stun and act1[0] in attack_actions:
        knock1, stun1 = attack_actions[act1[0]](player1, player2, act1)
    if act2 and not player2._stun and act2[0] in attack_actions:
        knock2, stun2 = attack_actions[act2[0]](player2, player1, act2)
        
    if act1 and not player1._stun and act1[0] in projectile_actions:
        projectiles.append(projectile_actions[act1[0]](player1, player2, act1))
    if act2 and not player2._stun and act2[0] in projectile_actions:
        projectiles.append(projectile_actions[act2[0]](player2, player1, act2))
        
    player1._moveNum += 1
    player2._moveNum += 1
    
    return knock1, stun1, knock2, stun2
                                        
def startGame(path1, path2):
    if not isinstance(path1, str) and isinstance(path2,str):
        return path2
    if isinstance(path1, str) and not isinstance(path2,str):
        return path1
    if not isinstance(path1, str) and not isinstance(path2,str):
        return None
    player1, player2 = setupGame()

    stun1 = stun2 = 0

    setMoves(player1, player2)

    #TODO dont hard code path use the player names and use os for current path
    # * Check if file exists if so delete it 
    if(os.path.isfile("jsonfiles\p1.json")):
        os.remove("jsonfiles\p1.json")
    if(os.path.isfile("jsonfiles\p2.json")):
        os.remove("jsonfiles\p2.json")
        
    player1_json = open("jsonfiles\p1.json", "a")
    player2_json = open("jsonfiles\p2.json", "a")
    # structure the dict
    p1_json_dict = {
        'hp': [],
        'xCoord': [],
        'yCoord': [],
        'state': [],
        'stun': [],
        'midair': [],
        'falling':[],
        'ProjectileType': None,
        'projXCoord':[],
        'projYCoord':[]
        }
    p2_json_dict = {
        'hp': [],
        'xCoord': [],
        'yCoord': [],
        'state': [],
        'stun': [],
        'midair': [],
        'falling':[],
        'ProjectileType': None,
        'projXCoord':[],
        'projYCoord':[]
    }
    projectiles = []
  
    for tick in range(timeLimit *movesPerSecond):
        #flips orientation if player jumps over each other
        if test.flip_orientation(player1, player2):
            player1.direction = GOLEFT
            player2.direction = GORIGHT
        else:
            player1.direction = GORIGHT
            player2.direction = GOLEFT
        
        knock1 = knock2 = 0
        
        act1 = player1._action()
        act2 = player2._action()
        
        test.playerInfo(player1, path1, act1)
        test.playerInfo(player2, path2, act2)
        
        knock1, stun1, knock2, stun2 = performActions(player1, player2, 
                                                      act1, act2, stun1, stun2, 
                                                      projectiles)
        # if there are projectiles, make them travel
        projectiles, knock1, stun1, knock2, stun2 = projectile_move(projectiles, 
                                knock1, stun1, knock2, stun2, player1, player2,
                                p1_json_dict, p2_json_dict)
        
        #only determine knockback and stun after attacks hit
        #knock1 and stun1 = knockback and stun inflicted by player1
        if knock1:
            player2._xCoord += knock1
            player2._stun += stun1
        if knock2:
            player1._xCoord += knock2
            player1._stun += stun2
            
        #if midair, start falling/rising
        updateMidair(player1)
        updateMidair(player2)

        # correct player positions if off screen/under ground
        test.correctPos(player1)
        test.correctPos(player2)
        
        test.correctOverlap(player1, player2, knock1, knock2)
            
        updateCooldown(player1)
        updateCooldown(player2)
        
        playerToJson(player1, p1_json_dict)
        playerToJson(player2,p2_json_dict)

    json.dump(p1_json_dict, player1_json)
    json.dump(p2_json_dict, player2_json)
    
    player1_json.close()
    player2_json.close()

    print(p1_json_dict)
    print(p2_json_dict)
    
    if player1._hp > player2._hp:
        print('match won by: ', path1)
        return path1
    elif player1._hp < player2._hp:
        print('match won by: ', path2)
        return path2
    else:
        print('Tie!')
        return None

if __name__ == "__main__":
    startGame("PLAYER 1", "PLAYER 2")
