JSONFILL = True # set to True for midtick info, like hurt etc
LEFTBORDER = 0
RIGHTBORDER = 15
DIST_FROM_MID = 0.5 if (RIGHTBORDER-LEFTBORDER)%2 else 1
BUFFERTURNS = 2
HP = 50
#game settings
timeLimit = 2
movesPerSecond = 4
#direction constants
GORIGHT = 1
GOLEFT = -1

LEFTSTART = int((RIGHTBORDER-LEFTBORDER)/2 - DIST_FROM_MID)
RIGHTSTART = int((RIGHTBORDER-LEFTBORDER)/2 + DIST_FROM_MID)

