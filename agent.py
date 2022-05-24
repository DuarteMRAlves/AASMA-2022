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
            env.Action.MOVE,
            env.Action.ROT_R,
            env.Action.ROT_L,
            env.Action.STAY,
            env.Action.PICK_UP,
            env.Action.DROP_OFF,
        ]

    def act(self) -> env.Action:
        return self._rng.choice(self._actions)

def bfs_with_positions(
    map: grid.Map, source: grid.Position, target: grid.Position,
) -> List[grid.Position]:
    """Computes the list of positions in the path from source to target.
    
    It uses a BFS so the path is the shortest path."""
    queue = [(source, None)]
    while len(queue) > 0:
        curr, parent = queue.pop(0)
        if curr == target:
            path = [curr]
            while parent is not None:
                parent_position, parent_parent = parent
                path.append(parent_position)
                parent = parent_parent
            return path.reverse()
        for neighbour in curr.adj:
            if neighbour != parent and map.is_road(neighbour):
                queue.extend((neighbour, curr))
    raise ValueError("No path found")