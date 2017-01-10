#Some inspiration drawn from Programming Collective Intelligence by Toby Segaran, Chapter 5 (O'Reilly, 2007)
import random
import math
import time
from copy import deepcopy

numprojects = 100
numgroups = 60
numprefs = 5

print "There are " + str(numgroups) + " groups selecting from " + str(numprojects) + " projects."
totalsearchspace = math.factorial(numprojects)/(math.factorial(numgroups)*math.factorial(numprojects-numgroups))
print "The total number of combinations is: " + str(totalsearchspace)
testiterations = 1000
print "The number of test iterations for each method is: " + str(testiterations)
minimabreak = 0.1 #Define when certain methods should stop trying if there is little to no improvement

#Generate some random preferences for now (replace with read from CSV eventually)
def generateprefs():
    prefs = []
    for i in range(numgroups):
        vec = [i for i in range(numprojects)]
        random.shuffle(vec)
        prefs.append(tuple(vec[:5])) #Five preferences 
    return prefs

#Print out the solution (replace with write to CSV eventually)
def printsolution(vec):
    for idx, i in enumerate(vec):
        print 'G'+str(idx), 'P'+str(i)

#Define a simple cost function so there is a target for optimisation        
def cost_function(vec):
    cost = 0

    for idx, i in enumerate(vec):
        pref = prefs[idx]
        
        cost_added = False
        for r in range(5):
            if pref[r] == i:
                cost += r #1 for 1st pref, 2 for 2nd pref, etc.
                cost_added = True
        if not cost_added:
            cost += 20 #Heavy penalty if project is none of the preferences
            
    return cost

#Generate random (but valid) vector    
def gen_vec(prefs):
    """
    #Create random solution where each project is only allocated once
    vec=[i for i in range(numprojects)]
    random.shuffle(vec)
    vec = vec[:numgroups]
    
    #Create random solution where project is drawn from preferences
    vec = []
    for pref in prefs:
        alloc = pref[random.randint(0,4)] #Select a random preference
        vec += [alloc]
    """

    #Create random solution where project is drawn from preferences, and each project is only allocated once
    vec = []
    for pref in prefs:
        alloc = pref[random.randint(0,2)] #Select a random preference from first three
        alloc_count = 0
        alloc_valid = True
        while alloc in vec:
            alloc = pref[alloc_count] #Try giving them their highest preferences first
            alloc_count += 1
            if alloc_count > numprefs-1: 
                alloc_valid = False
                break        
        vec += [alloc]    
    return vec, alloc_valid
    
#Mutation Operation
def mutate(v_in, prefs):
    i = random.randint(0, len(prefs)-1) #Select a random group
    #Identify the projects in their preferences that haven't been selected yet
    choices = list(set(prefs[i]) - set(v_in)) #Also removes the current allocation! Bonus!
    #Replace their current allocation with a random one if possible
    if choices != []:
        v_in[i] = choices[random.randint(0,len(choices)-1)]
    #Otherwise don't bother with replacing anything
    return v_in    
    
def random_allocate(costf, prefs, iterations):
    best = numgroups*20 #Maximum possible cost
    bestvec = None
    for i in range(iterations):
      
        vec, alloc_valid = gen_vec(prefs)
        
        if not alloc_valid: continue #Skip this iteration
        
        cost = costf(vec)
        
        if cost < best:
            best = cost
            bestvec = vec
        if cost == 0: break
    
    print "Final number of iterations: " + str(i+1)
    return bestvec

#Strictly speaking, this is not straight hill climbing because one of the variables is nominal
def hillclimbing(costf, prefs, iterations):
    best = numgroups*20 #Maximum possible cost
    bestvec = None
    
    vec, alloc_valid = gen_vec(prefs)
    
    #if not alloc_valid: return [-1]*len(prefs)
    while not alloc_valid: vec, alloc_valid = gen_vec(prefs)
    
    minimacount = 0
    #There is no "neighbouring" solution because the projects are nominal, not ordinal
    #So use mutation from genetic algorithm instead!
    bestvec = deepcopy(vec)
    for i in range(iterations):        
        vec = deepcopy(bestvec)
        vec = mutate(vec, prefs)
        cost = costf(vec)      
        minimacount += 1

        if cost < best:
            best = deepcopy(cost)
            bestvec = deepcopy(vec)
            minimacount = 0
            
        if minimacount > iterations*minimabreak: break #If stuck in same minima for awhile, just stop
        if cost == 0: break
    
    print "Final number of iterations: " + str(i+1)
    return bestvec
        
def geneticoptimise(costf, prefs, popsize=50, elite=0.2, maxiter=100):           
    #Build the initial (random) population, doesn't have to be initially valid
    pop = []
    for i in range(popsize):
        #Each project can only be allocated once!
        vec=[i for i in range(numprojects)]
        random.shuffle(vec)
        pop.append(vec[:numgroups])

    #Build in memory for best iteration seen so far
    best_pop = []
    best_score = numgroups*20 #Maximum possible score
    elite_num = int(popsize*elite)
    
    minimacount = 0
    #Main loop
    for i in range(maxiter):
        scores=[(costf(v),v) for v in pop]
        scores.sort()
        ranked=[v for (s, v) in scores]
        minimacount += 1
        
        if scores[0][0] < best_score:
            best_pop = deepcopy(scores)
            best_score = deepcopy(scores[0][0])
            minimacount = 0
            
        #Check if "optimal" solution has been found
        if all(x == scores[0] for x in scores) or best_score == 0:
            break
            
        if minimacount > maxiter*minimabreak: break #If no better solutions have been found for awhile, just stop
        
        #Start with the pure winners
        pop=ranked[0:elite_num]

        #Add mutated forms of the winners
        #Using mutation only, because breeding/crossover doesn't make sense for nominal variables without replacement
        while len(pop)<popsize:
            #Mutation 
            c = random.randint(0,elite_num)
            pop.append(deepcopy(mutate(ranked[c], prefs))) #For some reason not using deepcopy replaces all elements with the appended object
            
    print "Final number of iterations: " + str(i+1)
    return best_pop[0][1]

prefs = generateprefs()

#Random, just drops and finds a new valid solution and checks it
print "---------------------"
t0 = time.time()
s = random_allocate(cost_function, prefs, testiterations)
t1 = time.time()
print "Final cost (random): " + str(cost_function(s))
print "Time taken (random): " + str(t1-t0)
#printsolution(s)

#Hill climbing, faster than random because it's faster to mutate than to search for new valid solution
print "---------------------"
t0 = time.time()
s = hillclimbing(cost_function, prefs, testiterations)
t1 = time.time()
print "Final cost (hillclimb): " + str(cost_function(s))
print "Time taken (hillclimb): " + str(t1-t0)
#printsolution(s)

#Genetic algorithm (with mutation only, no breeding), takes about 50x longer but lowest cost
print "---------------------"
t0 = time.time()
s = geneticoptimise(cost_function, prefs, popsize=numgroups, maxiter=testiterations/1)
t1 = time.time()
print "Final cost (genetic): " + str(cost_function(s))
print "Time taken (genetic): " + str(t1-t0)
printsolution(s)