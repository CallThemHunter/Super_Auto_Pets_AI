from typing import List
from Core.GameElements import *
import random


class Team:
    def __init__(self, roster: List[Animal], equipment: List[Equipment]):
        self.animals = roster
        self.equipment = equipment
        self.acting = 0
        # random.seed(1)

    def size(self):
        i = 0
        for animal in self.animals:
            if not isinstance(animal, Empty):
                i += 1
        return i

    def lowest_health(self):
        return min(self.animals, key=lambda animal: animal.battle_hp)

    def ret_diff_tiers(self):
        pass

    def level(self):
        # level of currently acting team member
        return self.animals[self.acting].level()

    def faint(self, target):
        self.equipment[target] = Unarmed()
        self.animals[target] = Empty()

    def summon(self, animal, position):
        # insert unit to that position, if there would be too many units, insert and delete excess.
        self.animals.insert(animal, position)
        self.equipment.insert(Unarmed(), position)

        if self.size() == 6:
            self.animals.pop(5)
            self.equipment.pop(5)

    def has_lvl3(self):
        for animal in self.animals:
            if animal.level() == 3:
                return True
        return False

    def leftmost_unit(self):
        i = 0
        while isinstance(self.animals[i], Empty):
            # TODO will probably have to make it check for battle hp?
            i += 1
        return self.animals[i]

    def rightmost_unit(self):
        i = len(self.animals)-1
        while isinstance(self.animals[i], Empty):
            i -= 1
        return self.animals[i]

    def friend_ahead(self):
        for j in range(self.acting, len(self.animals)):
            if isinstance(self.animals[j], Empty):
                return self.animals[j]

    def other_lvl2_or_3(self):
        a: List[int] = list(range(0, 5))
        a.remove(self.acting)
        for i in a:
            if self.animals[i].level() == 1:
                a.remove(i)
        return [self.animals[i] for i in a]

    def friends_ahead(self, n):
        ret = []
        i = 0
        for j in range(self.acting, len(self.animals)):
            if isinstance(self.animals[j], Empty):
                if i < n:
                    ret += [self.animals[j]]
                    i += 1
        if len(ret) == 1:
            return ret[0]
        return ret

    def friend_behind(self):
        for j in range(self.acting-1, -1, -1):
            if isinstance(self.animals[j], Empty):
                return self.animals[j]

    def friends_behind(self, n):
        ret = []
        i = 0
        for j in range(self.acting-1, -1, -1):
            if isinstance(self.animals[j], Empty):
                if i < n:
                    ret += [self.animals[j]]
                    i += 1
        if len(ret) == 1:
            return ret[0]
        return ret

    def random_friend(self):
        a: List[int] = list(range(0, 5))
        a.remove(self.acting)
        for i in a:
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        if a == []:
            return None
        return self.animals[random.choice(a)]

    def friends(self):
        a: List[int] = list(range(0, 5))
        a.remove(self.acting)
        for i in a:
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        return [self.animals[i] for i in a]

    def random_friends(self, n):
        a = list(range(0, 5))
        a.remove(self.acting)
        for i in a:
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        if a == []:
            return []
        if len(a) < n:
            return [self.animals[i] for i in a]
        else:
            return random.sample([self.animals[i] for i in a], n)

    def random_unit(self):
        a = list(range(0, 5))
        for i in a:
            if isinstance(self.animals[i], Empty):
                a.remove(i)

        return self.animals[random.choice(list(range(0, 5)))]

    def random_units(self, n):
        a = list(range(0, 5))
        for i in a:
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        if a == []:
            return []
        if len(a) < n:
            return [self.animals[i] for i in a]
        else:
            return random.sample([self.animals[i] for i in a], n)

    def random_units_idx(self, n):
        a = list(range(0, 5))
        for i in a:
            if isinstance(self.animals[i], Empty):
                a.remove(i)
        if a == []:
            return []
        if len(a) < n:
            return [self.animals[i] for i in a]
        else:
            return random.sample(a, n)