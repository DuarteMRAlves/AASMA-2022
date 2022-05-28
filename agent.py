import abc
import env
import numpy as np

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
