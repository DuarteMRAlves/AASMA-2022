import abc
import grid
import entity
import numpy as np


class Environment:

    def __init__(self, map: grid.Map, init_passengers: int, printer: "Printer", seed: int = None):
        self.map = map
        self._rng = np.random.default_rng(seed=seed)
        self._printer = printer
        
        self.passengers = [self._create_passenger() for _ in range(init_passengers)]
        print(self.passengers)

    def render(self):
        self._printer.print(self)

    def _create_passenger(self):
        """Creates a passenger with random Pick-Up and Drop-Off locations."""

        possible_passenger_locations = [p for p in self.map.possible_passenger_positions]
        pick_up_loc = self._rng.choice(possible_passenger_locations)
        possible_passenger_locations.remove(pick_up_loc)
        drop_off_loc = self._rng.choice(possible_passenger_locations)
        return entity.Passenger(
            pick_up=pick_up_loc, drop_off=drop_off_loc, pick_up_time=0, travel_time=0,
        )


class Printer(abc.ABC):
    @abc.abstractmethod
    def print(self, env: Environment):
        pass