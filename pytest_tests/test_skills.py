from GameManager import execute_one_turn, setupGame
from Hackethon2024.turnUpdates import playerToJson
import Submissions.Player1 as p1
import Submissions.Player2 as p2

from Hackethon2024.GameManager import setupGame


def test_test():
    assert 1==1


def test_start_game():
    print("WOW")
    p1_script = p1.Script()
    p2_script = p2.Script()
    player1, player2 = setupGame(p1_script, p2_script)

    stun1 = stun2 = 0

    p1_json_dict = {
        'hp': [],
        'xCoord': [],
        'yCoord': [],
        'state': [],
        'stun': [],
        'midair': [],
        'falling':[],
        'ProjectileType': None,
        'projXCoord':[],
        'projYCoord':[]
        }
    p2_json_dict = {
        'hp': [],
        'xCoord': [],
        'yCoord': [],
        'state': [],
        'stun': [],
        'midair': [],
        'falling':[],
        'ProjectileType': None,
        'projXCoord':[],
        'projYCoord':[]
    }

    projectiles = []

    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    playerToJson(player1, p1_json_dict)
    playerToJson(player2,p2_json_dict)

    projectiles, stun1, stun2, p1_dead, p2_dead = execute_one_turn(player1, player2, p1_script, p2_script, p1_json_dict, p2_json_dict, projectiles, stun1, stun2)
    playerToJson(player1, p1_json_dict)
    playerToJson(player2,p2_json_dict)

    print("P1 JSON DICT", p1_json_dict)
    print("P2 JSON DICT", p2_json_dict)