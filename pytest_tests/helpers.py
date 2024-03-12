from Game.GameManager import get_empty_json, setupGame
from Game.gameSettings import JSONFILL
from Game.turnUpdates import playerToJson


def init_game(p1, p2):
    p1_script = p1.Script()
    p2_script = p2.Script()
    player1, player2 = setupGame(p1_script, p2_script)
    stun1 = stun2 = 0
    p1_json_dict = get_empty_json()
    p2_json_dict = get_empty_json()

    projectiles = []

    if JSONFILL:
        playerToJson(player1, p1_json_dict, fill=JSONFILL, checkHurt = JSONFILL, start=True)
        playerToJson(player2,p2_json_dict, fill=JSONFILL, checkHurt = JSONFILL, start=True)

    return p1_script, p2_script, player1, player2, stun1, stun2, p1_json_dict, p2_json_dict, projectiles

# only adds 1 x to coords
def artificially_move_player(player, x, p_json_dict):
    player._xCoord = x

    if JSONFILL:
        playerToJson(player, p_json_dict, fill=JSONFILL, checkHurt = JSONFILL, start=True)