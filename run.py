import agent
import env
import default
import grid
import graphical
import numpy as np
import pygame
import yaml
import tqdm


from typing import List


def run_graphical(map: grid.Map, agents: List[agent.Base], init_passengers: int, log_level: str):
    with graphical.EnvironmentPrinter(map.grid) as printer:
        environment = env.Environment(
            map=map, init_taxis=len(agents), init_passengers=init_passengers, printer=printer, log_level=log_level,
        )
        # Initial render to see initial environment.
        observations = environment.reset()
        environment.render()
        running = True
        n_steps = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for observations, agent in zip(observations, agents):
                agent.see(observations)

            actions = [a.act() for a in agents]
            observations, terminal = environment.step(*actions)
            n_steps += 1
            environment.render()
            if terminal:
                break

            #time.sleep(1)
    n_delivered = len(environment.final_passengers) - len(environment.passengers)
    return environment.taxis, environment.final_passengers, n_delivered, n_steps


def run_not_graphical(map: grid.Map, agents: List[agent.Base], init_passengers: int, log_level: str):
    environment = env.Environment(
        map=map, init_taxis=len(agents), init_passengers=init_passengers, log_level=log_level,
    )

    observations = environment.reset()
    running = True
    n_steps = 0
    while running:
        
        for observations, agent in zip(observations, agents):
            agent.see(observations)
        
        actions = [a.act() for a in agents]
        observations, terminal = environment.step(*actions)
        n_steps += 1
        if terminal:
            break
        #time.sleep(1)
    n_delivered = len(environment.final_passengers) - len(environment.passengers)
    return environment.taxis, environment.final_passengers, n_delivered, n_steps

def main():


    with open("./config.yml", "r") as fp:
        data = yaml.safe_load(fp)

    num_agents = data[data["agent_type"]]["nr_agents"]
    init_passengers = data[data["agent_type"]]["nr_passengers"]
    
    if data["agent_type"] == "Random":
        agents = [agent.Random() for i in range(num_agents)]
    elif data["agent_type"] == "PathPlanner":
        agents = [agent.PathPlanner(agent_id=i) for i in range(num_agents)]
    elif data["agent_type"] == "QuadrantsSocialConventions":
        agents = [agent.QuadrantsSocialConventions(agent_id=i) for i in range(num_agents)]
    elif data["agent_type"] == "IDsSocialConventions":
        agents = [agent.IDsSocialConventions(agent_id=i) for i in range(num_agents)]
    elif data["agent_type"] == "Roles":
        agents = [agent.Roles(agent_id=i) for i in range(num_agents)]
    elif data["agent_type"] == "Debug":
        agents = [agent.Debug(agent_id=i) for i in range(num_agents)]


    map = grid.Map(default.MAP)

    run_with_graphics = data["graphical"]
    log_level = data["log_level"]
    n_runs = data["n_runs"]

    taxis_distances = []
    pick_up_times = []
    drop_off_times = []
    all_n_delivered = []
    all_n_steps = []

    if run_with_graphics:
        iterable = range(n_runs)
    else:
        iterable = tqdm.tqdm(range(n_runs))
    
    for _ in iterable:
        if run_with_graphics:
            taxis, passengers, n_delivered, n_steps = run_graphical(map, agents, init_passengers, log_level)
        else:
            taxis, passengers, n_delivered, n_steps = run_not_graphical(map, agents, init_passengers, log_level)

        avg_taxi_distance = np.mean([taxi.total_distance for taxi in taxis])
        avg_pick_up = np.mean([p[0] for p in passengers])
        avg_drop_off = np.mean([p[1] for p in passengers])

        taxis_distances.append(avg_taxi_distance)
        pick_up_times.append(avg_pick_up)
        drop_off_times.append(avg_drop_off)
        all_n_delivered.append(n_delivered)
        all_n_steps.append(n_steps)

    # Stores each run in the following format
    # n_agents, n_passengers, avg_taxi_distance, avg_pick_up_time, avg_drop_off_time, avg_n_steps
    with open(f"metrics-{data['agent_type']}-agents-{num_agents}-passengers-{init_passengers}.csv", "w") as metrics:
        metrics.write("taxi_distance,pick_up_time,drop_off_time,n_delivered,n_steps\n")
        for t, p, d, a, n in zip(taxis_distances, pick_up_times, drop_off_times, all_n_delivered, all_n_steps):
            metrics.write(f"{t},{p},{d},{a},{n}\n")



if __name__ == "__main__":
    main()