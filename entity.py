import dataclasses
import grid

@dataclasses.dataclass(frozen=True)
class Passenger:
    pick_up: grid.Position
    drop_off: grid.Position

    # Passenger metrics
    pick_up_time: int
    travel_time: int