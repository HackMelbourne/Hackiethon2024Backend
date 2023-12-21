# Skill superclass
class Skill:
    def __init__(self, skillType, startup, cooldown, skillValue):
        #skillType can be either "move", "attack" or "defend" (can add more)
        self.skillType = skillType
        
        self.startup = startup
        #skill is casted once currentStartup decreases to 0
        self.currentStartup = startup
        
        #cooldown after skill is used
        self.maxCooldown = cooldown
        #current skill cooldown
        self.cooldown = 0
        
        #skillValue for "move" is (xcoord, ycoord), "attack" is damage, etc
        self.skillValue = skillValue
        
    # To use with external functions that check and update cooldown
    def reduceCd(self, reduction):
        if self.cooldown > 0:
            self.cooldown -= reduction
            
    """
    If startup time finished or no startup time, use skill
    Else if have startup time, return -1 to use in while loop to countdown
    startup
    If on cooldown, return current skill cooldown
    """
    def useSkill(self):
        if self.cooldown <= 0:
            if self.currentStartup == 0:
                self.currentStartup = self.startup
                self.cooldown = self.maxCooldown
                return self.skillType, self.skillValue
            else:
                self.currentStartup -= 1
                return -1
        else:
            return self.cooldown
    
    # Allows skill cancelling if skill is still in startup time
    def skillCancel(self):
        if self.currentStartup < self.startup:
            self.currentStartup = self.startup
       
# Below are example/sample skills 
    
class MoveSkill(Skill):
    def __init__(self, startup, cooldown, distance):
        super().__init__("move", startup, cooldown, distance)

    def activateSkill(self):
        return self.useSkill()
        
class AttackSkill(Skill):
    def __init__(self, startup, cooldown, damage, xRange, vertical, blockable, knockback, stun):
        super().__init__("attack", startup, cooldown, damage)
        # xRange : horizontal reach, vertical : 0 can only hit if same yCoord,
        # vertical > 0 can hit same yCoord and above, vertical < 0 can hit below
        self.xRange = xRange
        self.vertical = vertical
        self.blockable = blockable
        self.knockback = knockback
        self.stun = stun
        
    def activateSkill(self):
        if self.cooldown > 0:
            return self.cooldown
        else:
            # returns "attack", damage, xRange, vertical, block, knockback, stun
            skill = self.useSkill()
            if isinstance(skill, int):
                return -1
            return skill + (self.xRange, self.vertical,
                            self.blockable, self.knockback, self.stun)
        
class BlockSkill(Skill):
    def __init__(self, startup, cooldown, shieldHp, stunOnBreak):
        super().__init__("block", startup, cooldown, shieldHp)
        self.stunOnBreak = stunOnBreak
        self.shieldHp = self.skillValue
        self.maxShieldHp = shieldHp
        
    #regens shield hp to max
    def regenShield(self):
        if self.shieldHp < self.maxShieldHp:
            self.shieldHp = self.maxShieldHp
            
    #block takes damage, returns self stun amount if shield break
    def shieldDmg(self, damage):
        self.shieldHp -= damage
        if self.shieldHp <= 0:
            self.shieldHp = self.maxShieldHp
            return self.stunOnBreak
        return 0
    
    def activateSkill(self):
        return self.useSkill()

class DashAttackSkill(AttackSkill):
    def __init__(self):
        super().__init__(startup=0, cooldown=10, damage=10, xRange=4, 
                         vertical=0, blockable=False, knockback=0, stun=2)
        self.skillType = "dash_attack"


class UppercutSkill(AttackSkill):
    def __init__(self):
        super().__init__(startup=0, cooldown=10, damage=15, xRange = 1, 
                         vertical=2, blockable=True, knockback=2, stun=3)
        self.skillType = "uppercut"