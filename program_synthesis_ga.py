import random

MAX_GENERATIONS = 1
POPULATION_SIZE = 10
LOGGING = True

def genetic_programming(inductive_examples):
    # Initialize the population with random individuals
    population = initialize_population()

    # Set the maximum number of generations the algorithm will run
    generations = MAX_GENERATIONS

    # Evaluate the fitness of the initial population
    fitness_values = evaluate_fitness(population, inductive_examples)

    # Iterate through each generation
    for generation in range(generations):
        # Evaluate the fitness of each individual in the population based on the inductive examples
        fitness_values = evaluate_fitness(population, inductive_examples)

        # Initialize an empty new population that will be filled with offspring
        new_population = []

        # Continue creating offspring until the new population reaches the desired size
        while len(new_population) < POPULATION_SIZE:
            # Select two parents based on their fitness values (e.g., using roulette wheel or tournament selection)
            parent1, parent2 = select_parents(population, fitness_values)

            # Perform crossover (recombination) on the selected parents to create two children
            child1, child2 = crossover(parent1, parent2)

            # Mutate the children with a certain probability, introducing small random changes
            child1 = mutate(child1)
            child2 = mutate(child2)

            # Add the children to the new population
            new_population.append(child1)
            new_population.append(child2)

        # Replace the old population with the new population for the next generation
        population = new_population

    # Select the best solution from the final population based on fitness values
    best_solution = select_best_solution(population, fitness_values)

    # Return the best solution found
    return best_solution

def initialize_population():
    # Create an initial population of random programs
    
    # Define the length of each program (this would depend on your problem)
    PROGRAM_LENGTH = 10

    # Define the set of possible characters or tokens in a program (adapt to your problem)
    TOKENS = ['+', '-', '*', '/', '0', '1', '2', '3', '4', '5', 'x']

    # Create the initial population
    population = []
    for _ in range(POPULATION_SIZE):
        program = ''.join(random.choice(TOKENS) for _ in range(PROGRAM_LENGTH))
        population.append(program)

    if LOGGING: 
        print("Population: ", population)

    return population

def evaluate_fitness(population, examples):
    # Evaluate the fitness of each program in the population based on the provided examples
    fitness_values = []

    for program_code in population:
        fitness = 0

        # Iterate through the examples and evaluate how well the program performs
        for example_input, expected_output in examples:
            try:
                # Construct the code to evaluate, including the input
                code_to_execute = program_code.format(input=example_input)

                # Use eval to execute the code
                program_output = eval(code_to_execute)

                # Compare the program's output with the expected output
                if program_output == expected_output:
                    fitness += 1  # Increment fitness for correct output

            except Exception as e:
                # Handle any errors in execution (e.g., syntax errors in the program)
                print(f"Error executing program: {e}")

        # Normalize fitness by the number of examples
        fitness /= len(examples)

        # Append the fitness value to the list
        fitness_values.append(fitness)

    if LOGGING:
        print("Fitness values: ", fitness_values)

    return fitness_values

def select_parents(population, fitness_values):
    # Calculate the total fitness
    total_fitness = sum(fitness_values)

    # Check if total_fitness is zero
    if total_fitness == 0:
        # Handle the special case, e.g., by selecting two random parents
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        if LOGGING:
            print("Parent 1: ", parent1, " Parent 2: ", parent2)

        return parent1, parent2

    # Otherwise, proceed with roulette wheel selection
    normalized_fitness = [fitness / total_fitness for fitness in fitness_values]
    parent1_index = select_roulette(normalized_fitness)
    parent1 = population[parent1_index]
    parent2_index = select_roulette(normalized_fitness)
    parent2 = population[parent2_index]

    if LOGGING:
        print("Parent 1: ", parent1, " Parent 2: ", parent2)

    return parent1, parent2

def select_roulette(normalized_fitness):
    # Generate a random number in [0, 1)
    rand_num = random.random()

    # Find the index corresponding to the random number
    cumulative_prob = 0
    for index, fitness in enumerate(normalized_fitness):
        cumulative_prob += fitness
        if rand_num < cumulative_prob:
            return index

    # In case of numerical issues, return the last index
    return len(normalized_fitness) - 1

def crossover(parent1, parent2):
    # Perform one-point crossover between two parents to produce two children.
    # One-point crossover involves selecting a random point within the program's structure
    # and swapping all the elements after that point between the two parents.

    # Determine a random crossover point
    crossover_point = random.randint(1, len(parent1) - 1)

    # Create the first child by combining the segments before and after the crossover point
    child1 = parent1[:crossover_point] + parent2[crossover_point:]

    # Create the second child by combining the segments in the opposite order
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    if LOGGING:
        print("Child 1: ", child1, " Child 2: ", child2)

    return child1, child2

def mutate(child):
    # Define the mutation rate (probability of mutation occurring)
    MUTATION_RATE = 0.01

    # Define the set of possible characters or tokens in a program (adapt to your problem)
    TOKENS = ['+', '-', '*', '/', '0', '1', '2', '3', '4', '5', 'x']

    # Convert the child to a list for easier manipulation (if it's a string)
    child_list = list(child)

    # Iterate through each element in the child
    for i in range(len(child_list)):
        # Check if a mutation should occur
        if random.random() < MUTATION_RATE:
            # Select a random token from the set
            new_token = random.choice(TOKENS)

            # Replace the current element with the new token
            child_list[i] = new_token

    # Convert the child back to its original representation (if it was a string)
    mutated_child = ''.join(child_list)

    if LOGGING:
        print("Mutated child: ", mutated_child)

    return mutated_child

def select_best_solution(population, fitness_values):
    # Select the best solution from the population based on fitness values
    pass

def main():
    inductive_examples = [
        (1, 1),  # x = 1, y = 1
        (2, 4),  # x = 2, y = 4
        (3, 9),  # x = 3, y = 9
        (4, 16), # x = 4, y = 16
        (5, 25)  # x = 5, y = 25
    ]

    best_solution = genetic_programming(inductive_examples)
    print("Best solution found:", best_solution)

if __name__ == "__main__":
    main()