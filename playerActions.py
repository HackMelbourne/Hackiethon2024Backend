from test import validMove
def move(player, enemy, action):
    if (action[0] == "move"):
        if validMove(action[1], player, enemy) and not player.midair:
            player.blocking = False
            player.block.regenShield()
            player.moves.append(action)
            player.xCoord += player.direction * action[1][0]
            player.yCoord += action[1][1]
            if player.yCoord > 0:
                player.midair = True
        else:    
            print("Invalid movement")

def block(player, action):
    if (isinstance(action, str) and action == "block"):
        player.moves.append(action)
        player.blocking = True

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
        player.blocking = False
        player.block.regenShield()

        # 2 types of attack, light and heavy
        # action should be like ("attack", "light/heavy")
        attack = fetchAttack(player, action[1])
        
        # no action if attack is on cooldown or previous attack is still in startup
        if isinstance(attack, int):
            return
        
        player.moves.append(action)

        # fetch attack data
        damage = attack[1]
        atk_range = attack[2]
        blockable = attack[3]
        knockback = attack[4]
        stun = attack[5]
        
        # This is fine if we only allow horizontal attacks
        if (abs(player.xCoord-target.xCoord) == atk_range and player.yCoord == target.yCoord):
            # can be changed later : no knockback if block or stunned
            if target.blocking or target.stun:
                knockback = 0
            # if target is blocking
            if(target.blocking and blockable):
                #parry if block is frame perfect: the target blocks as attack comes out
                if target.moves[-1] == "block" and target.moves[-2] != "block":
                    player.stun = 2
                elif target.blocking:
                    target.stun += target.block.shieldDmg(damage)
            else:
                target.hp -= damage
    return knockback, stun