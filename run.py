import env
import default
import grid
import graphical
import time

def main():
    map = grid.Map(default.MAP)
    with graphical.EnvironmentPrinter() as printer:
        environment = env.Environment(map=map, init_taxis=4, init_passengers=4, printer=printer)
        for _ in range(100000000):
            environment.render()
            time.sleep(1)


if __name__ == "__main__":
    main()