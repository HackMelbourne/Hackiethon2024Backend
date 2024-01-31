from Skills import *
# use as a template for player1 and player2
class Player_Controller:
    def __init__(self, xCoord, yCoord, HP, direction):
        self.playerID = 2
        self.primarySkill = TeleportSkill()
        self.secondarySkill = UppercutSkill()
        self.lightAtk = AttackSkill(0, 1, 5, 1, 0, True, 1, 0)
        self.heavyAtk = AttackSkill(2, 4, 10, 2, 0, True, 1, 1)
        self.block = BlockSkill(0, 0, 15, 2)
        self.move = MoveSkill(0, 0, (0,0))
        
        self._xCoord = xCoord
        self._yCoord = yCoord

        #current stun duration
        self._stun = 0
        self._blocking = False
        self._hp = HP
        self.defense = 0
        #midair attributes
        self.midair = False
        self.jumpHeight = 2
        self.falling = False
        
        #direction player is facing
        self.direction = direction
        
        self.moves = []
        self.moveNum = 0
        
        #player scripts will append moves to this
        self.moveList = []
    def action(self):
        if self.moveNum < len(self.moveList):
            # print(f"{self.moveNum} , {self.moveList[self.moveNum]}")
            return self.moveList[self.moveNum]
        return ("NoMove")
    
    def move_self(self, action):
        self.blocking = False
        self.block.regenShield() 
        self.moves.append(action)
        self._xCoord += self.direction * action[0]
        self._yCoord += action[1]
        if self._yCoord > 0:
           self.midair = True
           
    def block_self(self, action):
        self.moves.append(action)
        self.blocking = True
        
    def get_pos(self):
        return (self._xCoord, self._yCoord)
    
    def take_damage(self, damage):
        self._hp -= damage
    

    