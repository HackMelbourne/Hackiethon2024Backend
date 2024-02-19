# Skill superclass
class Skill:
    def __init__(self, skillType, startup, cooldown, skillValue):
        #skillType can be either "move", "attack" or "defend" (can add more)
        self._skillType = skillType
        
        #skill is casted once currentStartup decreases to 0
        self._currentStartup = startup
        self._maxStartup = startup
        self._initMaxStartup = startup
        self._startupReducMult = 1
        
        #cooldown after skill is used
        self._maxCooldown = cooldown
        #current skill cooldown
        self._cooldown = 0
        
        #skillValue for "move" is (xcoord, ycoord), "attack" is damage, etc
        self._skillValue = skillValue
        
    # To use with external functions that check and update cooldown
    def _reduceCd(self, reduction):
        if self._cooldown > 0:
            self._cooldown -= reduction
            
    """
    If startup time finished or no startup time, use skill
    Else if have startup time, return -1 to use in while loop to countdown
    startup
    If on cooldown, return current skill cooldown
    """
    def _useSkill(self):
        if self._cooldown <= 0:
            if self._currentStartup == 0:
                self._currentStartup = self._maxStartup
                self._cooldown = self._maxCooldown
                return self._skillType, self._skillValue
            else:
                self._currentStartup -= 1
                return -1
        else:
            return self._cooldown
    
    # resets startup
    def _resetStartup(self):
        self._currentStartup = self._maxStartup
    
    def _reduceMaxStartup(self, reductionMult):
        if reductionMult == 0:
            self._resetMaxStartup()
        else:
            if reductionMult < 1 and self._maxStartup == 0:
                self._maxStartup = 1
            else:
                self._maxStartup = int(self._maxStartup / reductionMult)
                self._startupReducMult = reductionMult
            self._currentStartup = self._maxStartup
        print(f"New: {self._currentStartup, self._maxStartup}")
            
    def _resetMaxStartup(self):
        self._maxStartup = self._initMaxStartup
        self._currentStartup = self._maxStartup
    
    # public methods
    def get_skillname(self):
        return self._skillType
    
    def on_cooldown(self):
        return self._cooldown != 0
       
# when moving, use activateSkill to specify direction   
class MoveSkill(Skill):
    def __init__(self, startup, cooldown, distance):
        super().__init__("move", startup, cooldown, distance)

    def _activateSkill(self, direction):
        self._skillValue = direction
        return self._useSkill()
        
class AttackSkill(Skill):
    def __init__(self, startup, cooldown, damage, xRange, vertical, blockable, knockback, stun):
        super().__init__("attack", startup, cooldown, damage)
        # xRange : horizontal reach, vertical : 0 can only hit if same yCoord,
        # vertical > 0 can hit same yCoord and above, vertical < 0 can hit below
        self._xRange = xRange
        self._vertical = vertical
        self._blockable = blockable
        self._knockback = knockback
        self._stun = stun
        self._initDamage = self._skillValue
        
    def _activateSkill(self):
        if self._cooldown > 0:
            return self._cooldown
        else:
            # returns "attack", damage, xRange, vertical, block, knockback, stun
            skill = self._useSkill()
            if isinstance(skill, int):
                return -1
            return skill + (self._xRange, self._vertical,
                            self._blockable, self._knockback, self._stun)
    def _damageBuff(self, buffVal):
        self._skillValue = int(self._skillValue * buffVal)
        if self._skillValue == 0:
            self._skillValue = self._initDamage
        
class BlockSkill(Skill):
    def __init__(self, startup, cooldown, shieldHp, stunOnBreak):
        super().__init__("block", startup, cooldown, shieldHp)
        self._stunOnBreak = stunOnBreak
        self._shieldHp = self._skillValue
        self._maxShieldHp = shieldHp
        
    #regens shield hp to max
    def _regenShield(self):
        if self._shieldHp < self._maxShieldHp:
            self._shieldHp = self._maxShieldHp
            
    #block takes damage, returns self stun amount if shield break
    def _shieldDmg(self, damage):
        self._shieldHp -= damage
        if self._shieldHp <= 0:
            self._shieldHp = self._maxShieldHp
            return self._stunOnBreak
        return 0
    
    def _activateSkill(self):
        return self._useSkill()

class DashAttackSkill(AttackSkill):
    def __init__(self, player=None):
        super().__init__(startup=0, cooldown=10, damage=10, xRange=4, 
                         vertical=0, blockable=False, knockback=0, stun=2)
        self._skillType = "dash_attack"

class UppercutSkill(AttackSkill):
    def __init__(self, player=None):
        super().__init__(startup=0, cooldown=10, damage=15, xRange = 1, 
                         vertical=2, blockable=True, knockback=2, stun=2)
        self._skillType = "uppercut"

#TODO add one_punch, super saiyan and meditate/heal playeractions
#TODO add buff duration timer 

class OnePunchSkill(AttackSkill):
    def __init__(self, player=None):
        super().__init__(startup=0, cooldown=10, damage=20, xRange=2,
                         vertical=0, blockable=False, knockback=4, stun=3)
        self._skillType = "onepunch"

# returns ("buff", (speedBuff, attackBuff, defenseBuff))
class BuffSkill(Skill):
    def __init__(self, startup, cooldown, speedBuff, attackBuff, duration):
        super().__init__("buff", startup, cooldown, (speedBuff, attackBuff, duration))

    def _activateSkill(self):
        return self._useSkill()
    
class Meditate(Skill):
    def __init__(self, player=None):
        super().__init__(skillType="meditate", startup=0, cooldown=20, skillValue=10)
    
    def _activateSkill(self):
        return self._useSkill()

class TeleportSkill(Skill):
    def __init__(self, player=None):
        super().__init__(skillType= "teleport", startup= 0, cooldown= 10, skillValue= 5)

    def _activateSkill(self):
        return self._useSkill()

# returns ("super_saiyan", (speedBuff, attackBuff, defenseBuff))
class SuperSaiyanSkill(BuffSkill):
    def __init__(self, player=None):
        super().__init__(startup=0, cooldown=15, speedBuff=2, attackBuff=2, 
                         duration=1)
        self._skillType = "super_saiyan"
