import agent
import env
import default
import grid
import graphical
import pygame
import time
import yaml


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
    with graphical.EnvironmentPrinter(map.grid) as printer:
        environment = env.Environment(map=map, init_taxis=num_agents, init_passengers=init_passengers, printer=printer)
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


if __name__ == "__main__":
    main()