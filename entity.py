import dataclasses
import enum
import grid




class TripState(enum.Enum):
    WAITING = 0
    INTRIP = 1
    FINISHED = 2

    def __repr__(self) -> str:
        return f"TripState({self.name})"


@dataclasses.dataclass
class Passenger:
    pick_up: grid.Position
    drop_off: grid.Position
    in_trip : TripState = TripState.WAITING
    
    # Passenger metrics
    pick_up_time: int = 0
    travel_time: int = 0


class Direction(enum.Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __repr__(self) -> str:
        return f"Direction({self.name})"

@dataclasses.dataclass
class Taxi:
    loc: grid.Position
    direction: Direction 
    #has_passenger: bool = False
    has_passenger: Passenger = None
        
    def pickup_up(self, passengers: list, env_grid: grid.Map):
        """
        Picks-Up Passenger from a location if near him
        """
        passenger = env_grid.choose_adj_passenger(self.loc, passengers, TripState)
        if passenger != None and self.has_passenger == None:
            passenger.in_trip = TripState.INTRIP
            self.has_passenger = passenger
            return passenger
            
        return None


    def drop_off(self, env_grid: grid.Map):
        """
        Drops-Off Passenger in a nearby sidewalk if near one
        """
        
        if self.has_passenger != None:
            drop_off = env_grid.choose_drop_location(self.loc)

            if drop_off != self.has_passenger.drop_off:
                self.has_passenger.in_trip = TripState.WAITING

            else:
                self.has_passenger.in_trip = TripState.FINISHED
            
            self.has_passenger.pick_up = drop_off

        return None