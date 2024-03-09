# from GameManager import setupGame
# import ..Submissions.Player1 as p1
# import ..Submissions.Player2 as p2

from Hackethon2024.GameManager import setupGame


def test_test():
    pass

def test_start_game():
    print("WOW")
    p1_script = p1.Script()
    p2_script = p2.Script()
    player1, player2 = setupGame(p1_script, p2_script)

    # stun1 = stun2 = 0

    # p1_json_dict = {
    #     'hp': [],
    #     'xCoord': [],
    #     'yCoord': [],
    #     'state': [],
    #     'stun': [],
    #     'midair': [],
    #     'falling':[],
    #     'ProjectileType': None,
    #     'projXCoord':[],
    #     'projYCoord':[]
    #     }
    # p2_json_dict = {
    #     'hp': [],
    #     'xCoord': [],
    #     'yCoord': [],
    #     'state': [],
    #     'stun': [],
    #     'midair': [],
    #     'falling':[],
    #     'ProjectileType': None,
    #     'projXCoord':[],
    #     'projYCoord':[]
    # }

    # projectiles = []

