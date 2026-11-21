# Smart City AI System
# Genetic Algorithm for Traffic Signal Optimization

import random


# ------------------------------------------
# CONFIGURATION
# ------------------------------------------

POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.2

MIN_GREEN = 10
MAX_GREEN = 40

TOTAL_GREEN_TIME = 100

# Traffic demand for four roads
# North, South, East, West
TRAFFIC_DEMAND = [80, 60, 100, 40]


# ------------------------------------------
# CREATE INITIAL POPULATION
# ------------------------------------------

def create_individual():
    """
    Creates a traffic signal timing configuration.

    Each individual represents green signal duration
    for North, South, East, and West roads.
    """

    timings = [
        random.randint(MIN_GREEN, MAX_GREEN)
        for _ in range(4)
    ]

    return normalize_timings(timings)


def normalize_timings(timings):
    """
    Ensures total green time remains fixed
    and timings remain within valid limits.
    """

    timings = timings.copy()

    while sum(timings) != TOTAL_GREEN_TIME:

        difference = TOTAL_GREEN_TIME - sum(timings)

        index = random.randint(0, 3)

        if difference > 0:

            available = MAX_GREEN - timings[index]

            if available > 0:

                adjustment = min(difference, available)

                timings[index] += adjustment

        else:

            available = timings[index] - MIN_GREEN

            if available > 0:

                adjustment = min(abs(difference), available)

                timings[index] -= adjustment

    return timings


def create_population():
    """
    Generates the initial population
    of possible traffic signal timings.
    """

    return [
        create_individual()
        for _ in range(POPULATION_SIZE)
    ]


# ------------------------------------------
# FITNESS FUNCTION
# ------------------------------------------

def calculate_delay(individual, traffic_demand):
    """
    Calculates estimated traffic delay.
    Lower delay indicates better traffic efficiency.
    """

    total_delay = 0

    for index in range(4):

        demand = traffic_demand[index]

        green_time = individual[index]

        delay = demand * (TOTAL_GREEN_TIME - green_time)

        total_delay += delay

    return total_delay


def calculate_extreme_delay(traffic_demand, maximize_delay):
    """
    Calculates theoretical best and worst delays
    under the green-time constraints.
    """

    timings = [MIN_GREEN] * 4

    remaining_time = TOTAL_GREEN_TIME - sum(timings)

    road_indices = sorted(
        range(4),
        key=lambda index: traffic_demand[index],
        reverse=not maximize_delay
    )

    for index in road_indices:

        available = MAX_GREEN - timings[index]

        allocation = min(
            remaining_time,
            available
        )

        timings[index] += allocation

        remaining_time -= allocation

        if remaining_time == 0:
            break

    return calculate_delay(timings, traffic_demand)


def calculate_fitness(individual, traffic_demand):
    """
    Evaluates traffic signal timing using:
    1. Normalized traffic efficiency
    2. Fairness across roads

    Higher fitness = better solution.
    """

    # --------------------------------
    # 1. Traffic Efficiency
    # --------------------------------

    current_delay = calculate_delay(
        individual,
        traffic_demand
    )

    worst_delay = calculate_extreme_delay(
        traffic_demand,
        maximize_delay=True
    )

    best_delay = calculate_extreme_delay(
        traffic_demand,
        maximize_delay=False
    )

    if worst_delay == best_delay:

        efficiency_score = 1.0

    else:

        efficiency_score = (
            worst_delay - current_delay
        ) / (
            worst_delay - best_delay
        )

    efficiency_score = max(
        0.0,
        min(1.0, efficiency_score)
    )

    # --------------------------------
    # 2. Fairness
    # --------------------------------

    service_ratios = []

    for index in range(4):

        ratio = (
            individual[index]
            / traffic_demand[index]
        )

        service_ratios.append(ratio)

    numerator = sum(service_ratios) ** 2

    denominator = (
        len(service_ratios)
        * sum(ratio ** 2 for ratio in service_ratios)
    )

    fairness_score = numerator / denominator

    # --------------------------------
    # 3. Combined Fitness
    # --------------------------------

    efficiency_weight = 0.7

    fairness_weight = 0.3

    combined_fitness = (
        efficiency_score * efficiency_weight
        + fairness_score * fairness_weight
    )

    return combined_fitness


