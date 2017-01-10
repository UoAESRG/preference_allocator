# preference_allocator
A simple script for allocating projects to groups of students based on entered preferences. This script currently generates a random set of preferences, and then passes it through three approaches:

## Random Selection
1. Generate a random, valid solution (based on the preferences to improve the likelihood of a good solution being found).
2. If this solution is better than the current best solution, save it. Otherwise, throw it away.
3. Repeat.

## Hill Climbing
1. Generate a random, valid solution (based on the preferences to improve the likelihood of a good solution being found).
2. Save this as the current best solution.
3. Mutate the solution slightly by changing a random project allocation to another preference.
4. Check if this is better than the current best solution. If so, save it. Otherwise, throw it away.
5. Repeat from step 3 onwards.

## Genetic Algorithm
1. Generate a population of random, valid solutions (but without looking at the preferences).
2. Rank these solutions based on their costs.
3. Save the best x solutions, and throw away the rest.
4. Generate mutations of the best solutions to create a new population.
5. Repeat from step 2 onwards.

Valid solutions are ones where all groups are allocated a project with no duplicates (i.e. no projects are allocated more than once).

# Important Parameters
* numprojects = Total number of projects available
* numgroups = Total number of groups needing projects
* numprefs = Number of preferences expressed by each group
* testiterations = Maximum number of iterations before each method should stop and present the best solution found so far
* minimabreak = When the hill climbing and genetic algorithm approaches should stop if they are not making much progress (i.e. they are already in a minima and the solution isn't likely to get much better). Expressed as a percentage of testiterations, so a larger minimabreak means that the algorithms should try for longer.
