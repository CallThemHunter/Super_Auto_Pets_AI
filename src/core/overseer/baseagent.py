import copy
from abc import abstractmethod
from typing import List, Union, Tuple, Optional

from .state import State
from ..game_elements.abstract_elements import Animal, Team, Spawner
from ..game_elements import Shop
from ..game_systems import BattleSystem, ShopSystem


# all messages flow through the agent
class BaseAgent:
    def __init__(self, mode):
        self.__mode = mode
        self.__battler: Optional[BattleSystem] = None
        self.__shopper: Optional[ShopSystem] = None

        self.spawner = Spawner(mode)

        # all that is needed to define current state
        self.team = Team()
        self.life = 10
        self.gold = 10
        self.turn = 1
        self.battle_lost = False
        self.in_shop = True
        self.shop = Shop(mode, 1)
        ################################################

        self._team_backup = None

        self.enemy = Team()

        self.shop = Shop(mode, 1)

        # animal that triggered the event is the event_raiser
        # animal that responded to event is the acting animal
        self.event_raiser: Tuple[str, int] = ("team", 0)
        self.target: Tuple[str, int] = ("team", 0)

    @abstractmethod
    def handle_event(self, message, event_raiser=None, target=None):
        pass

    @abstractmethod
    def trigger_ability(self, message):
        pass

    @property
    def acting_team(self):
        if self.event_raiser[0] == "team":
            return self.team
        elif self.event_raiser[0] == "enemy":
            return self.enemy
        else:
            raise ValueError(f"{self.event_raiser[0]} is not a valid team type")

    @property
    def target_team(self):
        if self.target[0] == "team":
            return self.team
        elif self.event_raiser[0] == "enemy":
            return self.enemy
        else:
            raise ValueError(f"{self.target[0]} is not a valid team type")

    @property
    def event_raising_animal(self) -> Animal:
        if self.event_raiser[0] == "team":
            return self.team.animals[self.event_raiser[1]]
        elif self.event_raiser[0] == "enemy":
            return self.enemy.animals[self.event_raiser[1]]
        raise ValueError("event raiser tuple's string should be either team or enemy")

    @property
    def target_animal(self) -> Animal:
        if self.target[0] == "team":
            return self.team.animals[self.target[1]]
        elif self.target[0] == "enemey":
            return self.enemy.animals[self.target[1]]
        raise ValueError("target tuple's string should be either team or enemy")

    @property
    def team_opposing_event_raiser(self):
        if self.event_raiser[0] == "team":
            return self.enemy
        elif self.event_raiser[0] == "enemy":
            return self.team
        else:
            raise ValueError(f"{self.event_raiser[0]} is not a valid team type")

    # re-enter shop from a given state
    # used for simulation and replay
    @staticmethod
    @abstractmethod
    def load(state: State) -> 'BaseAgent':
        pass

    def save(self, include_shop: bool) -> State:
        if include_shop:
            state = State(
                self.__mode, self.turn, self.life, self.gold, self.battle_lost, self.team, self.shop
            )
        else:
            state = State(
                self.__mode, self.turn, self.life, self.gold, self.battle_lost, self.team
            )

        return state

    # enables reset of team after a battle
    def store_backup(self):
        self._team_backup = copy.deepcopy(self.team)

    def load_backup(self):
        if self._team_backup is not None:
            self.team = self._team_backup
            self._team_backup = None

    def set_battler(self, battle_system: BattleSystem):
        self.__battler = battle_system

    def set_shopper(self, game_system: ShopSystem):
        self.__shopper = game_system

    def reset_temp_stats(self):
        for animal in self.team.animals:
            animal.reset_temp_stats()

    def _nop(self):
        return

    def buff(self, unit: Union[List[Animal], Animal], atk, hp):
        if self.in_shop:
            if isinstance(unit, Animal):
                unit.permanent_buff(atk, hp)
            else:
                for animal in unit:
                    animal.permanent_buff(atk, hp)
        else:
            if isinstance(unit, Animal):
                unit.temp_buff(atk, hp)
            else:
                for animal in unit:
                    animal.temp_buff(atk, hp)
        return

    def summon(self, unit: Animal):
        if self.in_shop:
            self.__shopper.summon(unit)
        else:
            self.__battler.summon(unit)
