import agent
import env
import default
import grid
import graphical
import pygame
import yaml

from typing import List


def run_graphical(map: grid.Map, agents: List[agent.Base], init_passengers: int):
    with graphical.EnvironmentPrinter(map.grid) as printer:
        environment = env.Environment(map=map, init_taxis=len(agents), init_passengers=init_passengers, printer=printer)
        # Initial render to see initial environment.
        environment.render()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            actions = [a.act() for a in agents]
            environment.step(*actions)
            environment.render()
            #time.sleep(1)

def run_not_graphical(map: grid.Map, agents: List[agent.Base], init_passengers: int):
    environment = env.Environment(map=map, init_taxis=len(agents), init_passengers=init_passengers)

    running = True
    while running:
        actions = [a.act() for a in agents]
        environment.step(*actions)
        #time.sleep(1)

def main():

    with open("./config.yml", "r") as fp:
        data = yaml.safe_load(fp)

    num_agents = data[data["agent_type"]]["nr_agents"]
    init_passengers = data[data["agent_type"]]["nr_passengers"]
    
    if data["agent_type"] == "Random":
        agents = [agent.Random() for i in range(num_agents)]
    elif data["agent_type"] == "Deliberative":
        agents = None
        #agents = [agent.Deliberative(agent_id=i) for i in range(num_agents)]
    elif data["agent_type"] == "Greedy":
        agents = None
        #agents = [agent.Greedy() for i in range(num_agents)]
    elif data["agent_type"] == "Debug":
        agents = [agent.Debug(agent_id=i) for i in range(num_agents)]

    map = grid.Map(default.MAP)

    run_with_graphics = data["graphical"]
    if run_with_graphics:
        run_graphical(map, agents, init_passengers)
    else:
        run_not_graphical(map, agents, init_passengers)


if __name__ == "__main__":
    main()