
from Skills import AttackSkill, BlockSkill
class Player_Controller:
    def __init__(self, xCoord, yCoord, HP, direction):
        self.primarySkill ="dash_attack"
        self.secondarySkill = ""
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.lightAtk = AttackSkill(0, 1, 5, 1, True, 1, 0)
        self.heavyAtk = AttackSkill(2, 4, 10, 2, True, 1, 1)
        self.block = BlockSkill(0, 0, 15, 2)
        
        self.blocking = False
        self.hp = HP
        self.jumpHeight = 2
        self.falling = False
        
        #current stun duration
        self.stun = 0
        self.midair = False
        #direction player is facing
        self.direction = direction
        
        self.moveNum = 0
        self.moves = []
        #for testing
        #player scripts will append moves to this
        self.moveList = [("dash_attack", None), ("move", (1,1)), ("move",(1,1)), ("move", (-1,0)), ("attack", "light"), ("attack", "heavy")]
    def action(self):
        if self.moveNum < len(self.moveList):
            # print(f"{self.moveNum} , {self.moveList[self.moveNum]}")
            return self.moveList[self.moveNum]
        return ("NoMove")