from typing import TYPE_CHECKING

from ....eventnames import ON_FAINT
from ....game_elements.game_objects.equipment import *

if TYPE_CHECKING:
    from ... import MessageAgent


class Equipment:
    @staticmethod
    def apple(agent: 'MessageAgent'):
        # raise eat food
        agent.team.animals[agent.team.acting].permanent_buff(1, 1)

    @staticmethod
    def honey(agent: 'MessageAgent'):
        # raise eat food
        pass

    @staticmethod
    def cupcake(agent: 'MessageAgent'):
        # raise eat food
        agent.team.animals[agent.team.acting].temp_buff(3, 3)

    @staticmethod
    def meat_bone(agent: 'MessageAgent'):
        # raise eat food
        pass

    @staticmethod
    def sleeping_pill(agent: 'MessageAgent'):
        # raise eat food
        # raise faint, have variables set properly
        agent.event_raiser = agent.team.acting
        agent.handle_event(ON_FAINT)

    @staticmethod
    def garlic(agent: 'MessageAgent'):
        # raise eat food
        pass

    @staticmethod
    def salad_bowl(agent: 'MessageAgent'):
        units = agent.team.random_units_idx(2)
        for unit in units:
            # raise eat food
            pass
