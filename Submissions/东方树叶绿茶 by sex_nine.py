from types import SimpleNamespace
from typing import List, Optional


def noop(*_args, **_kwargs):
    pass


PROD = True
if PROD:
    import sys

    print = noop
    sys.modules["ext.Game"] = __import__("Game")

from ext.Game.PlayerConfigs import Player_Controller
from ext.Game.Skills import Meditate, get_skill
from ext.Game.projectiles import Grenade, Projectile
from ext.Game.gameSettings import HP, LEFTBORDER, TIME_LIMIT, MOVES_PER_SECOND, RIGHTBORDER

TOTAL_TICKS = TIME_LIMIT * MOVES_PER_SECOND
LAST_TICK = TOTAL_TICKS  # for some reason, get_move is called 121 times, must be an off-by-one error in the game lmfao

PRIMARY_SKILL = Meditate
SECONDARY_SKILL = Grenade

ACTIONS = SimpleNamespace(
    JUMP=("move", (0, 1)),
    MOVE_FORWARD=("move", (1, 0)),
    MOVE_BACK=("move", (-1, 0)),
    JUMP_FORWARD=("move", (1, 1)),
    JUMP_BACKWARD=("move", (-1, 1)),
    LIGHT_ATTACK=("light",),
    HEAVY_ATTACK=("heavy",),
    BLOCK=("block",),
    PRIMARY=get_skill(PRIMARY_SKILL),
    SECONDARY=get_skill(SECONDARY_SKILL),
    CANCEL_SKILL=("skill_cancel",),
    NOOP="NoMove",
)


class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL

    def init_player_skills(self):
        return self.primary, self.secondary

    @staticmethod
    def _heal(data: dict, tick: int):
        data["healed_at"] = tick
        return ACTIONS.PRIMARY

    @staticmethod
    def _grenade(data: dict, tick: int):
        data["secondary_at"] = tick
        return ACTIONS.SECONDARY

    @staticmethod
    def _safely_get_move_name(player: Player_Controller, index: int) -> Optional[tuple]:
        try:
            return player._moves[index][0]
        except IndexError:
            return None

    def get_move(self, player: Player_Controller, enemy: Player_Controller, player_projectiles: List[Projectile],
                 enemy_projectiles: List[Projectile]):
        if not player.__dict__.get("_data"):
            player.__dict__["_data"] = {
                "tick": -1,
                "block_next": False,
                "healed_at": -1,
                "secondary_at": -1,
            }

        data = player._data
        data["tick"] += 1

        tick = data["tick"]
        print("tick: ", tick)
        if self._safely_get_move_name(enemy, -1) == "dash_attack" and self._safely_get_move_name(enemy,
                                                                                                 -2) != "dash_attack":
            return ACTIONS.JUMP_FORWARD

        if len(player_projectiles) > 0:
            projectile = player_projectiles[0]
            print("kms: ", projectile._pathIndex)

        # this is because of the weird shit with two grenades cancelling each other out, with
        # usually whichever one shoots last takes priority (maybe, idk, weird behaviour)
        if tick == 0 and enemy.get_secondary_name() != "grenade":
            return self._grenade(data, tick)
        if tick == 1 and enemy.get_secondary_name() == "grenade":
            return self._grenade(data, tick)

        if tick >= LAST_TICK:
            return self._heal(data, tick)

        if data["block_next"]:
            data["block_next"] = False
            return ACTIONS.BLOCK

        projectile: Optional[Projectile] = None
        dont_move_forward = False
        if len(enemy_projectiles) > 0:
            projectile = enemy_projectiles[0]

            if projectile.get_type() == "grenade":
                ticks_till_landing = 3 - projectile._pathIndex  # 0 = exploding this tick
                print("TTL:", ticks_till_landing)

                landing_coord = projectile._playerInitPos
                landing_coord = ((landing_coord[0] + projectile._path[-1][0]), landing_coord[1])
                landing_x = landing_coord[0]
                print("LC: ", landing_coord)
                print("PC: ", player.get_pos())

                player_x = player.get_pos()[0]
                in_blast_zone = abs(player_x - landing_x) <= 1
                print("in blast zone: ", in_blast_zone)

                enemy_x = enemy.get_pos()[0]
                enemy_in_way = enemy_x == player_x + player._direction * 2 or enemy_x == player_x + player._direction

                # this is so fucking dumb holy shit why does this game work like this
                if ticks_till_landing == 2 and projectile.get_pos()[0] == player_x:
                    print("MOVE bc COLLISION")
                    return ACTIONS.JUMP_FORWARD if enemy_in_way else ACTIONS.MOVE_FORWARD

                if in_blast_zone:
                    if player_x == landing_x:
                        if player_x + player._direction * 2 >= RIGHTBORDER or player_x + player._direction * 2 <= LEFTBORDER:
                            print("JUDGE: BACK bc BORDER")
                            return ACTIONS.MOVE_BACK
                        print("JUDGE: MOVE OR JUMP_FORWARD")
                        return ACTIONS.JUMP_FORWARD if enemy_in_way else ACTIONS.MOVE_FORWARD

                    direction_to_move = player_x - landing_x
                    if player_x + direction_to_move >= RIGHTBORDER or player_x + direction_to_move <= LEFTBORDER:
                        print("CHANGE DIRECTION bc BORDER")
                        direction_to_move = -direction_to_move

                    if direction_to_move == player._direction:
                        print("JUDGE: MOVE OR JUMP_FORWARD 2")
                        return ACTIONS.JUMP_FORWARD if enemy_in_way else ACTIONS.MOVE_FORWARD

                    print("JUDGE: BACK")
                    return ACTIONS.MOVE_BACK

                if abs((player_x + player._direction) - landing_x) <= 1:
                    dont_move_forward = True

            if projectile.get_pos()[0] + projectile._direction == player.get_pos()[0]:
                # print()
                if projectile.get_type() == "hadoken":
                    return ACTIONS.JUMP_FORWARD
                if projectile.get_type() != "beartrap":
                    data["block_next"] = True
                    return ACTIONS.BLOCK

        player_x = player.get_pos()[0]
        enemy_x = enemy.get_pos()[0]
        distance = abs(player_x - enemy_x)

        can_heal = not player.primary_on_cd(get_timer=False) and tick < LAST_TICK - 20
        if can_heal and player.get_hp() <= 90:
            print(f"HEALING | {player.get_hp()}")
            return self._heal(data, tick)
        if can_heal and LAST_TICK - 24 < tick < LAST_TICK - 20:
            print(f"HEALING | {player.get_hp()}")
            return self._heal(data, tick)

        if distance > 3 and not (projectile and projectile.get_type() == "beartrap" and player_x + player._direction ==
                                 projectile.get_pos()[0]):
            print("JUDGE: MOVE_FORWARD bc DISTANCE")
            return ACTIONS.LIGHT_ATTACK if dont_move_forward else ACTIONS.MOVE_FORWARD

        if tick > 100 and enemy.get_hp() > player.get_hp():
            if distance > 1:
                return ACTIONS.LIGHT_ATTACK if dont_move_forward else ACTIONS.MOVE_FORWARD
            return ACTIONS.LIGHT_ATTACK

        can_secondary = not player.secondary_on_cd(get_timer=False)
        if can_secondary and distance > 1:
            return self._grenade(data, tick)

        return ACTIONS.LIGHT_ATTACK
