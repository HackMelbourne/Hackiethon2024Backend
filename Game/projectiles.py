import itertools
from Game.Skills import AttackSkill
from Game.gameSettings import LEFTBORDER, RIGHTBORDER
class Projectile:
    # auto increment projectile id whenever a new projectile is summoned
    id = itertools.count()
    
    def __init__(self, player, path, size, type, trait, collision, timer):
        # size = (x, y) hitbox size of projectile
        # type =  type of projectile eg hadoken
        self._direction = player._direction
        self._initdirection = self._direction
        self._distance = 0
        self._size = list(size)
        self._type = type
        self._timer = timer
        
        # True if projectile damages on hit during travel eg hadoken, lasso
        # False if prpojectile damages after travel eg ice wall, landmine
        self._collision = collision
        
        # trait = effect after projectile has travelled its path
        # pop = remove projectile, explode = AOE dmg after timer, timer = pop after timer, no dmg
        self._trait = trait
        self._id = next(self.id)
        self._player = player
        
        # this is an array of projectile positions relative to cast position over time
        self._path = path
        self._pathIndex = 0
        
        
        for i in range(len(self._path)):
            self._path[i][0] = self._direction * abs(self._path[i][0])
        print(player._direction, self._path)
        
        
            
        self._xCoord = player._xCoord + path[0][0]
        self._yCoord = player._yCoord + path[0][1]

    def _travel(self):
        print(self._pathIndex)
        if 0 < self._pathIndex < len(self._path):
            pos = self._path[self._pathIndex]
            self._xCoord += pos[0] - self._path[self._pathIndex - 1][0]
            self._yCoord += pos[1] - self._path[self._pathIndex - 1][1]
        elif self._pathIndex >= len(self._path):
            # has reached end of path, so do effects based on trait
            self._do_trait()
            
        self._pathIndex += 1
        if ((self._xCoord < LEFTBORDER) or (self._xCoord > RIGHTBORDER)):
            self._size = (0,0)
      
    def _do_trait(self):
        if not self._trait:
            # pop
            self._size = (0, 0)
            
        elif self._trait == "return":
            # dynamically return towards player
            self._direction = -1 * self._initdirection
            if (self._xCoord == self._player._xCoord and 
                self._yCoord == self._player._yCoord):
                # boomerang caught, or player in front of projectile
                self._size = (0,0)
            elif (self._player._xCoord - self._xCoord) * self._direction > 0 :
                # if the player is currently at least behind the projectile 
                # travel towards caster
                self._xCoord += self._direction
                if self._yCoord < self._player._yCoord:
                    self._yCoord += 1
                elif self._yCoord > self._player._yCoord:
                    self._yCoord -= 1
            else:
                self._size = (0,0)
                
        elif self._trait == "timer":
            # stay at current position for given time to live
            # does damage if hits opponent before given time
            self._collision = True
            if self._timer:
                self._timer -= 1
            else:
                self._size = (0,0)
            
            
        elif self._trait == "timer_explode":
            # similar to timer, but does aoe damage after timer
            if self._timer:
                self._timer -= 1
            else:
                # explode
                self._size = (self._size[0] + 1, self._size[1] + 1)
                self._collision = True
                self._trait = "explode"
              
    def get_pos(self):
        return (self._xCoord, self._yCoord)
            
    def _checkCollision(self, target):
        # checks if projectile has a size
        if self._size[0] and self._size[1] and self._collision:
            # checks if projectile hits target
            if ((abs(target._xCoord-self._xCoord) < self._size[0]) and
                (abs(target._yCoord-self._yCoord) < self._size[1])):
                return target != self._player
        return False
            
    def _checkProjCollision(self, target):
        if self._size[0] and self._size[1] and self._collision:
            # this projectiles range = x to x + target size * direction
            # therefore, get max x and max y sizes, check if they hit
            # hits if both positions within the max x and y sizes
            max_x = max(target._size[0], self._size[0])
            max_y = max(target._size[1], self._size[1])
            if ((abs(target._xCoord-self._xCoord) < max_x) and 
                (abs(target._yCoord-self._yCoord) < max_y)):
                return True
        return False
    
