import os
import random
from GameManager import startGame

dir_path = os.path.join(os.getcwd(), "Submissions")
player = os.listdir(dir_path)

clean_player = []
for i in player:
    if i[-3:] == ".py":
        clean_player.append(i[:-3])
print(clean_player)

roundNum = 1


class TournamentNode:
    def __init__(self, player=None, left=None, right=None):
        self.player = player
        self.left = left
        self.right = right

def buildBracket(players):
    if not players:
        return None

    if len(players) == 1:
        return TournamentNode(player=players[0])

    middle = len(players) // 2
    left_child = buildBracket(players[:middle])
    right_child = buildBracket(players[middle:])

    return TournamentNode(left=left_child, right=right_child)

def printBracket(node, depth=0):
    if node:
        print("  |" * depth, node.player)
        printBracket(node.left, depth + 1)
        printBracket(node.right, depth + 1)
    

def findWinner(node):
    global roundNum
    if not node:
        return None

    if node.player:
        return node.player
    print(f"RoundNum: {roundNum}")
    printBracket(node)
    print("\n")
    left_winner = findWinner(node.left)
    right_winner = findWinner(node.right)

    retval = startGame(left_winner, right_winner, "Submissions", roundNum)
    print(retval)
    roundNum += 1
    return retval

def simulateTournament(players_list, randomize = False):
    if randomize:
        random.shuffle(players_list)
    root = buildBracket(players_list)
    print("Initial Bracket:")
    # a bunch of nones are cuz the winners arent listed
    # the branch is printed sideways in a very weird :P
    winner = findWinner(root)
    print("\nThe winner is:", winner)
    print(clean_player)
    printBracket(root)


repeat_simulations = 1
for i in range(repeat_simulations):
    simulateTournament(clean_player, randomize=True)
    roundNum = 1