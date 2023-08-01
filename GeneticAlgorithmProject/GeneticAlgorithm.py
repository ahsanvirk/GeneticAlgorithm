from collections import namedtuple
from random import choices, randint, randrange, random
from typing import List, Callable, Tuple

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
Item = namedtuple('Item', ['name', 'value', 'weight'])

items = [
    Item('Sleeping Bag', 15, 15),
    Item('Rope', 7, 3),
    Item('Pocket Knife', 10, 2),
    Item('Flashlight', 5, 5),
    Item('Bottle', 8, 9),
    Item('Sugar Candy', 10, 2),
    Item('Pistol Crossbow', 13, 8),
    Item('Compass', 9, 2),
    Item('Solar Powered Radio', 15, 12),
    Item('Backpack', 14, 9)
    ]


def generate_genome(length: int) -> Genome:
    return choices([0,1], k=length)

def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def fitness(genome: Genome, items: [Item], weight_limit: int) -> int:
    if len(genome) != len(items):
        raise ValueError("genome and items must be of the same length")

    weight = 0

    value = 0

    for i, item in enumerate(items):
        if genome[i] == 1:
            weight += item.weight
            value += item.value

            if weight > weight_limit:
                return 0


    return value


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
        return choices(
            population=population,
            weights=[fitness_func(genome) for genome in population],
            k = 2
        )

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be the same length")

    length = len(a)
    if length < 2:
        return a, b

    p = randint(1, length -1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = randrange(len(genome))
        genome[index] = genome[index] if random() > probability else abs(genome[index] - 1)
    return genome

def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100
    ) -> Tuple[Population, int]:
        population = populate_func()

        for i in range(generation_limit):
            population = sorted(
                population,
                key=lambda genome: fitness_func(genome),
                reverse=True
            )

            if fitness_func(population[0]) >= fitness_limit:
                break

            next_generation = population[0:2]#4

            for j in range(int(len(population) / 2) -1):
                parents = selection_func(population, fitness_func)
                offspring_a, offspring_b = crossover_func(parents[0], parents[1])
                offspring_a = mutation_func(offspring_a)
                offspring_b = mutation_func(offspring_b)
                next_generation += [offspring_a, offspring_b]

            population = next_generation


        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

        return population, i

population, generations = run_evolution(

    populate_func=partial(
        generate_population, size=10, genome_length=len(items)
    ),
    fitness_func=partial(
        fitness, items=items, weight_limit=30
    ),
    fitness_limit = 1000,
    generation_limit=100

    )

#def genome_to_items(genome: Genome, items: [Item]) -> [Item]:
 #   result = []
  #  for i, item in enumerate(items):
   #     if genome[i] == 1:
    #        result += [item.name]

    #return result


print(f"number of generations: {generations}")
#print(f"best solution: {genome_to_items(population[0], items)}")
