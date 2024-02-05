# Skill superclass
import itertools
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
        self.skillValue += buffVal
        if self.skillValue < 0:
            self.skillValue = 0
        
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
        super().__init__(startup=2, cooldown=10, damage=20, xRange=2,
                         vertical=0, blockable=False, knockback=4, stun=3)
        self.skillType = "one_punch"

# returns ("buff", (speedBuff, attackBuff, defenseBuff))
class BuffSkill(Skill):
    def __init__(self, startup, cooldown, speedBuff, attackBuff, defenseBuff):
        super.__init__(self, "buff", startup, cooldown, (speedBuff, attackBuff, defenseBuff))

    def activateSkill(self):
        return self.useSkill()
    
class HealSkill(Skill):
    def __init__(self, player=None):
        super.__init__(self, skillType="heal", startup=0, cooldown=20, skillValue=10)
    
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
                         defenseBuff=0)
        self.skillType = "super_saiyan"

class Projectile:
    #TODO change max distance to timer/time to live
    # auto increment projectile id whenever a new projectile is summoned
    id = itertools.count()
    
    def __init__(self, player, position, gravity, velocity, acceleration, 
                 range, size, type, proj_return):
        # position = (int, int), contains position of projectile relative to player
        # direction = (int, int), direction of travel in (x, y) grid
        # velocity = how fast the projectile moves horizontally
        # gravity = how fast the projectile moves vertically
        # size = (x, y) hitbox size of projectile
        # type =  type of projectile eg hadoken
        # proj_return = whether or not the projectile comes back to player
        self.xCoord = player._xCoord + position[0]
        self.yCoord = player._yCoord + position[1]
        self.gravity = gravity
        self._direction = player._direction
        self.velocity = velocity * self._direction
        self.initVelocity = velocity
        self.acceleration = acceleration
        self.distance = 0
        self.range = range
        self.size = size
        self.type = type
        self.proj_return = proj_return
        self.id = next(self.id)


    def travel(self):
        if self.distance < self.range :
            self.xCoord += self.velocity
            self.yCoord -= self.gravity
            self.distance += self.velocity
            self.velocity *= (1 + self.acceleration)
        elif self.proj_return:
            # for returning projectiles, check if reach the max range
            # if reached, flip horizontal direction and start moving back
            self.direction *= -1
            self.velocity = self.initVelocity * self._direction
            self.xCoord += self.velocity
            self.yCoord -= self.gravity
            self.distance += self.velocity
            self.velocity *= (1 + self.acceleration)
        # check if off-screen or below ground or moves out of range
        if ((self.yCoord < 0) or (self.xCoord < 0) or (self.xCoord > 30) or 
            (self.distance >= self.range) or (self.distance <= 0)):
            self.size = (0,0)
            
    def get_pos(self):
        return (self.xCoord, self.yCoord)
            

    def checkCollision(self, target):
        # checks if projectile has a size
        if self.size[0] and self.size[1]:
            # checks if projectile hits target
            if (abs(target._xCoord-self.xCoord) < self.size[0] and
                abs(target._yCoord-self.yCoord) <= self.size[1]):
                return True
        return False
            
    def checkProjCollision(self, target):
        if self.size[0] and self.size[1]:
            if (abs(target.xCoord + target.size[0]*target._direction 
                    - self.xCoord) <= self.size[0] and
                abs(target.yCoord + target.size[1] - self.yCoord) 
                <= self.size[1]):
                return True
        return False
    
    
class ProjectileSkill(AttackSkill):
    def __init__(self, player, startup, cooldown, damage, blockable, knockback,
                 stun, skillName):
        AttackSkill.__init__(self, startup=startup, cooldown=cooldown, 
                            damage=damage, xRange=0, vertical=0, 
                            blockable=blockable, knockback=knockback, 
                            stun=stun)
        self.player = player
        self.skillType = skillName
        
    def summonProjectile(self, position, gravity, velocity, accel, range, size, 
                         proj_return):
        projectile = Projectile(self.player, position, gravity, velocity, accel, 
                                range, size, self.skillType, proj_return)
        return projectile
    

class Hadoken(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=10,
                                 blockable=True, knockback=2, stun=2, 
                                 skillName="hadoken")
        
    
    def activateSkill(self):
        atk_info = super().activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(position=(1, 0), gravity=0, velocity=1,
                                           accel=0, range=20, size=(1,1), 
                                           proj_return=False)
        return [self.skillType,  {"damage":self.skillValue, "blockable": self.blockable, 
                "knockback":self.knockback, "stun":self.stun, 
                "projectile": projectile}]
    
    
class Lasso(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=5,
                                 blockable=True, knockback=-2, stun=0, 
                                 skillName="lasso")
        
    
    def activateSkill(self):
        atk_info = super().activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(position=(1, 0), gravity=0, velocity=1,
                                           accel=0, range=5, size=(1,1), 
                                           proj_return=False)
        return [self.skillType,  {"damage":self.skillValue, "blockable": self.blockable, 
                "knockback":self.knockback, "stun":self.stun, 
                "projectile": projectile}]