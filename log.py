import env
import entity
import logging

logging.basicConfig(format="t = %(timestep)s \t %(levelname)s \t %(name)s \t %(message)s")

def new(name: str, lvl: str = "info") -> logging.Logger:
    logger = logging.getLogger(name=name)
    lvl = getattr(logging, lvl.upper(), None)
    if not isinstance(lvl, int):
        raise ValueError(f"Invalid log level: {lvl}")
    logger.setLevel(lvl)
    return logger

def create_taxi(logger: logging.Logger, t: int, taxi: entity.Taxi):
    logger.info("Created %r", taxi, extra={"timestep": t})

def create_passenger(logger: logging.Logger, t: int, passenger: entity.Passenger):
    logger.info("Created %r", passenger, extra={"timestep": t})

def choosen_action(logger: logging.Logger, t: int, agent: int, action: "env.Action"):
    logger.info("Agent %d wants to %r", agent, action, extra={"timestep": t})

def taxi(logger: logging.Logger, t: int, taxi: entity.Taxi):
    logger.info("Taxi %r", taxi, extra={"timestep": t})

def passenger(logger: logging.Logger, t: int, passenger: entity.Passenger):
    logger.info("Passenger %r", passenger, extra={"timestep": t})