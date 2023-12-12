from Skills import AttackSkill
class Player_Controller:
    def __init__(self, xCoord, yCoord, HP, direction):
        self.primarySkill =""
        self.secondarySkill = ""
        self.lightAtk = AttackSkill(0, 1, 5, 1, True, 1, 0)
        self.heavyAtk = AttackSkill(2, 4, 10, 2, True, 1, 1)
        
        self.xCoord = xCoord
        self.yCoord = yCoord
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
        self.moveList = [("move", (1,1)), ("attack","light"), 
        ("move", (1,0)), ("move", (1,0)), ("attack", "light"), 
        ("move", (1,0)), ("attack", "light")]

    def updateGravity(self):
        if self.midair:
            self.yCoord -= 1
            if self.yCoord == 0: 
                self.midair = False

    def updateCooldown(self):
        self.lightAtk.reduceCd(1)
        self.heavyAtk.reduceCd(1)

    def updateStun(self):
        if self.stun >0:
            self.stun -=1

    def update(self):
        self.updateGravity(self)
        self.updateCooldown(self)
        self.updateStun(self)
    
    def action(self):
        if self.moveNum < len(self.moveList):
            # print(f"{self.moveNum} , {self.moveList[self.moveNum]}")
            return self.moveList[self.moveNum]
        return ("NoMove")
    