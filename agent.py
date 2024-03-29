import abc
import entity
import env
import grid
import numpy as np

from typing import List

class Base(abc.ABC):
    """Base class for all agents."""

    _last_observation: env.Observation
    
    def see(self, obs: env.Observation) -> None:
        """Observes the current state of the environment through its sensores."""
        self._last_observation = obs

    @abc.abstractmethod
    def act(self) -> env.Action:
        """Acts based on the last observation and any other information."""
        pass

class Random(Base):
    """Baseline agent that randomly chooses an action at each timestep."""

    def __init__(self, seed: int = None) -> None:
        self._rng = np.random.default_rng(seed=seed)
        self._actions = [
            env.Action.UP,
            env.Action.DOWN,
            env.Action.LEFT,
            env.Action.RIGHT,
            env.Action.STAY,
            env.Action.PICK_UP,
            env.Action.DROP_OFF,
        ]

    def act(self) -> env.Action:
        return self._rng.choice(self._actions)


class PathBased(Base):
    """Utility class with path based functions."""

    def _pickup_nearest_passenger(
        self, map: grid.Map, agent_taxi: entity.Taxi, passengers: List[entity.Passenger],
    ) -> env.Action:
        if len(passengers) == 0:
            return env.Action.STAY

        shortest_paths = [
            self._bfs_with_positions(map, agent_taxi.loc, p.pick_up) 
            for p in passengers
        ]
        path_idx = np.argmin([len(p) for p in shortest_paths])
        return self._move_in_path_and_act(shortest_paths[path_idx], env.Action.PICK_UP)

    def _dropoff_current_passenger(self, map: grid.Map, agent_taxi: entity.Taxi) -> env.Action:
        passenger = agent_taxi.has_passenger
        shortest_path = self._bfs_with_positions(map, agent_taxi.loc, passenger.drop_off)
        return self._move_in_path_and_act(shortest_path, env.Action.DROP_OFF)

    def _move_in_path_and_act(self, path: List[grid.Position], last_action: env.Action) -> env.Action:
        if len(path) == 1:
            return last_action
        curr_pos = path[0]
        next_pos = path[1]
        if next_pos == curr_pos.up:
            return env.Action.UP
        elif next_pos == curr_pos.down:
            return env.Action.DOWN
        elif next_pos == curr_pos.left:
            return env.Action.LEFT
        elif next_pos == curr_pos.right:
            return env.Action.RIGHT
        else:
            raise ValueError(
                f"Unknown adj direction: (curr_pos: {curr_pos}, next_pos: {next_pos})"
            )

    def _bfs_with_positions(
        self, map: grid.Map, source: grid.Position, target: grid.Position,
    ) -> List[grid.Position]:
        """Computes the list of positions in the path from source to target.
        
        It uses a BFS so the path is the shortest path."""
        
        # The queue stores tuple with the nodes to explore
        # and the path taken to the node.
        queue = [(source, (source,))]
        # Visited stores already explored positions to avoid
        # loops.
        visited = set()
        while len(queue) > 0:
            curr, curr_path = queue.pop(0)
            if curr in target.adj:
                return list(curr_path)
            for neighbour in curr.adj:
                if neighbour not in visited and map.is_road(neighbour):
                    neighbour_path = curr_path + (neighbour,)
                    queue.append((neighbour, neighbour_path))
                    visited.add(neighbour)
        raise ValueError("No path found")


class PathPlanner(PathBased):
    """Agent that plans its path using a BFS."""

    def __init__(self, agent_id: int = 0) -> None:
        super().__init__()
        self._agent_id = agent_id

    def act(self) -> env.Action:
        map = self._last_observation.map
        agent_taxi = self._last_observation.taxis[self._agent_id]
        passengers = self._last_observation.passengers

        if agent_taxi.has_passenger is None:
            possible_passengers = [p for p in passengers if p.in_trip == entity.TripState.WAITING]
            return self._pickup_nearest_passenger(map, agent_taxi, possible_passengers)
        return self._dropoff_current_passenger(map, agent_taxi)
    

