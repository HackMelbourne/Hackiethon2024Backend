from test import validMove
def move(player, enemy, action):
    if (action[0] == "move"):
        if validMove(action[1], player, enemy) and not player.midair:
            player.moves.append(action)
            player.xCoord += player.direction * action[1][0]
            player.yCoord += action[1][1]
            if player.yCoord > 0:
                player.midair = True
        else:    
            print("Invalid movement")

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
    knockback = stun = 0
    
    if (action[0] == "attack"):
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
        knockback = attack[4]
        stun = attack[5]
        
        # This is fine if we only allow horizontal attacks
        if (abs(player.xCoord-target.xCoord) == atk_range and player.yCoord == target.yCoord):
            #check for blocks
            if(target.blocking and blockable):
                #parry if block is frame perfect
                if target.moves[-1] != "block":
                    player.stun = 2
            else:
                target.hp -= damage
    return knockback, stun