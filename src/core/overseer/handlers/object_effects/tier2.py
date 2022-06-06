from typing import TYPE_CHECKING, Tuple

from ....game_elements.abstract_elements import Animal
from ....game_elements.game_objects.animals import Dirty_Rat
from ....game_elements.game_objects.equipment import Weak

if TYPE_CHECKING:
    from ... import MessageAgent


class Tier2:
    @staticmethod
    def bat(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        units = agent.team_opposing_(actor).random_units(agent.actor(actor).level)

        for unit in units:
            unit.held = Weak()

    @staticmethod
    def crab(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        battle_hp = agent.team_of_(actor).highest_health_unit().battle_hp * agent.actor(actor).level // 2
        agent.actor(actor).battle_hp = max(1, battle_hp)

    @staticmethod
    def dodo(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        unit = agent.actor(actor)
        battle_atk = unit.battle_atk * unit.level // 2
        agent.team_of_(actor).friend_ahead(actor[1]).battle_atk += battle_atk

    @staticmethod
    def dirty_rat(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        pass

    @staticmethod
    def dromedary(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        if agent.actor(actor).level == 1:
            agent.shop.buff(1, 1)
        elif agent.actor(actor).level == 2:
            agent.shop.buff(2, 2)
        else:
            agent.shop.buff(3, 3)

    @staticmethod
    def elephant(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        friend_behind = agent.team_of_(actor).friend_behind(actor[1])
        friend_tup = (actor[0], agent.team_of_(actor).animals.index(friend_behind))
        for _ in range(agent.actor(actor).level):
            agent.deal_ability_damage_handle_hurt(1, actor, friend_tup)

    @staticmethod
    def flamingo(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        friends = agent.team_of_(actor).friends_behind(actor[1], 2)
        if agent.actor(actor).level == 1:
            agent.buff(friends, 1, 1)
        elif agent.actor(actor).level == 2:
            agent.buff(friends, 2, 2)
        else:
            agent.buff(friends, 3, 3)

    # hedgehog has to trigger the hurt trigger!!
    @staticmethod
    def hedgehog(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int], fainted: Animal):
        damage = 2 * fainted.level

        units = agent.sorted_team("both")
        for unit in units:
            if unit in agent.team:
                target = ("team", agent.team.animals.index(unit))
            else:
                target = ("enemy", agent.enemy.animals.index(unit))

            agent.deal_ability_damage_handle_hurt(damage, actor, target)

    @staticmethod
    def peacock(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        if agent.actor(actor).level == 1:
            agent.actor(actor).temp_buff(2, 0)
        elif agent.actor(actor).level == 2:
            agent.actor(actor).temp_buff(4, 0)
        else:
            agent.actor(actor).temp_buff(6, 0)

    @staticmethod
    def rat(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int], fainted: Animal):
        for _ in range(fainted.level):
            unit = Dirty_Rat()
            unit.battle_atk = 1
            unit.battle_hp = 1
            agent.team_opposing_(actor).summon(unit, 0)

    @staticmethod
    def shrimp(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        if agent.actor(actor).level == 1:
            agent.team_of_(actor).random_friend(actor[1]).temp_buff(0, 1)
        elif agent.actor(actor).level == 2:
            agent.team_of_(actor).random_friend(actor[1]).temp_buff(0, 2)
        else:
            agent.team_of_(actor).random_friend(actor[1]).temp_buff(0, 3)

    @staticmethod
    def spider(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int], fainted: Animal):
        unit: Animal = agent.shop[0].spawner.spawn_tier(3)

        # stats fixed at 2, 2
        unit.battle_atk = 2
        unit.battle_hp = 2

        if fainted.level == 1:
            unit.xp = 0
        elif fainted.level == 2:
            unit.xp = 2
        else:
            unit.xp = 5

        agent.summon(unit, actor)

    @staticmethod
    def swan(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        if agent.actor(actor).level == 1:
            agent.gold += 1
        elif agent.actor(actor).level == 2:
            agent.gold += 2
        else:
            agent.gold += 3

    @staticmethod
    def tabby_cat(agent: 'MessageAgent', actor: Tuple[str, int], target: Tuple[str, int]):
        if agent.actor(actor).level == 1:
            [friend.temp_buff(1, 0) for friend in agent.team_of_(actor).friends(actor[1])]
        elif agent.actor(actor).level == 2:
            [friend.temp_buff(2, 0) for friend in agent.team_of_(actor).friends(actor[1])]
        else:
            [friend.temp_buff(3, 0) for friend in agent.team_of_(actor).friends(actor[1])]
