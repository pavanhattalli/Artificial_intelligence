
import random
import math
import itertools,time
from itertools import combinations
import pandas as pd

#----------------------------------------------------------------------------------------------------------

list_of_dimensions = []                                                                  # Global variables
covered_pairs = []

#----------------------------------------------------------------------------------------------------------

def form_pairs(l,ele):                                                                      # Forming Pairs
    pairs = []
    for i in l:
        for j in l:
            
            pairs.append([ele,i,j])
    return pairs

#----------------------------------------------------------------------------------------

def generate_pairs(l):                                                      # Generating all possible pairs
    
    all_pairs = []
    counter1 = 1
    for i in l:
        temp_list = []
        
        for j in range(i):
            temp_list.append(counter1)
            counter1 = counter1 + 1
        list_of_dimensions.append(temp_list)
        
    for i in range(len(l)):
        
        temp_list2 = []
        counter2 = 0
        
        for j in range(i+1,len(l)):
            temp_list2 = temp_list2 + list_of_dimensions[j]  
        
        for k in range(len(list_of_dimensions[i])):
            temp_list3 = []
            temp_list3 = temp_list3 + temp_list2
            all_pairs = all_pairs + form_pairs(temp_list3,list_of_dimensions[i][k])

    return all_pairs

#----------------------------------------------------------------------------------------------------------    
       
def generate_random_particles(num_of_particles,size_of_each_dimension):       # Generating random particles
    
    particle_list = []
    tp = []
    
    for i in range(num_of_particles):
        tp1 = []
        temp_list = []
        for j in range(len(size_of_each_dimension)):
            temp_variable = random.randint(0,size_of_each_dimension[j]-1)
            temp_list.append(list_of_dimensions[j][temp_variable])
            tp1.append(temp_variable)
        particle_list.append(temp_list)
        tp.append(tp1)
#     print(tp)
    return particle_list,tp

#----------------------------------------------------------------------------------------------------------

def assign_random_position(size_of_each_dimension):
    maxValue = max(size_of_each_dimension)
    intial_pos = []
    
    for i in range(len(size_of_each_dimension)):
        temp_variable = random.randint(0,maxValue-1)
        intial_pos.append(temp_variable)

#------------------------------------------------------------------------------------------------------------

flag = int(input("Enter 1 for default test case or press any other key for custom input: "))
if flag == 1:
    no_of_dimensions = 10
    size_of_each_dimension = [15,15,15,15,15,15,15,15,15,15]
    no_of_particles = 2
else:
    no_of_dimensions = int(input('Enter Number of Dimensions : '))
    size_of_each_dimension = [int(x) for x in input('Enter Size of Each Dimension : ').split()]
    #no_of_particles = int(input("Enter number of particles : "))


#no_of_iter = int(input("Enter the number of iterations : "))    
    
pairs = generate_pairs(size_of_each_dimension)
#while(pairs):
    #if(pairs present in pso == pairs generated in sa ):
        #pso(pair[]).pop
        
    
particle_list,particle_pos = generate_random_particles(no_of_particles,size_of_each_dimension)


total_pairs = len(pairs)
print("\nTotal pairs : {} \nPairs :- {}".format(total_pairs,pairs))
print("\nparticle list is -----> ",particle_list)


ideal = (no_of_dimensions) * (no_of_dimensions - 1) // 2
    
print("\nIdeally any configuration should cover --> {} pairs".format(ideal))   


# Temperature and Cooling Factor

T = 200
cf = 0.99842
print("\n\tTemperature :- {} \n\tCooling factor :- {}".format(T,cf))

ch = int(input("\nDo you want to change these parameters ? Enter 1 for Yes..!! :- "))
if ch == 1:
	T = int(input("Enter starting temperature (T) :- "))
	cf = float(input("Enter Cooling Factor (cf) :- "))


def unique_pairs(values_list,pairs_in_while):
    
    uniq_p = 0
    temp_pairs = []
    for comb in combinations(values_list, 2):
        temp_pairs.append(list(comb))
    
    for i in range(len(temp_pairs)):
        if (not temp_pairs[i] in pairs_in_while) and temp_pairs[i] in pairs:
            uniq_p += 1
            pairs_in_while.append(temp_pairs[i])
        else:
            print("this pair is repeated ",temp_pairs[i])
            pass
            
    return uniq_p,pairs_in_while
    
    
# ------------------------------------------------------------------------------------------------

selected_conf = []
count = 1
overall_prob = []
overall_prob_dash = []
overall_un_pair = []
overall_temp = []
#print("no of iterations are :- ",no_of_iter)
while T > 0.000001 and len(pairs) > 0: 
#and no_of_iter > 0:
    
    print("\n\n*********** Iteration no. {} ************".format(count))
    count += 1
    #no_of_iter -= 1
    print("\nT is now --> ",T)
    pairs_in_while = []
    
    select_iter = []
    prob = []
    prob_dash = []
    un_pair_list = []
    temperature = []
    for i in range(len(particle_list)):
        uniq_p,pairs_in_while = unique_pairs(particle_list[i],pairs_in_while)
        
        print("\nparticle {} is generating {} unique pairs ".format(particle_list[i],uniq_p))
        if uniq_p == ideal:
            select_iter.append(particle_list[i])
            prob.append(0)
            temperature.append(T)
            prob_dash.append(0)
            un_pair_list.append(uniq_p)
        elif uniq_p > (ideal // 3):
            diff = ideal - uniq_p
            p = math.exp(-(diff)/T)
            p_dash = random.uniform(0,1)
            if p_dash < p:
                select_iter.append(particle_list[i])
                un_pair_list.append(uniq_p)
                temperature.append(T)
                prob.append(p)
                prob_dash.append(p_dash)
                
    for k in select_iter:
        selected_conf.append(k)
        print("selected pairs is now ",selected_conf)
        for c in combinations(k,2):
            
#                 print("removing this item from pairs list :- ",list(c))
                pairs.remove(list(c))
            
#                 print("{} is not present in pairs (already removed in previous iterations)".format(list(c)))
                
            
    particle_list,particle_pos = generate_random_particles(no_of_particles,size_of_each_dimension)
    
    print("\nnew set of particles are :- \n",particle_list)
    
    overall_prob = overall_prob + prob
    
    overall_prob_dash = overall_prob_dash + prob_dash
  
    overall_un_pair = overall_un_pair + un_pair_list
    
    overall_temp = overall_temp + temperature
    
    T = T * cf
    
    
rem_pairs = len(pairs)
coverage = ((total_pairs - rem_pairs)/ total_pairs) * 100

print("\nNumber of pairs left to be covered :- ",rem_pairs)

print("\nPairs left to be covered :- \n",pairs)

df = pd.DataFrame()
df['Configuration'] = selected_conf
df['Distinct_pairs'] = overall_un_pair
df['Temperature'] = overall_temp
df['P_dash'] = overall_prob_dash
df['P'] = overall_prob 

print("\n\n -----------> {} configurations with {:.2f}% coverage <--------------\n\n".format(len(selected_conf),coverage))
print(df)

print("\n ------------------------------------------------------------------ ")