# ------------------------------------------
# SELECTION
# ------------------------------------------

def selection(population, traffic_demand):
    """
    Selects better individuals using tournament selection.
    """

    tournament = random.sample(population, 3)

    winner = max(
        tournament,
        key=lambda individual: calculate_fitness(
            individual,
            traffic_demand
        )
    )

    return winner


# ------------------------------------------
# CROSSOVER
# ------------------------------------------

def crossover(parent1, parent2):
    """
    Combines two parents to create a new individual.
    """

    child = []

    for index in range(4):

        if random.random() < 0.5:

            child.append(parent1[index])

        else:

            child.append(parent2[index])

    return normalize_timings(child)


# ------------------------------------------
# MUTATION
# ------------------------------------------

def mutation(individual):
    """
    Randomly modifies signal timings
    to explore new solutions.
    """

    individual = individual.copy()

    if random.random() < MUTATION_RATE:

        road1 = random.randint(0, 3)

        road2 = random.randint(0, 3)

        while road1 == road2:

            road2 = random.randint(0, 3)

        adjustment = random.randint(1, 5)

        # Transfer green time between roads
        if individual[road1] + adjustment <= MAX_GREEN:

            if individual[road2] - adjustment >= MIN_GREEN:

                individual[road1] += adjustment

                individual[road2] -= adjustment

    return individual


# ------------------------------------------
# GENETIC ALGORITHM
# ------------------------------------------

def optimize_traffic_signals(traffic_demand):
    """
    Runs the Genetic Algorithm
    to optimize traffic signal timings.
    """

    population = create_population()

    best_solution = None

    best_fitness = 0

    for generation in range(GENERATIONS):

        population = sorted(
            population,
            key=lambda individual: calculate_fitness(
                individual,
                traffic_demand
            ),
            reverse=True
        )

        current_best = population[0]

        current_fitness = calculate_fitness(
            current_best,
            traffic_demand
        )

        if current_fitness > best_fitness:

            best_solution = current_best.copy()

            best_fitness = current_fitness

        new_population = []

        # Elitism: preserve the best solution
        new_population.append(
            population[0].copy()
        )

        while len(new_population) < POPULATION_SIZE:

            parent1 = selection(population, traffic_demand)

            parent2 = selection(population, traffic_demand)

            child = crossover(parent1, parent2)

            child = mutation(child)

            new_population.append(child)

        population = new_population

    return best_solution, best_fitness


# ------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------

if __name__ == "__main__":

    random.seed(42)

    print("=" * 50)

    print("SMART CITY TRAFFIC SIGNAL OPTIMIZATION")

    print("=" * 50)

    print("\nTraffic Demand:")

    print(f"North Road: {TRAFFIC_DEMAND[0]} vehicles")

    print(f"South Road: {TRAFFIC_DEMAND[1]} vehicles")

    print(f"East Road: {TRAFFIC_DEMAND[2]} vehicles")

    print(f"West Road: {TRAFFIC_DEMAND[3]} vehicles")

    print("\nRunning Genetic Algorithm...")

    best_solution, best_fitness = optimize_traffic_signals(
        TRAFFIC_DEMAND
    )

    print("\nOPTIMAL SIGNAL TIMINGS")

    print("-" * 30)

    roads = ["North", "South", "East", "West"]

    for index, road in enumerate(roads):

        print(
            f"{road}: "
            f"{best_solution[index]} seconds green"
        )

    print("\nTotal Green Time:")

    print(f"{sum(best_solution)} seconds")

    print("\nFitness Score:")

    print(f"{best_fitness:.6f}")

    print("\nOptimization completed successfully!")