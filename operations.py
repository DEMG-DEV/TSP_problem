import numpy as np
import random
import operator
import pandas as pd
import matplotlib.pyplot as plt
from fitness import Fitness


class Operations:
    def __init__(self):
        pass

    def create_route(self, city_list):
        route = random.sample(city_list, len(city_list))
        return route

    def initial_population(self, pop_size, city_list):
        population = []
        for i in range(0, pop_size):
            population.append(self.create_route(city_list))
        return population

    def rank_routes(self, population):
        fitness_results = {}
        for i in range(0, len(population)):
            fitness_results[i] = Fitness(population[i]).route_fitness()
        return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)

    def selection(self, pop_ranked, elite_size):
        selection_results = []
        df = pd.DataFrame(np.array(pop_ranked), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()

        for i in range(0, elite_size):
            selection_results.append(pop_ranked[i][0])
        for i in range(0, len(pop_ranked)-elite_size):
            pick = 100 * random.random()
            for i in range(0, len(pop_ranked)):
                if pick <= df.iat[i, 3]:
                    selection_results.append(pop_ranked[i][0])
                    break
        return selection_results

    def mating_pool(self, population, selection_results):
        mating_pool = []
        for i in range(0, len(selection_results)):
            index = selection_results[i]
            mating_pool.append(population[index])
        return mating_pool

    def breed(self, parent1, parent2):
        child = []
        child_p1 = []
        child_p2 = []

        gene_a = int(random.random() * len(parent1))
        gene_b = int(random.random() * len(parent2))

        start_gene = min(gene_a, gene_b)
        end_gene = max(gene_a, gene_b)

        for i in range(start_gene, end_gene):
            child_p1.append(parent1[i])

        child_p2 = [item for item in parent2 if item not in child_p1]

        child = child_p1+child_p2
        return child

    def breed_population(self, mating_pool, elite_size):
        children = []
        length = len(mating_pool)-elite_size
        pool = random.sample(mating_pool, len(mating_pool))

        for i in range(0, elite_size):
            children.append(mating_pool[i])

        for i in range(0, length):
            child = self.breed(pool[i], pool[len(mating_pool)-i-1])
            children.append(child)
        return children

    def mutate(self, individual, mutation_rate):
        for swapped in range(len(individual)):
            if(random.random() < mutation_rate):
                swap_with = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swap_with]

                individual[swapped] = city2
                individual[swap_with] = city1
        return individual

    def mutate_population(self, population, mutation_rate):
        mutate_pop = []

        for ind in range(0, len(population)):
            mutate_ind = self.mutate(population[ind], mutation_rate)
            mutate_pop.append(mutate_ind)
        return mutate_pop

    def next_generation(self, current_gen, elite_size, mutation_rate):
        pop_ranked = self.rank_routes(current_gen)
        selection_results = self.selection(pop_ranked, elite_size)
        matingpool = self.mating_pool(current_gen, selection_results)
        children = self.breed_population(matingpool, elite_size)
        next_generation = self.mutate_population(children, mutation_rate)
        return next_generation
