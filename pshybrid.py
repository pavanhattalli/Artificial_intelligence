import random
import math
import itertools,time
from itertools import combinations
import pandas as pd
#----------------------------------------------------------------------------------------------------------

list_of_dimensions = []                                                                  # Global variables
# gBest = []
covered_pairs = []
sod = []
soln_set = []
rem_pairs = 0
#----------------------------------------------------------------------------------------------------------

def form_pairs(l,ele):                                                                      # Forming Pairs
    pairs = []
    for i in l:
            pairs.append([ele,i])
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

flag = int(input("Enter 1 for default test case or any other number for custom input : "))
if flag == 1:
    no_of_dimensions = 20
    size_of_each_dimension = [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
    no_of_particles = 2
else:
    no_of_dimensions = int(input('Enter Number of Dimensions : '))
    size_of_each_dimension = [int(x) for x in input('Enter Size of Each Dimension : ').split()]
    no_of_particles = int(input("Enter number of particles : "))


no_of_iter = int(input("Enter the number of iterations : "))    
ideal = no_of_dimensions*(no_of_dimensions-1) // 2    
pairs = generate_pairs(size_of_each_dimension)
particle_list,particle_pos = generate_random_particles(no_of_particles,size_of_each_dimension)

# particle_pos = [[0,0,0,0],[1,1,1,1],[2,2,2,2],[1,0,2,0],[2,1,1,0]]
# particle_list = [[1,4,7,10],[2,5,8,11],[3,6,9,12],[2,4,9,10],[3,5,8,10]]

print("\nTotal pairs : {} \nPairs :- {}".format(len(pairs),pairs))
print("\nparticle list is -----> ",particle_list)
ttp = len(pairs)

# particle_object_list = []
# for i in range(no_of_particles):
#     particle_object_list.append(Particle(no_of_dimensions,particle_pos[i]))


class Particle:
    
    def __init__(self,num_dimensions,positions,particle_list):
        self.particle_values = particle_list
        self.particle_position = positions
        self.particle_velocity = []
        self.iter_pbest = []
        self.pbest = -1
        self.iter_gbest = []
        self.gbest = -1
        
        for i in range(0,num_dimensions):
            self.particle_velocity.append(random.uniform(-1,1))
        
        
particle_object_list = []
for i in range(no_of_particles):
    particle_object_list.append(Particle(no_of_dimensions,particle_pos[i],particle_list[i]))
    

print("Particle object list :- ",particle_object_list);


def display(particle_object_list):
    for i in range(len(particle_object_list)):
        print("\n------ Particle {} initialization details ------".format(i+1))
        print("particle position :- ",particle_object_list[i].particle_position)
        print("particle values :- ",particle_object_list[i].particle_values)
        print("particle velocity :- ",particle_object_list[i].particle_velocity)
        #print("particle iter_best :- ",particle_object_list[i].iter_pbest)
        #print("particle iter_gbest :- ",particle_object_list[i].iter_gbest)
        

display(particle_object_list)

def unique_pairs(values_list,pairs_in_while):
    
    temp_pbest = 0
    temp_pairs = []
    for comb in combinations(values_list, 2):
        temp_pairs.append(list(comb))
    
    for i in range(len(temp_pairs)):
        if (not temp_pairs[i] in pairs_in_while) and temp_pairs[i] in pairs:
            temp_pbest += 1
            pairs_in_while.append(temp_pairs[i])
        else:
            print("this pair is repeated ",temp_pairs[i])
            
    return temp_pbest,pairs_in_while


    
# --------------------------------------------------------------------------------------------------------------
    
def update_velocity(particle_object,gbest):
    w = 0.9
    c1 = 0.8
    c2 = 0.3
    
    pos = particle_object.particle_position
    print("\n--Update velocity --\npositions are :- ",pos)
    vel_upd = []
    print("previous velocities are ",particle_object.particle_velocity)
    for i in range(no_of_dimensions):
        r1=random.random()
        r2=random.random()
        
        vel_cog = c1 * r1 * (particle_object.pbest - pos[i])
        vel_soc = c2 * r2 * (gbest - pos[i])
        
        res = w * particle_object.particle_velocity[i] + vel_cog + vel_soc
        
        #res = math.tanh(res)            #to map between -1 and 1
        if res < (-1 * size_of_each_dimension[i]):
        	res = float(-1 * size_of_each_dimension[i])
        elif res > size_of_each_dimension[i]:
        	res = float(size_of_each_dimension[i])
        vel_upd.append(res)
    
    particle_object.particle_velocity = vel_upd
    print("updated velocity are :- ",vel_upd)
    
# -----------------------------------------------------------------------------------------------------------------

def update_position(particle_object):
    
    print("\nprevios positions are :- ",particle_object.particle_position)
    for i in range(no_of_dimensions):
        res = particle_object.particle_position[i] + particle_object.particle_velocity[i]
#         res = round(res)
        
        if res > size_of_each_dimension[i]-1:
#             res = size_of_each_dimension[i]-1
            res = random.randint(0,size_of_each_dimension[i]-1)
        elif res < 0:
#             res = 0
            res = random.randint(0,size_of_each_dimension[i]-1)
        else:
            res = round(res)
            
        particle_object.particle_position[i] = res
        
    print("updated positions are :- ",particle_object.particle_position)        


# --------------------------------------------------------------------------------------------------------------------

def update_values(particle_object):
    
    print("\nprevious particle values are :- ",particle_object.particle_values)
    for i in range(no_of_dimensions):
        if i == 0:
            particle_object.particle_values[i] = particle_object.particle_position[i] + 1
        else:
            s = sum(size_of_each_dimension[0:i]) + particle_object.particle_position[i] 
            particle_object.particle_values[i] = s + 1
            
    print("updated particle values are :- ",particle_object.particle_values)
    


# -------------------------------------------------------------------------------------------------------------------
# driver code

selected_pairs = []
# no_of_iter = 5
ic = 0
while no_of_iter > 0 and len(pairs) > 0:
    print("\n\n--------- Iteration no. {} ------------".format(ic+1))
    ic += 1
    no_of_iter = no_of_iter - 1
    
    pbest_in_iter = []
    
    pairs_in_while = []
    for i in range(no_of_particles):
        print("\nparticles is : ",particle_object_list[i].particle_values)
        particle_object_list[i].pbest,pairs_in_while = unique_pairs(particle_object_list[i].particle_values,pairs_in_while)
        print("It's pbest is :- ",particle_object_list[i].pbest)
        pbest_in_iter.append(particle_object_list[i].pbest)
        
#     print("Unique pairs generated in this iteration :- ",pairs_in_while)
    
    iter_gbest = max(pbest_in_iter)
    print("\n**********GBEST OF THIS ITERATION IS************==",iter_gbest)
    print(ideal)
        

    flag = 0
    
    all_gbest_particles = []
    
    if iter_gbest != 0:
        for i in range(no_of_particles):
            if particle_object_list[i].pbest == iter_gbest:
                print("hey adding result")
                temp2 = particle_object_list[i].particle_values.copy()
                if temp2 not in selected_pairs:
                    all_gbest_particles.append(temp2)
#                     selected_pairs.append(temp2)
#                     print("selected pairs is now ",selected_pairs)
                    flag = 1
#                     break
    
    
    
    if flag == 1:
        for k in all_gbest_particles:
            selected_pairs.append(k)
            soln_set.append(k)
            print("selected pairs is now ",selected_pairs)
            for c in combinations(k,2):
                try:
                    print("removing this item from pairs list :- ",list(c))
                    pairs.remove(list(c))
                except:
                    print("{} is not present in pairs (already removed in previous iterations)".format(list(c)))
    
    
    for i in range(no_of_particles):
        update_velocity(particle_object_list[i],iter_gbest)
        
        
    print("\nNow number of pairs left are ",len(pairs))
    print("remaining pairs are :- ",pairs)
    
    for i in range(no_of_particles):
        update_position(particle_object_list[i])
    
    for i in range(no_of_particles):
        update_values(particle_object_list[i])
        
        
# -----------------------------------------------------------------------------------------------------------------

print("\nLength of selected particles :- ",len(selected_pairs))

print("\nSelected particles :- ",selected_pairs)

print("\nLength of pairs left to be covered :- ",len(pairs))

print("\nPairs left to be covered :- ",pairs)


if len(pairs)==0:
    print("All Pairs Covered by PSO")
else:
    
    class simulated_annealing:
        def generate_pairs(self,l):
            all_pairs = []
            counter1 = 1
            self.l = l
            for i in l:
                temp_list = []
        
                for j in range(i):
                    temp_list.append(counter1)
                    counter1 = counter1 + 1
                    list_of_dimensions.append(temp_list)
        
            for i in range(len(l)):
        
                temp_list2 = []
        
            for j in range(i+1,len(l)):
                temp_list2 = temp_list2 + list_of_dimensions[j]  
        
            for k in range(len(list_of_dimensions[i])):
                temp_list3 = []
                temp_list3 = temp_list3 + temp_list2
                all_pairs = all_pairs + form_pairs(temp_list3,list_of_dimensions[i][k])

            return all_pairs
        
        
        def generate_random_particles(self,num_of_particles,size_of_each_dimension):       # Generating random particles
            self.num_of_particles = num_of_particles
            self.size_of_each_dimension = size_of_each_dimension
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
        
        
    sann = simulated_annealing()
    sa_pairs = []
    sa_particle_list,sa_particle_pos = sann.generate_random_particles(no_of_particles,size_of_each_dimension)
    total_pairs = len(pairs)
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
   
    print("Particles generated by SA=",sa_particle_list)
    
    cov = ((ttp-len(pairs))/ttp)*100
    print("Total number of pairs generated=",ttp)
    print("Number of pairs covered by PSO=",(ttp-len(pairs)))
    print("Number of Remaining Pairs after PSO=",len(pairs))
    print("Coverage after PSO=",cov)
   
    print("Number of Particles generated from SA=",len(sa_particle_list))
    
    
    print("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
    #------------------------------------------------------------------------------------------------------------------------------------------
    T = 200
    cf = 0.99842
    print("\n\tTemperature :- {} \n\tCooling factor :- {}".format(T,cf))

    ch = int(input("\nDo you want to change these parameters ? Enter 1 for Yes..!! :- "))
    if ch == 1:
         int(input("Enter starting temperature (T) :- "))
         cf = float(input("Enter Cooling Factor (cf) :- "))
    p_dash = 0
    p = 0
    selected_conf = []
    count = 1
    overall_prob = []
    overall_prob_dash = []
    overall_un_pair = []
    overall_temp = []
    s = []
    while T > 0.000001 and len(pairs) > 0:
        
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
        
        for i in range(len(sa_particle_list)):
            uniq_p,pairs_in_while = unique_pairs(sa_particle_list[i],pairs_in_while)
            
            print("\nparticle {} is generating {} unique pairs ".format(sa_particle_list[i],uniq_p))
            if uniq_p == ideal:
                select_iter.append(sa_particle_list[i])
                prob.append(0)
                temperature.append(T)
                prob_dash.append(0)
                un_pair_list.append(uniq_p)
                
            elif uniq_p > (ideal // 3):
                diff = ideal - uniq_p
                p = math.exp(-(diff)/T)
                p_dash = random.uniform(0,1)
            
                if p_dash < p:
                    select_iter.append(sa_particle_list[i])
                    un_pair_list.append(uniq_p)
                    temperature.append(T)
                    prob.append(p)
                    prob_dash.append(p_dash)
                
                    
        for k in select_iter:
            selected_conf.append(k)
            soln_set.append(k)
            print("selected pairs is now ",selected_conf)
            for c in combinations(k,2):
                    s = list(c)
                    sa_pairs.append(s)
                       
        sa_particle_list,particle_pos = generate_random_particles(no_of_particles,size_of_each_dimension)
    
        print("\nnew set of particles are :- \n",sa_particle_list)
    
        overall_prob = overall_prob + prob
        
        overall_prob_dash = overall_prob_dash + prob_dash
  
        overall_un_pair = overall_un_pair + un_pair_list
    
        overall_temp = overall_temp + temperature
        
        T = T * cf

#-------------------------------------------------------------------------------------------

    print("SA PAIRS=",sa_pairs)
    for i in sa_pairs:
        for j in pairs:
            if i==j:
                pairs.remove(j)
                
    rem_pairs = len(pairs)

    print("TOTAL REMAINING PAIRS=",len(pairs))
    print("PAIRS REMAINING AFTER SIMULATED ANNEALING=",rem_pairs)
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
print("ttp=",ttp)  
df1 = pd.DataFrame()
df1['TOTAL CONFIGURATIONS PSO + SA'] = soln_set
print(df1)
acc = ((ttp - rem_pairs) / ttp) * 100
print("TOTAL ACCURACY=",acc)



  
          
                
                
            
            
        
        
    
            
       
       
        
        
        


    
