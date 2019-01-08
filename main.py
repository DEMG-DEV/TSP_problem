import random
import matplotlib.pyplot as plt
from city import City
from operations import Operations


def genetic_algorithm(population, pop_size, elite_size, mutation_rate, generations):
    operation = Operations()
    pop = operation.initial_population(pop_size, population)
    print("Initial distance: " + str(1/operation.rank_routes(pop)[0][1]))
    progress = []
    progress.append(1/operation.rank_routes(pop)[0][1])

    for i in range(0, generations):
        pop = operation.next_generation(pop, elite_size, mutation_rate)
        progress.append(1/operation.rank_routes(pop)[0][1])

    print("Final distance: "+str(1/operation.rank_routes(pop)[0][1]))
    best_route_index = operation.rank_routes(pop)[0][0]
    best_route = pop[best_route_index]
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()
    return best_route


cityList = []
popSize = 100
eliteSize = 20
mutationRate = 0.01
generations = 500

for i in range(0, 25):
    cityList.append(City(x=int(random.random() * 200),
                         y=int(random.random() * 200)))
genetic_algorithm(population=cityList, pop_size=popSize, elite_size=eliteSize,
                  mutation_rate=mutationRate, generations=generations)
