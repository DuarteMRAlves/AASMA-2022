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


class PathPlanner(Base):
    """Agent that plans its path using a BFS."""

    def __init__(self, agent_id: int = 0) -> None:
        super().__init__()
        self._agent_id = agent_id

    def act(self) -> env.Action:
        map = self._last_observation.map
        agent_taxi = self._last_observation.taxis[self._agent_id]
        passengers = self._last_observation.passengers
        
        if agent_taxi.has_passenger is None:
            return self._pickup_nearest_passenger(map, agent_taxi, passengers)
        return self._dropoff_current_passenger(map, agent_taxi)
            
    def _pickup_nearest_passenger(
        self, map: grid.Map, agent_taxi: entity.Taxi, passengers: List[entity.Passenger],
    ) -> env.Action:
        possible_passengers = [p for p in passengers if p.in_trip == entity.TripState.WAITING]
        if len(possible_passengers) == 0:
            return env.Action.STAY

        shortest_paths = [
            bfs_with_positions(map, agent_taxi.loc, p.pick_up) 
            for p in possible_passengers
        ]
        path_idx = np.argmin([len(p) for p in shortest_paths])
        return self._move_in_path_and_act(shortest_paths[path_idx], env.Action.PICK_UP)

    def _dropoff_current_passenger(self, map: grid.Map, agent_taxi: entity.Taxi) -> env.Action:
        passenger = agent_taxi.has_passenger
        shortest_path = bfs_with_positions(map, agent_taxi.loc, passenger.drop_off)
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


def bfs_with_positions(
    map: grid.Map, source: grid.Position, target: grid.Position,
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