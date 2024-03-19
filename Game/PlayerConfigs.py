from Game.Skills import *
# use as a template for player1 and player2
class Player_Controller:
    def __init__(self, xCoord, yCoord, HP, direction, primary, secondary, id):
        self._entityType = "player"
        self._primarySkill = primary(self)
        self._secondarySkill = secondary(self)
        self._lightAtk = AttackSkill(0, 1, 2, 1, 0, True, 0, 0)
        self._heavyAtk = AttackSkill(0, 3, 4, 1, 0, True, 1, 1, recovery=1)
        self._block = BlockSkill(0, 0, 10, 2)
        self._move = MoveSkill(0, 0, (0,0))
        self._id = id
        
        self._xCoord = xCoord
        self._yCoord = yCoord

        #current stun duration
        self._stun = 0
        self._recovery = 0
        self._midStartup = False
        self._blocking = False
        self._hp = HP
        self._defense = 1
        self._superarmor = False
        #midair attributes
        self._midair = False
        self._defaultJumpHeight = 1
        self._jumpHeight = self._defaultJumpHeight
        self._falling = False
        self._velocity = 0
        self._airvelo = 0
        
        #direction player is facing
        self._direction = direction
        
        # actual moves taken
        self._moves = []
        self._moveNum = 0
        self._skill_state = False
        
        # moves input by player
        self._inputs = []
        
        # buffs
        self._speed = 1
        self._atkbuff = 0
        self._currentBuffDuration = 0
        self._encumberedDuration = 0
        self._encumbered = False
        
    def _action(self):
        if self._moveNum < len(self._inputs) and self._inputs[self._moveNum]:
            return self._inputs[self._moveNum]
        else:   
            return ("NoMove")
           
    def get_pos(self):
        '''Returns player position -> (x, y) as (int, int)'''
        return (self._xCoord, self._yCoord)
    
    def get_hp(self):
        '''Return player HP as int'''
        return self._hp
    
    def get_stun(self):
        '''Return player's current stun duration as int, 0 means not stunned'''
        return self._stun
    
    def get_block(self):
        '''Returns player current block value: shield strength if blocking, 0 if not'''
        if self._blocking:
            return self._block._shieldHp
        return 0
    
    def get_last_move(self):
        '''Returns player's most recent move -> (move, moveValue)
           as (string, any type)
        '''
        if len(self._moves) > 0:
            return self._moves[-1]
        return None
    
    def primary_on_cd(self, get_timer):
        if get_timer:
            return self._primarySkill.get_cooldown()
        else:
            return self._primarySkill.on_cooldown()
        
    
    def secondary_on_cd(self, get_timer):
        if get_timer:
            return self._primarySkill.get_cooldown()
        else: 
            return self._secondarySkill.on_cooldown()
    
    def heavy_on_cd(self):
        return self._heavyAtk.on_cooldown()
    
    def primary_range(self):
        try:
            return self._primarySkill._xRange
        except:
            return 0
    
    # todo make this work with projectile range   
    def secondary_range(self):
        try:
            second_range = self._secondarySkill._xRange
            if second_range == 0:
                # this is a projectile
                return self._secondarySkill.path_range()
        except:
            return 0
        
    def get_past_move(self, turns):
        if turns <= len(self._moves):
            return (self._moves[-turns])
        else:
            return None
        
    def get_recovery(self):
        return self._recovery
    
    def skill_cancellable(self):
        return (self._skill_state or self._midStartup)
    
    def get_primary_name(self):
        return self._primarySkill._skillType
    
    def get_secondary_name(self):
        return self._secondarySkill._skillType
    
    def get_landed(self):
        return self._move._cooldown > 0