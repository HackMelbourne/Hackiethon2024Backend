from Skills import *
# use as a template for player1 and player2
class Player_Controller:
    def __init__(self, xCoord, yCoord, HP, direction, primary, secondary, id):
        self._primarySkill = primary(self)
        self._secondarySkill = secondary(self)
        self._lightAtk = AttackSkill(0, 1, 5, 1, 0, True, 1, 0)
        self._heavyAtk = AttackSkill(0, 4, 10, 2, 0, True, 2, 1)
        self._block = BlockSkill(0, 0, 15, 2)
        self._move = MoveSkill(0, 0, (0,0))
        self._id = id
        
        self._xCoord = xCoord
        self._yCoord = yCoord

        #current stun duration
        self._stun = 0
        self._blocking = False
        self._hp = HP
        self._defense = 0
        #midair attributes
        self._midair = False
        self._jumpHeight = 2
        self._falling = False
        self._velocity = 0
        
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
            if self._inputs[self._moveNum][0] == ("skill_cancel") and self._skill_state:
                self._skill_state = False
            if not self._skill_state:
                return self._inputs[self._moveNum]
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
    
    def get_blocking(self):
        '''Returns player current block status as boolean'''
        return self._blocking
    
    def get_last_move(self):
        '''Returns player's most recent move -> (move, moveValue)
           as (string, any type)
        '''
        return self._moves[-1]