class QuadrantsSocialConventions(PathBased):
    """Agent that uses social conventions to attribute passengers.
    
    Each agent picks up from a quadrant, as follows:
    |-------------------|-------------------|
    | agent (0, 4, ...) | agent (1, 5, ...) |
    |-------------------|-------------------|
    | agent (2, 6, ...) | agent (3, 7, ...) |
    |-------------------|-------------------|
    """

    def __init__(self, agent_id: int = 0) -> None:
        super().__init__()
        self._agent_id = agent_id
        self._quadrant = (agent_id % 4) + 1

    def act(self) -> env.Action:
        map = self._last_observation.map
        agent_taxi = self._last_observation.taxis[self._agent_id]
        passengers = self._last_observation.passengers
        
        if agent_taxi.has_passenger is None:
            check_quadrant_mapper = {
                1: self._is_first_quadrant,
                2: self._is_second_quadrant,
                3: self._is_third_quadrant,
                4: self._is_fourth_quadrant,
            }
            check_quadrant_fn = check_quadrant_mapper[self._quadrant]
            passengers = [
                p for p in passengers
                if check_quadrant_fn(map, p.pick_up) and p.in_trip == entity.TripState.WAITING
            ]
            return self._pickup_nearest_passenger(map, agent_taxi, passengers)
        return self._dropoff_current_passenger(map, agent_taxi)

    def _is_first_quadrant(self, map: grid.Map, pos: grid.Position):
        return pos.x < map.width // 2 and pos.y < map.height // 2

    def _is_second_quadrant(self, map: grid.Map, pos: grid.Position):
        return pos.x >= map.width // 2 and pos.y < map.height // 2

    def _is_third_quadrant(self, map: grid.Map, pos: grid.Position):
        return pos.x < map.width // 2 and pos.y >= map.height // 2

    def _is_fourth_quadrant(self, map: grid.Map, pos: grid.Position):
        return pos.x >= map.width // 2 and pos.y >= map.height // 2


class IDsSocialConventions(PathBased):
    """Agent that uses social conventions to attribute passengers by using their ID.
    
    Each agent picks up a passenger as follows:
    
    """

    def __init__(self, agent_id: int = 0) -> None:
        super().__init__()
        self._agent_id = agent_id

    def act(self) -> env.Action:
        map = self._last_observation.map
        agent_taxi = self._last_observation.taxis[self._agent_id]
        nr_agents = len(self._last_observation.taxis)
        passengers = self._last_observation.passengers
        
        if agent_taxi.has_passenger is None:
            
            passengers = [
                p for p in passengers
                if (p.id % nr_agents) == self._agent_id and p.in_trip == entity.TripState.WAITING
            ]
            return self._pickup_nearest_passenger(map, agent_taxi, passengers)
        return self._dropoff_current_passenger(map, agent_taxi)


class Roles(PathBased):
    """Agent that attributes passengers based on distance to pick up location."""

    def __init__(self, agent_id: int = 0) -> None:
        super().__init__()
        self._agent_id = agent_id

    def act(self) -> env.Action:
        map = self._last_observation.map
        taxis = self._last_observation.taxis
        passengers = self._last_observation.passengers

        roles = []

        # First assign passengers already in trip to their taxis.
        for t in taxis:
            if t.has_passenger is not None:
                roles.append((t, t.has_passenger))
            
        possible_passengers = [p for p in passengers if p.in_trip == entity.TripState.WAITING]
        possible_taxis = [t for t in taxis if t.has_passenger is None]
        assigned_taxis = []
        for p in possible_passengers:
            shortest_paths = [
                self._bfs_with_positions(map, t.loc, p.pick_up)
                for t in possible_taxis
            ]
            taxi = None
            min_dist = np.inf
            for t, path in zip(possible_taxis, shortest_paths):
                if len(path) < min_dist and t not in assigned_taxis:
                    min_dist = len(path)
                    taxi = t
            assigned_taxis.append(taxi)
            roles.append((taxi, p))

        agent_taxi = taxis[self._agent_id]
        for t, p in roles:
            if t == agent_taxi:
                if agent_taxi.has_passenger:
                    return self._dropoff_current_passenger(map, agent_taxi)
                shortest_path = self._bfs_with_positions(map, agent_taxi.loc, p.pick_up)
                return self._move_in_path_and_act(shortest_path, env.Action.PICK_UP)
        return env.Action.STAY    


class Debug(Base):
    """Debug agent that prompts the user for the next action."""

    def __init__(self, agent_id: int = 0) -> None:
        self._prompt = f"Choose agent {agent_id} action [W(Up),S(Down),A(Left),D(Right),Z(Stay),X(Pick),C(Drop)]?"

    def act(self) -> env.Action:
        action = None
        while action is None:
            # Lower to ignore uppercase letters
            action_input = input(self._prompt).lower()
            if action_input in ("w", "up"):
                action = env.Action.UP
            elif action_input in ("s", "down"):
                action = env.Action.DOWN
            elif action_input in ("a", "left"):
                action = env.Action.LEFT
            elif action_input in ("d", "right"):
                action = env.Action.RIGHT
            elif action_input in ("z", "stay"):
                action = env.Action.STAY
            elif action_input in ("x", "pick"):
                action = env.Action.PICK_UP
            elif action_input in ("c", "drop"):
                action = env.Action.DROP_OFF

        return action