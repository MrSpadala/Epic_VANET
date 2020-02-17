
from sim_config import config, load_opt_parameters
from simulator import performSimulations, computeMetrics

city_scenario = {
    "Luxembourg": [
        "time27100Tper1000.txt",
        "time27100Tper50.txt"
    ],
    "Cologne": [
        "time23000Tper1000.txt",
        "time23000Tper50.txt"
    ],
    "NewYork": [
        "Newyork7005.mat",
        "Newyork3005.mat"
    ]
}


for city, scenarios in city_scenario.items():
    for i, scenario in enumerate(scenarios):
        config.scenario = scenario
        config.city_name = city
        load_opt_parameters()
        config.use_CBF = True
        print(f"EXECUTING for {config.scenario}")

        sims = performSimulations(config.nsimulations, verbose=False)
        res = computeMetrics(sims)
        n_cars, sent_msgs, recv_msgs, t_last_infect, cars_infected_ratio, network_traffic = res
        print(n_cars)
        print("sent", sent_msgs)
        print("recv ratio", cars_infected_ratio)
        print("last infect t", t_last_infect)
        print()