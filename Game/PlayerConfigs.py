from Game.Skills import *
# use as a template for player1 and player2
class Player_Controller:
    def __init__(self, xCoord, yCoord, HP, direction, primary, secondary, id):
        self._entity_type = "player"
        self._primary_skill = primary(self)
        self._secondary_skill = secondary(self)
        self._light_atk = AttackSkill(0, 1, 3, 1, 0, True, 0, 0)
        self._heavy_atk = AttackSkill(0, 3, 5, 1, 0, True, 1, 2, recovery=1)
        self._block = BlockSkill(0, 0, 10, 2)
        self._move = MoveSkill(0, 0, (0,0))
        self._id = id
        
        self._xCoord = xCoord
        self._yCoord = yCoord

        #current stun duration
        self._stun = 0
        self._recovery = 0
        self._mid_startup = False
        self._blocking = False
        self._hp = HP
        self._defense = 1
        self._superarmor = False
        #midair attributes
        self._midair = False
        self._default_jump_height = 1
        self._jump_height = self._default_jump_height
        self._falling = False
        self._velocity = 0
        self._airvelo = 0
        
        #direction player is facing
        self._direction = direction
        
        # actual moves taken
        self._moves = []
        self._move_num = 0
        self._skill_state = False
        
        # moves input by player
        self._inputs = []
        
        # buffs
        self._speed = 1
        self._atkbuff = 0
        self._curr_buff_duration = 0
        
    def _action(self):
        if self._move_num < len(self._inputs) and self._inputs[self._move_num]:
            return self._inputs[self._move_num]
        else:   
            return ("NoMove", None)
           
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
            return self._primary_skill.get_cooldown()
        else:
            return self._primary_skill.on_cooldown()
        
    
    def secondary_on_cd(self, get_timer):
        if get_timer:
            return self._primary_skill.get_cooldown()
        else: 
            return self._secondary_skill.on_cooldown()
    
    def heavy_on_cd(self):
        return self._heavy_atk.on_cooldown()
    
    def primary_range(self):
        try:
            return self._primary_skill._xRange
        except:
            return 0
    
    def secondary_range(self):
        try:
            second_range = self._secondary_skill._xRange
            if second_range == 0:
                # this is a projectile
                return self._secondary_skill.path_range()
        except:
            return 0
        
    def get_past_move(self, turns):
        if turns <= len(self._moves):
            return self._moves[-turns]
        else:
            return None
        
    def get_recovery(self):
        return self._recovery
    
    def skill_cancellable(self):
        return (self._skill_state or self._mid_startup)
    
    def get_primary_name(self):
        return self._primary_skill._skillType
    
    def get_secondary_name(self):
        return self._secondary_skill._skillType
    
    def get_landed(self):
        return self._move._cooldown > 0