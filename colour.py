import numpy as np

from typing import List, Optional, Tuple

Colour = Tuple[int, int, int]

ROAD: Colour = (75, 75, 75)
SIDEWALK: Colour = (50, 100, 50)

class Picker:
    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = np.random.default_rng(seed)
        self._choices = np.arange(256)

    def random(self, not_close: Optional[List[Colour]] = None):
        colour = self._unchecked_random()
        if not_close is not None:
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


def are_similar(a: Colour, b: Colour, tol: int = 20) -> bool:
    """Verifies if two colours are similar."""
    return np.allclose(a, b, atol=tol)
