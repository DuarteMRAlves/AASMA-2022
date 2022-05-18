import abc
import grid


class Environment:

    def __init__(self, map: grid.Map, printer: "Printer"):
        self.map = map
        self.__printer = printer

    def render(self):
        self.__printer.print(self)

class Printer(abc.ABC):
    @abc.abstractmethod
    def print(self, env: Environment):
        pass