import numpy as np

from typing import List, Optional, Tuple

Colour = Tuple[int, int, int]

ROADS: List[Colour] = [(58, 68, 102), (38, 43, 68)]
SIDEWALKS: List[Colour] = [(228, 166, 114), (216, 118, 68), (190, 74, 47)]
TAXI: List[Colour] = [(254, 231, 97)]

class Picker:
    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = np.random.default_rng(seed)
        self._choices = np.arange(256)

    def random_not_close(self, *not_close: Colour):
        colour = self._unchecked_random()
        not_close = list(not_close)
        checked = False
        while not checked:
            found_close = False
            for c in not_close:
                if are_similar(colour, c):
                    found_close = True
                    break
            if found_close:
                colour = self._unchecked_random()
                found_close = False
            else:
                checked = True
        return colour

    def _unchecked_random(self):
        return tuple(self._rng.choice(self._choices, size=3))


def are_similar(a: Colour, b: Colour, tol: int = 50) -> bool:
    """Verifies if two colours are similar."""
    a = np.array(a)
    b = np.array(b)
    return np.all(np.abs(a - b) <= tol)