class ProjectileSkill(AttackSkill):
    def __init__(self, player, startup, cooldown, damage, blockable, knockback,
                 stun, skillName):
        AttackSkill.__init__(self, startup=startup, cooldown=cooldown, 
                            damage=damage, xRange=0, vertical=0, 
                            blockable=blockable, knockback=knockback, 
                            stun=stun)
        self._player = player
        self._skillType = skillName
        self._recovery = 0
        
    def summonProjectile(self, path, size, trait, collision, timer):
        projectile = Projectile(self._player, path, size, self._skillType, trait, 
                                collision, timer)
        return projectile
    
class Hadoken(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=10,
                                 blockable=True, knockback=2, stun=2, 
                                 skillName="hadoken")
        self._path = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]
        self._stunself = False
    
    def _activateSkill(self):
        atk_info = super()._activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(path = self._path, size=(1,1), 
                                           trait=None, collision=True, timer=0)
        return [self._skillType,  {"damage":self._skillValue, "blockable": self._blockable, 
                "knockback":self._knockback, "stun":self._stun,  "self_stun":self._stunself,
                "projectile": projectile}]
        
    def path_range(self):
        return self._path[-1][0] - self._path[0][0]
    
# TODO while lasso projecile is up, caster cannot move
class Lasso(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=5,
                                 blockable=True, knockback=-2, stun=0, 
                                 skillName="lasso")
        self._path = [[1, 0], [2, 0], [3, 0], [4,0]]
        self._stunself = True
    
    def _activateSkill(self):
        atk_info = super()._activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(path=self._path, size=(1,1), 
                                           trait=None, collision=True, timer=0)
        return [self._skillType,  {"damage":self._skillValue, "blockable": self._blockable, 
                "knockback":self._knockback, "stun":self._stun,  "self_stun":self._stunself,
                "projectile": projectile}]
    
    def path_range(self):
        return self._path[-1][0] - self._path[0][0]
        
class Boomerang(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=5,
                                 blockable=True, knockback=2, stun=2, 
                                 skillName="boomerang")
        self._path = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]
        self._stunself = False
    
    def _activateSkill(self):
        atk_info = super()._activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(path = self._path, size=(1,1), 
                                           trait="return", collision=True, timer=0)
        return [self._skillType,  {"damage":self._skillValue, "blockable": self._blockable, 
                "knockback":self._knockback, "stun":self._stun,  "self_stun":self._stunself,
                "projectile": projectile}]
    
    def path_range(self):
        return self._path[-1][0] - self._path[0][0]
        
class Grenade(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=10,
                                 blockable=False, knockback=3, stun=3, 
                                 skillName="grenade")
        self._path = [[1,1], [2,1], [3,1], [4,1]]
        self._stunself = False
    
    def _activateSkill(self):
        atk_info = super()._activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(path = self._path, size=(1,1), 
                                           trait="timer_explode", 
                                           collision=False, timer=0)
        return [self._skillType,  {"damage":self._skillValue, "blockable": self._blockable, 
                "knockback":self._knockback, "stun":self._stun,  "self_stun":self._stunself,
                "projectile": projectile}]
        
    def path_range(self):
        return self._path[-1][0] - self._path[0][0]
    
class BearTrap(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=10,
                                 blockable=False, knockback=0, stun=3, 
                                 skillName="beartrap")
        self._path = [[1,0], [2,0]]
        self._stunself = False
        
    def _activateSkill(self):
        atk_info = super()._activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(path = self._path, size=(1,1), 
                                           trait="timer", 
                                           collision=False, timer=5)
        return [self._skillType,  {"damage":self._skillValue, "blockable": self._blockable, 
                "knockback":self._knockback, "stun":self._stun,  "self_stun":self._stunself,
                "projectile": projectile}]
        
    def path_range(self):
        return self._path[-1][0] - self._path[0][0]
        
class IceWall(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=30, damage=10,
                                 blockable=False, knockback=2, stun=1, 
                                 skillName="icewall")
        self._path = [[1,0], [2,0], [3,0]]
        self._stunself = False
        
    def _activateSkill(self):
        atk_info = super()._activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(path = self._path, size=(1,3), 
                                           trait="timer", 
                                           collision=True, timer=10)
        return [self._skillType,  {"damage":self._skillValue, "blockable": self._blockable, 
                "knockback":self._knockback, "stun":self._stun,  "self_stun":self._stunself,
                "projectile": projectile}]
    
    def path_range(self):
        return self._path[-1][0] - self._path[0][0]