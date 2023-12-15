from Skills import AttackSkill, DashAttackSkill
class Player_Controller:
    def __init__(self, xCoord, yCoord, HP, direction):
        self.primarySkill = DashAttackSkill(3, 15)
        self.secondarySkill = ""
        
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.width = 10
        self.height = 20
        self.moves = []
        self.blocking = False
        self.hp = HP
        
        #current stun duration
        self.stun = 0
        self.midair = False
        #direction player is facing
        self.direction = direction
        
        self.moveNum = 0
        
        #for testing
        #player scripts will append moves to this
        self.moveList = [("dash_attack", None), ("move", (1,1)), ("attack","light"), 
        ("move", (1,0)), ("move", (1,0)), ("attack", "light"), 
        ("move", (1,0)), ("attack", "light")]
    def action(self):
        if self.moveNum < len(self.moveList):
            # print(f"{self.moveNum} , {self.moveList[self.moveNum]}")
            return self.moveList[self.moveNum]
        return ("NoMove")