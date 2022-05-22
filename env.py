import abc
import grid
import entity
import log
import numpy as np

from typing import List


class Environment:

    taxis: List[entity.Taxi]


    def __init__(self, map: grid.Map, init_taxis: int, init_passengers: int, printer: "Printer", seed: int = None):
        self.map = map
        self._rng = np.random.default_rng(seed=seed)
        self._printer = printer

        self._logger = log.new(__name__)
        self._timestep = 0

        self.taxis = []
        for _ in range(init_taxis):
            self.taxis.append(self._create_taxi())

        self.passengers = []
        for _ in range(init_passengers):
            self.passengers.append(self._create_passenger())

    def render(self):
        self._printer.print(self)

    def _create_taxi(self) -> entity.Taxi:
        """Creates a taxi with a random location and direction.
        
        The taxi initial location will not overlap with another taxi."""

        occupied_locations = set()
        for t in self.taxis:
            occupied_locations.add(t.loc)

        possible_taxi_locations = [
            l
            for l in self.map.possible_taxi_positions
            if l not in occupied_locations
        ]
        if len(possible_taxi_locations) == 0:
            raise ValueError("Unable to create taxi: Not enough free locations.")
        loc = self._rng.choice(possible_taxi_locations)
        possible_taxi_directions = [
            entity.Direction.UP, 
            entity.Direction.DOWN, 
            entity.Direction.LEFT, 
            entity.Direction.RIGHT,
        ]
        direction = self._rng.choice(possible_taxi_directions)
        taxi = entity.Taxi(loc=loc, direction=direction)
        log.create_taxi(self._logger, self._timestep, taxi)
        return taxi

    def _create_passenger(self):
        """Creates a passenger with random Pick-Up and Drop-Off locations.
        
        Both the passenger locations will not overlap with other passsenger
        locations.
        """

        occupied_locations = set()
        for p in self.passengers:
            occupied_locations.add(p.pick_up)
            occupied_locations.add(p.drop_off)

        possible_passenger_locations = [
            p 
            for p in self.map.possible_passenger_positions 
            if p not in occupied_locations
        ]
        if len(possible_passenger_locations) < 2:
            raise ValueError("Unable to create passenger: Not enough free locations.")
        pick_up_loc = self._rng.choice(possible_passenger_locations)
        possible_passenger_locations.remove(pick_up_loc)
        drop_off_loc = self._rng.choice(possible_passenger_locations)
        passenger = entity.Passenger(pick_up=pick_up_loc, drop_off=drop_off_loc)
        log.create_passenger(self._logger, self._timestep, passenger)
        return passenger


class Printer(abc.ABC):
    @abc.abstractmethod
    def print(self, env: Environment):
        pass