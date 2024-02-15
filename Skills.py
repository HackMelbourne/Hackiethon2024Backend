# Skill superclass
class Skill:
    def __init__(self, skillType, startup, cooldown, skillValue):
        #skillType can be either "move", "attack" or "defend" (can add more)
        self.skillType = skillType
        
        #skill is casted once currentStartup decreases to 0
        self.currentStartup = startup
        self.maxStartup = startup
        self.initMaxStartup = startup
        self.startupReducMult = 1
        
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
                self.currentStartup = self.maxStartup
                self.cooldown = self.maxCooldown
                return self.skillType, self.skillValue
            else:
                self.currentStartup -= 1
                return -1
        else:
            return self.cooldown
    
    # resets startup
    def resetStartup(self):
        self.currentStartup = self.maxStartup
    
    def reduceMaxStartup(self, reductionMult):
        if reductionMult == 0:
            self.resetMaxStartup()
        else:
            if reductionMult < 1 and self.maxStartup == 0:
                self.maxStartup = 1
            else:
                self.maxStartup = int(self.maxStartup / reductionMult)
                self.startupReducMult = reductionMult
            self.currentStartup = self.maxStartup
        print(f"New: {self.currentStartup, self.maxStartup}")
            
    def resetMaxStartup(self):
        self.maxStartup = self.initMaxStartup
        self.currentStartup = self.maxStartup
    
   
    def get_skillname(self):
        return self.skillType
       
# when moving, use activateSkill to specify direction   
class MoveSkill(Skill):
    def __init__(self, startup, cooldown, distance):
        super().__init__("move", startup, cooldown, distance)

    def activateSkill(self, direction):
        self.skillValue = direction
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
        self.initDamage = self.skillValue
        
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
    def damageBuff(self, buffVal):
        self.skillValue = int(self.skillValue * buffVal)
        if self.skillValue == 0:
            self.skillValue = self.initDamage
        
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
    def __init__(self, player=None):
        super().__init__(startup=0, cooldown=10, damage=10, xRange=4, 
                         vertical=0, blockable=False, knockback=0, stun=2)
        self.skillType = "dash_attack"

class UppercutSkill(AttackSkill):
    def __init__(self, player=None):
        super().__init__(startup=0, cooldown=10, damage=15, xRange = 1, 
                         vertical=2, blockable=True, knockback=2, stun=3)
        self.skillType = "uppercut"

#TODO add one_punch, super saiyan and meditate/heal playeractions
#TODO add buff duration timer 

class OnePunchSkill(AttackSkill):
    def __init__(self, player=None):
        super().__init__(startup=0, cooldown=10, damage=20, xRange=2,
                         vertical=0, blockable=False, knockback=4, stun=3)
        self.skillType = "onepunch"

# returns ("buff", (speedBuff, attackBuff, defenseBuff))
class BuffSkill(Skill):
    def __init__(self, startup, cooldown, speedBuff, attackBuff, duration):
        super().__init__("buff", startup, cooldown, (speedBuff, attackBuff, duration))

    def activateSkill(self):
        return self.useSkill()
    
class Meditate(Skill):
    def __init__(self, player=None):
        super().__init__(skillType="meditate", startup=0, cooldown=20, skillValue=10)
    
    def activateSkill(self):
        return self.useSkill()

class TeleportSkill(Skill):
    def __init__(self, player=None):
        super().__init__(skillType= "teleport", startup= 0, cooldown= 10, skillValue= 5)

    def activateSkill(self):
        return self.useSkill()

# returns ("super_saiyan", (speedBuff, attackBuff, defenseBuff))
class SuperSaiyanSkill(BuffSkill):
    def __init__(self, player=None):
        super().__init__(startup=0, cooldown=15, speedBuff=2, attackBuff=2, 
                         duration=1)
        self.skillType = "super_saiyan"
