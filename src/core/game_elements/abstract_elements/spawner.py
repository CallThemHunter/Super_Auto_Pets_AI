import random
from typing import List, Union

from ..game_objects import Base, Items, Paid1
from . import Animal, Equipment


# outputs a random animal given a range of tiers
class Spawner:
    def __init__(self, mode):
        self._mode = mode
        self._population = []
        if mode == "base":
            animals = Base().animals
            self._population = []
            for tier in animals:
                self._population.append([])
                for animal in tier:
                    if animal.rollable:
                        self._population[-1].append(animal)

        elif mode == "paid_1":
            animals = Paid1().animals
            self._population = []
            for tier in animals:
                self._population.append([])
                for animal in tier:
                    if animal.rollable:
                        self._population[-1].append(animal)

        elif mode == "food":
            items = Items().items
            self._population = []
            for tier in items:
                self._population.append([])
                for item in tier:
                    if item.rollable:
                        self._population[-1].append(item)

    def spawn(self, max_tier) -> type(Union[Animal, Equipment]):
        return type(self.spawn_n(1, max_tier)[0])()

    def spawn_n(self, n, max_tier) -> List[type(Union[Animal, Equipment])]:
        max_idx = min(max_tier, 6)
        max_idx = max(max_idx, 1)

        subpopulation = sum(self._population[:max_idx], [])
        sample = random.choices(subpopulation, k=n)
        return [type(instance)() for instance in sample]

    def spawn_tier(self, tier) -> type(Union[Animal, Equipment]):
        idx = tier - 1
        idx = max(idx, 0)
        idx = min(idx, 5)

        subpopulation = self._population[idx]
        return type(random.choice(subpopulation))()
