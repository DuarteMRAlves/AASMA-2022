import agent
import env
import default
import grid
import graphical
import time

def main():
    map = grid.Map(default.MAP)
    num_agents = 4
    agents = [agent.Random() for _ in range(num_agents)]
    with graphical.EnvironmentPrinter(map.grid) as printer:
        environment = env.Environment(map=map, init_taxis=num_agents, init_passengers=4, printer=printer)
        for _ in range(100000000):
            actions = [a.act() for a in agents]
            environment.step(*actions)
            environment.render()
            time.sleep(1)


if __name__ == "__main__":
    main()