import abc
import dataclasses
import enum
import grid
import entity
import log
import numpy as np

from typing import List


@dataclasses.dataclass(frozen=True)
class Observation:
    """Defines the observation for a given agent.
    
    Attributes:
        loc: position of the agent taxi in the grid.
        has_passenger: whether the agent taxi has a passenger or not.
        taxis: positions of all the taxis in the grid.
        passengers: Pick-Up and Drop-Off locations for the passengers.
    """

    loc: grid.Position
    has_passenger: bool
    taxis: grid.Position
    passengers: entity.Passenger

class Action(enum.Enum):
    """Specifies possible actions the taxis can perform."""

    UP = 0
    """Moves the taxi up."""

    DOWN = 1
    """Moves the taxi down."""

    LEFT = 2
    """Moves the taxi to the left."""

    RIGHT = 3
    """Moves the taxi to the right."""

    STAY = 4
    """Stays in the same position."""

    PICK_UP = 5
    """Picks up an adjacent passenger."""

    DROP_OFF = 6
    """Drops off a passenger in an adjacent cell."""

    def __repr__(self) -> str:
        return f"Action({self.name})"

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

    def step(self, *actions: Action) -> List[Observation]:
        """Performs an environment step.
        
        Args:
            actions: List of actions returned by the agents.

        Returns: List of observations for the agents.
        """
        actions = list(actions)
        assert len(self.taxis) == len(actions), f"Received {len(actions)} actions for {len(self.taxis)} agents."

        self._timestep += 1

        # Log actions
        for i, act in enumerate(actions):
            log.choosen_action(self._logger, self._timestep, i, act)

        # Move taxis
        for taxi, act in zip(self.taxis, actions):
            if act in (Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT):
                self._move_taxi(taxi, act)
            elif act == Action.PICK_UP:
                taxi.pickup_up(self.passengers, self.map)
            elif act == Action.DROP_OFF:
                taxi.drop_off(self.map)
            log.taxi(self._logger,self._timestep, taxi)
            for passenger in self.passengers:
                log.passenger(self._logger, self._timestep, passenger)
            
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

    def _move_taxi(self, taxi: entity.Taxi, action: Action):
        """Move a taxi according to an action while checking for sidewalks."""
        if action == Action.UP:
            target_loc = taxi.loc.up
            target_dir = entity.Direction.UP
        elif action == Action.DOWN:
            target_loc = taxi.loc.down
            target_dir = entity.Direction.DOWN
        elif action == Action.RIGHT:
            target_loc = taxi.loc.right
            target_dir = entity.Direction.RIGHT
        elif action == Action.LEFT:
            target_loc = taxi.loc.left
            target_dir = entity.Direction.LEFT
        else:
            raise ValueError(f"Unknown direction in taxi movement {self.direction}")
        # Do not move if the target location is not a road.
        # However we still update target dir to "show" the
        # taxi went into a sidewalk.
        if not self.map.is_road(target_loc):
            target_loc = taxi.loc
        taxi.loc = target_loc
        taxi.direction = target_dir

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