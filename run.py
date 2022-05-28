import agent
import env
import default
import grid
import graphical
import pygame
import time

def main():
    map = grid.Map(default.MAP)
    num_agents = 1
    agents = [agent.Debug(agent_id=i) for i in range(num_agents)]
    with graphical.EnvironmentPrinter(map.grid) as printer:
        environment = env.Environment(map=map, init_taxis=num_agents, init_passengers=4, printer=printer)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            actions = [a.act() for a in agents]
            environment.step(*actions)
            environment.render()
            time.sleep(1)


if __name__ == "__main__":
    main()