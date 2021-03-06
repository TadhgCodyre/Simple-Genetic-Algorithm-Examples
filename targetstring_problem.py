# -*- coding: utf-8 -*-
"""TargetString Problem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cI-Gigcr0VLZXCk1d96Rw-3jPOY9ES_4
"""

# Fitness is found by counting the number of 1's present
def fitness(chromosome, target, numberBits):
    count = 0
    for i in range(numberBits):
        # Increment whenever a bit equals the target
        if ((chromosome >> i) & 1) == ((target >> i) & 1):
            count += 1
    return count

# Whenver there is a mutation, simply flip a random bit
def mutate(child, mutateRate, numberBits):
    if rand() < mutateRate:
        index = randint(0, numberBits)
        return (child ^ (1 << index))
    return child

def tournamentSelection(population, scores, numberPop):
    # Pick some random index in population
    bestChrom = randint(0, numberPop)

    # Pick contending chromosomes randomly
    for chromosome in randint(0, numberPop, 4):
        # Find best score in tournament round
        if scores[chromosome] > scores[bestChrom]:
            bestChrom = chromosome
    return population[bestChrom]

# Crossover between two parents to create two children
def crossover(p1, p2, crossRate, numberBits):
    # Children are the same as their parents
    c1, c2 = p1, p2

    # Randomly decide if crossover happens based on the rate of crossover
    if rand() < crossRate:
        # i decides where crosover happens between parents
        i = randint(1, numberBits-1)

        # front_mask gets the first i bits of binary
        # back_mask gets the rest of the bits
        firstBits = ((1 << i) - 1) << (numberBits - i)
        restBits = (1 << (numberBits - i)) - 1

        # child_1 is the first i bits of parent_1. The rest are from parent_2
        c1 = (p1 & firstBits) | (p2 & restBits)

        # child_2 is the first i bits of parent_2. The rest are from parent_1
        c2 = (p2 & firstBits) | (p1 & restBits)

    return c1, c2

def geneticAlgorithm(population, averages, numberBits, numberIter, numberPop, crossRate, mutateRate, target):
    # Cycle through generations
    for gen in range(numberIter):
        p = []
        c = []

        # Calculate all fitness scores for population
        scores = [fitness(n, target, numberBits) for n in population]

        averages.append(statistics.mean(scores))

        # Print scores of current generation
        bestIndex, bestScore = scores.index(max(scores)), max(scores)
        print(f'GENERATION {gen+1}')
        print(f'BEST ITEM: {population[bestIndex]:030b}')
        print(f'ITEM SCORE: {bestScore}')
        print(f'AVERAGE SCORE: {averages[gen]}\n')

        # Find parent chromosomes of next generation via selection
        for i in range(numberPop):
            p.append(tournamentSelection(population, scores, numberPop))

        # Pair up chromosome with the one right after it
        for i in range(0, numberPop, 2):
            parent1, parent2 = p[i], p[i+1]

            # Perform crossover, mutate children and append to list
            for child in crossover(parent1, parent2, crossRate, numberBits):
                child = mutate(child, mutateRate, numberBits)
                c.append(child)

        # Replace current generation with children
        population = c

def plot_averages(averages, totalIter):
    plt.plot(range(1, totalIter+1), averages)
    plt.title(f'Average fitness for {totalIter} '
              'generations (Target String)')
    plt.xlabel('Generation')
    plt.ylabel('Average fitness')
    plt.show()

import statistics
import matplotlib.pyplot as plt
from numpy.random import randint, rand

def main():
    # number of iterations
    numberIter = 10

    # number of bits
    numberBits = 30

    # population
    numberPop = 100

    # crossover rate
    crossRate = 0.9
    
    # mutation rate
    mutateRate = 1.0 / float(numberBits)

    # List tracking the average fitness of each generation
    averages = []

    # Max value of a bit string in the population
    maxValue = (1 << numberBits) - 1

    # Create a random bit string as target
    target = randint(0, maxValue)

    # Array to hold the population
    population = []

    print(f'Target string is: {target:030b}\n')

    # Target of GA is a 30 bit string of 1s
    print(f'Max Value is: {maxValue:030b}\n')

    # Generate initial generation of chromosomes
    for i in range(0, numberPop):
        population.append(randint(0, maxValue+1))

    geneticAlgorithm(population, averages, numberBits, numberIter, numberPop, crossRate, mutateRate, target)
    plot_averages(averages, numberIter)

if __name__ == '__main__':
    main()