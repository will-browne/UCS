from Read_UCS import Read_UCS_Sets
from Read_UCS import Read_Natural_UCS_Solution
from Read_UCS import Read_XCS_Absumption_Sets
from Read_UCS import Read_XCS_Standard_Sets
from Env import environment
from Time_Record import Time_Calculate
import copy


class UCS_RCR:
    def __init__(self,add):

        self.TC=Time_Calculate()

        UCS_Set=Read_UCS_Sets(add)

        format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()

        self.Populations_Set=UCS_Set.population_list


        self.Diversity_Razor()

        self.problem_length=self.Get_Problem_length()

        #self.Print_Population(self.Populations_Set[2])

        self.clustered=self.Cluster()
        
        #self.Print_Cluster()

        self.discount=0.3

        self.Polymorphism_Razor()

        self.Print_Cluster()

        format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
        r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
        
        print(r_time)
        #self.savename='Natural_Solution\\6_MUX.txt'
        #self.savename='Natural_Solution\\6_Carry.txt'
        #self.savename='Natural_Solution\\6_MajorityOn.txt'
        #self.savename='Natural_Solution\\8_MajorityOn.txt'
        #self.savename='Natural_Solution\\ZOO.txt'
        #self.savename='Natural_Solution\\ZOO_RICH.txt'
        #self.savename='Natural_Solution\\ZOO_100k_UCS.txt'
        #self.savename='Natural_Solution\\11_MUX.txt'
        #self.savename='Natural_Solution\\20_MUX.txt'
        #self.savename='Natural_Solution\\10_Majority.txt'
        #self.savename='Natural_Solution\\12_carry.txt'
        #self.savename='Natural_Solution\\10_carry.txt'
        #self.savename='Natural_Solution\\9_MajorityOn.txt'
        #self.savename='Natural_Solution\\default.txt'
        #self.savename='Natural_Solution\\carry_8.txt'
        self.savename='Natural_Solution\\7_MajorityOn.txt'
        self.Save()

    ########################################################
    ############            Diversity Razor        #########
    ########################################################
    #Remove the potential incorrect rules
    #Accuracy<1.0 
    #(experience<representativeRange * BargainRate)  Not Use Yet

    def Accuracy_Remover(self,population):
        remove_list=[]
        for id in range(0,len(population)):
            if population[id][4]<1.0:
                remove_list.append(id)
        count=0
        for id in remove_list:
            population.pop(id-count)
            count+=1


    def Diversity_Razor(self):
         for i in range(0,len(self.Populations_Set)):
             self.Accuracy_Remover(self.Populations_Set[i])

    ########################################################
    ############            Cluster                #########
    ########################################################

    def Get_Problem_length(self):
        return len(self.Populations_Set[0][0][0])

    def Initial_Cluster(self):
        cluster=[]
        for i in range(0,self.problem_length+1):
            p=[]
            cluster.append(p)
        return cluster

    def calculate_cluster_level(self,condition):
        id=0
        for cod in condition:
            if cod=='#':
                id+=1
        return id

    #judge whether two condition is same
    def Is_Same_Condition(self,c1,c2):
        for i in range(0,len(c1)):
            if c1[i] != c2[i]:
                return False
        return True

    #judge is exist
    def Is_Same_Rule(self,R1,R2):
        if R1[1]!=R2[1]:
            return False
        else:
            #condition 0
            if self.Is_Same_Condition(R1[0],R2[0]):
                return True
            else:
                return False

    #Judge is rule exist in cluster
    def Is_Exist_Level(self,cluster,rule):
        for id in range(0,len(cluster)):
            if self.Is_Same_Rule(cluster[id],rule):
                return id
        return None

    def Cluster(self):
        cluster=self.Initial_Cluster()
        for population in self.Populations_Set:
            for rule in population:
                #0 condition
                level=self.calculate_cluster_level(rule[0])
                id= self.Is_Exist_Level(cluster[level],rule)
                if id !=None:
                    #numerosity 2
                    cluster[level][id][2]+=rule[2]
                    #exp 9
                    cluster[level][id][9]+=rule[9]
                else:
                    cluster[level].append(rule)
        return cluster




    ########################################################
    ############        Polymorphism Razor         #########
    ########################################################

    #check whether gener rule is more gener
    def Is_More_general_Subsumption(self,gener_condition,specific_condition):
         for i in range(0,len(gener_condition)):
             if gener_condition[i] !='#' and gener_condition[i]!=specific_condition[i]:
                 return False
         return True

    
     

    #check whether gener rule is more gener

    def Sub_sumption(self):

         for level in range(len(self.clustered)-1,0,-1):
             for g_rule in self.clustered[level]:
                 
                 for C_level in range(level-1,-1,-1):
                     remove_list=[]
                     for S_id in range(0,len(self.clustered[C_level])):
                         #0 condition
                         if self.Is_More_general_Subsumption(g_rule[0],self.clustered[C_level][S_id][0]):
                             remove_list.append(S_id)
                     count=0
                     for r_id in remove_list:
                         self.clustered[C_level].pop(r_id-count)
                         count+=1


    def Is_More_general_Subsumption(self,gener_condition,specific_condition):
         for i in range(0,len(gener_condition)):
             if gener_condition[i] !='#' and gener_condition[i]!=specific_condition[i]:
                 return False
         return True


    def Cal_Clustered_average_experience(self):
        experience=[]
        for i in range(0,len(self.clustered)):
            experience.append(0)
        for i in range(0,len(self.clustered)):
            for rule in self.clustered[i]:
                experience[i]+=rule[9]
            if len(self.clustered[i])>0:
                experience[i]=int((experience[i]*1.0)/len(self.clustered[i]))
        return experience

    def Raw_Tested_Razor(self):
        experience=self.Cal_Clustered_average_experience()
        #print experience
        for i in range(0,len(self.clustered)):
            delete_list=[]
            for j in range(0,len(self.clustered[i])):
                if self.clustered[i][j][9]<self.discount*experience[i]:
                    delete_list.append(j)
 
            count=0
            for number in delete_list:
                self.clustered[i].pop(number-count)
                count+=1

    def Polymorphism_Razor(self):
        self.Raw_Tested_Razor()
        self.Error_Detection()
        self.Sub_sumption()

    #check whether two rules conflit
    def Over_lapping_Outer(self,condition_1, condition_2):
        for i in range(0,len(condition_1)):
            if condition_1[i] !='#' and condition_2[i]!='#' and condition_1[i]!=condition_2[i]:
                return False
        return True

    #initial the error list
    def Initial_Error_List_Outer(self):
        result=[]
        
        for i in range(0,self.problem_length+1):
            temp=[]
            result.append(temp)
        return result

    def Error_Detection(self):
        # initial the error list
        error_list=self.Initial_Error_List_Outer()

        for i in range(1,len(self.clustered)):
            # judge wether is unvalied
            
            for rule_h in range(0,len(self.clustered[i])):
                #using error score or not
                error_score=0
                for j in range(0,i+1): 
                    if  rule_h in error_list[i]: 
                        break
                    else:       
                        for rule_l in range(0,len(self.clustered[j])):
                            if not rule_l in error_list[j]:
                                #same action 1
                                #6 critical state of gener explore state
                                #if population[j][rule_l][6]==True:
                                if self.clustered[i][rule_h][1] != self.clustered[j][rule_l][1]:
                                    if self.Over_lapping_Outer(self.clustered[i][rule_h][0],self.clustered[j][rule_l][0]):
                                            error_score+=self.clustered[j][rule_l][10]
                                            if error_score>self.clustered[i][rule_h][10]:
                                            #print (error_score, population[i][rule_h][3]+population[i][rule_h][4])
                                                error_list[i].append(rule_h)
                                                break


        for i in range(1,len(error_list)):
            if len(error_list[i])!=0:
                count=0
                del_list=copy.deepcopy(error_list[i])
                del_list.sort()
                for dele in del_list:
                    self.clustered[i].pop(dele-count)
                    count+=1

        print (error_list)
        #return error_list
    ################### Print Population  ##############
    def Print_Population(self,population):
        for id in range(0,len(population)):
            print(population[id][0],':',population[id][1],"Num:",population[id][2],
                  "Fit:", round(population[id][3],2),"Acc:", round(population[id][4],2),
                  "EXP",population[id][9])

    def Print_Cluster(self):
        size=0
        for i in range(0,len(self.clustered)):
            print('=================================',i)
            size+=len(self.clustered[i])
            for rule in self.clustered[i]:
                print (rule)
        print(size)

    ################### Save compacted result  ##############
    def save_performance(self,txt,name):
        f=open(name,'wb')
        f.write(txt.encode())
        f.close()

    def Convert_To_String(self):
        results=''
        for i in range(0,len(self.clustered)):
            for rule in self.clustered[i]:
                condition=''
                for cod in rule[0]:
                    condition+=str(cod)+' '
                result=condition+'--> '+str(rule[1])+'\n'
                results+=result
        return results
    
    
    def Save(self):
        result=self.Convert_To_String()
        self.save_performance(result,self.savename)
        
class UCS_Optimal:
    def __init__(self,address,problem_ID):
       Read_UCS=Read_Natural_UCS_Solution(address)

       self.env=environment(None)
       self.env.Initial_Real_Value(problem_ID)


       self.Raw_Population=Read_UCS.population

       self.record_matched_instance()

       #self.Test_Accuracy()

       self.clustered=self.Conver_to_Cluster()

       self.Optimal()

       self.savename='Natural_Solution\\ZOO_RICH_OPTIMAL.txt'

       self.print_clustered()

       self.Save()

    #convert 
    def Conver_to_Cluster(self):
        length=len(self.Raw_Population[0][0])
        cluster=[]
        for i in range(0,length+1):
            temp=[]
            cluster.append(temp)

        for rule in self.Raw_Population:
            level=self.General_Level(rule[0])
            cluster[level].append(rule)

        return cluster

    #change the population' rules format
    def Add_Record_Column(self):
        for rule in self.Raw_Population:
            #3 record the matched instances
            temp=[]
            rule.append(temp)

    def isConditionMatched(self,condition,state):
        for i in range(0,len(condition)):
            if condition[i]!='#' and condition[i] != state[i]:
                return False
        return True

    def Prediction(self,state):
        for rule in self.Raw_Population:
            if self.isConditionMatched(rule[0],state):
                return rule[1]

    def Test_Accuracy(self):
        count=0
        for id in range(0,len(self.env.state)):
            action_p=self.Prediction(self.env.state[id])
            if action_p==self.env.actions[id]:
                count+=1
        acc= 1.0*count/len(self.env.state)
        print(acc,'%')
        return acc

    def General_Level(self,condition):
        count=0
        for cod in condition:
            if cod=='#':
                count+=1
        return count

    def record_matched_instance(self):
        self.Add_Record_Column()
        kill_list=[]
        for i in range(0,len(self.env.state)):
            for rule in self.Raw_Population:
                if self.isConditionMatched(rule[0],self.env.state[i]):
                    if rule[1]==self.env.actions[i]:
                        rule[2].append(i)
                    else:
                        kill_list.append(rule)
        #print 'k',kill_list 
        #self.Print_population()


    def Print_population(self):
        for rule in self.Raw_Population:
            print (rule)

    def print_clustered(self):
        for i in range(0,len(self.clustered)):
            print ('==========================================')
            for rule in self.clustered[i]:
                print(rule)

    def Is_contained_two_level(self,gener_list,specific_list):
        for spe in specific_list:
            if not spe in gener_list:
                return False
        return True

    def Optimal(self):

        #remove the over specific rule in lower level
        for i in range(len(self.clustered)-1,0,-1):
            #remove subsumable rules based pn genptype(phenotype)
            if len(self.clustered[i])>0:
                for g_rule in self.clustered[i]:
                    
                    for c_i in range(i-1,-1,-1):
                        s_d_list=[]
                        if len(self.clustered[c_i])>0:                        
                            for s_id in range(0,len(self.clustered[c_i])):
                                if g_rule[1]==self.clustered[c_i][s_id][1]:
                                    if self.Is_contained_two_level(g_rule[2],self.clustered[c_i][s_id][2]):
                                        s_d_list.append(s_id)

                        inner_count=0
                        if len(s_d_list)>0:
                            for r_id in s_d_list:
                                self.clustered[c_i].pop(r_id-inner_count)
                                inner_count+=1
                        
        #remove the over specific rule in same level
        for i in range(0,len(self.clustered)):
            if len(self.clustered[i])>0:
                remove_list=[]
                #find subsumable at the same general level
                for g_id in range(0,len(self.clustered[i])):
                    for s_id in range(0,len(self.clustered[i])):
                        if not s_id in remove_list:
                            if g_id!=s_id:
                                if self.clustered[i][g_id][1]==self.clustered[i][s_id][1]:
                                    if self.Is_contained_same_level(self.clustered[i][g_id][2],self.clustered[i][s_id][2]):
                                        remove_list.append(s_id)
                same_count=0
                if len(remove_list)>0:
                    remove_list.sort()
                    for r_id in remove_list:
                        self.clustered[i].pop(r_id-same_count)
                        same_count+=1


    def Is_contained_same_level(self,gener_list,specific_list):
        for spe in specific_list:
            if not spe in gener_list:
                return False

        if len(gener_list)==len(specific_list):
            return False
        return True
          
    def save_performance(self,txt,name):
        f=open(name,'wb')
        f.write(txt.encode())
        f.close()

    def Convert_To_String(self):
        results=''
        for i in range(0,len(self.clustered)):
            for rule in self.clustered[i]:
                condition=''
                for cod in rule[0]:
                    condition+=str(cod)+' '
                result=condition+'--> '+str(rule[1])+'\n'
                results+=result
        return results
    
    
    def Save(self):
        result=self.Convert_To_String()
        self.save_performance(result,self.savename)

#add='Check_Boolean\\Mux'
#add='Check_Boolean\\Carry_6'
#add='Check_Boolean\\Majority_6'
#add='Result'
#add='Check_Boolean\\ZOO_100K'
#add='Check_Boolean\\ZOO_4m_ucs'
#add='Check_Boolean\\11_mux_ucs'
#add='Check_Boolean\\20_mux_ucs'
#add='Check_Boolean\\20_mux_ucs'
#add='Check_Boolean\\Majority_10'
#add='Check_Boolean\\carry_12'
#add='Check_Boolean\\carry_10'
#add='Check_Boolean\\Majority_9'
#add='Check_Boolean\\20_mux_new'
#add='Check_Boolean\\carry_8'
add='Check_Boolean\\Majority_7'
#RCR=UCS_RCR(add)    

#add='Natural_Solution\\ZOO_RICH.txt'
#add='Natural_Solution\\ZOO_100k_UCS.txt'
#ID=1
#UCS_Optimal(add,ID)

class XCS_Abusmption_RCR:
    def __init__(self,add,problem_ID,XCS_Type):
        if XCS_Type==0:
            XCS_Set=Read_XCS_Absumption_Sets(add)
        elif XCS_Type==1:
            XCS_Set=Read_XCS_Standard_Sets(add)
        self.Populations_Set=XCS_Set.population_list

        #initial environment
        self.env=environment(None)
        self.env.Initial_Real_Value(problem_ID)


        print len(self.Populations_Set[0])
        self.Diversity_Razor()
        print len(self.Populations_Set[0])

        self.problem_length=self.Get_Problem_length()


        self.clustered_P,self.clustered_N=self.Cluster()

        self.Optimal_P()
        
        self.Optimal_N()

        self.Print_Cluster_P()

        self.Print_Cluster_N()



        

        #self.savename_P='Natural_Solution\\ZOO_Absumption_100k_Positive.txt'
        #self.savename_N='Natural_Solution\\ZOO_Absumption_100k_Negative.txt'
        #self.savename_P='Natural_Solution\\ZOO_Standard_100k_Positive.txt'
        #self.savename_N='Natural_Solution\\ZOO_Standard_100k_Negative.txt'
        self.savename_P='Natural_Solution\\test_Positive.txt'
        self.savename_N='Natural_Solution\\test_Negative.txt'
        self.Save()

        #self.Print_population()


    ########################################################
    ############            Diversity Razor        #########
    ########################################################
    #Remove the potential incorrect rules
    #Accuracy<1.0 
    #(experience<representativeRange * BargainRate)  Not Use Yet

    def Accuracy_Remover(self,population):
        remove_list=[]
        for id in range(0,len(population)):
            #3 Accuracy
            if population[id][3]<1.0:
                remove_list.append(id)
        count=0
        for id in remove_list:
            population.pop(id-count)
            count+=1

    def Inconsist_Remover(self,population):
        remove_list=[]
        for id in range(0,len(population)):
            #3 Accuracy
            if population[id][9]*population[id][10]!=0:
                remove_list.append(id)
            elif population[id][9]==0 and population[id][10]==0:
                remove_list.append(id)

        count=0
        for id in remove_list:
            population.pop(id-count)
            count+=1


    def Diversity_Razor(self):
        
        for i in range(0,len(self.Populations_Set)):
             #self.Accuracy_Remover(self.Populations_Set[i])
             self.record_matched_instance(self.Populations_Set[i])
             self.Inconsist_Remover(self.Populations_Set[i])

    #change the population' rules format
    def Add_Record_Column(self,population):
        for rule in population:
            #3 record the matched instances
            temp=[]
            rule.append(temp)
            rule[9]=0
            rule[10]=0

    def isConditionMatched(self,condition,state):
        for i in range(0,len(condition)):
            #if len(condition)!= len(state):
            #    print len(state)
            #    print state
            #    print len(condition)
            #    print condition
            if condition[i]!='#' and condition[i] != state[i]:
                return False
        return True

    def record_matched_instance(self,population):
        self.Add_Record_Column(population)        
        for i in range(0,len(self.env.state)):
            for rule in population:
                if self.isConditionMatched(rule[0],self.env.state[i]):
                    if rule[1]==self.env.actions[i]:
                        rule[11].append(i)
                        rule[10]+=1
                    else:
                        rule[11].append(i)
                        rule[9]+=1

    ###### Print Population ###############
    def Print_population(self):
        for rule in self.Populations_Set[0]:
            print rule


    ########################################################
    ############            Cluster                #########
    ########################################################

    def Get_Problem_length(self):
        return len(self.Populations_Set[0][0][0])

    def Initial_Cluster(self):
        cluster=[]
        for i in range(0,self.problem_length+1):
            p=[]
            cluster.append(p)
        return cluster

    def calculate_cluster_level(self,condition):
        id=0
        for cod in condition:
            if cod=='#':
                id+=1
        return id

    #judge whether two condition is same
    def Is_Same_Condition(self,c1,c2):
        for i in range(0,len(c1)):
            if c1[i] != c2[i]:
                return False
        return True

    #judge is exist
    def Is_Same_Rule(self,R1,R2):
        if R1[1]!=R2[1]:
            return False
        else:
            #condition 0
            if self.Is_Same_Condition(R1[0],R2[0]):
                return True
            else:
                return False

    #Judge is rule exist in cluster
    def Is_Exist_Level(self,cluster,rule):
        for id in range(0,len(cluster)):
            if self.Is_Same_Rule(cluster[id],rule):
                return id
        return None



    def Cluster(self):
        cluster_P=self.Initial_Cluster()
        cluster_N=self.Initial_Cluster()
        for population in self.Populations_Set:
            for rule in population:
                if rule[6]==1000:
                #0 condition
                    level=self.calculate_cluster_level(rule[0])
                    id= self.Is_Exist_Level(cluster_P[level],rule)
                    if id !=None:
                        #numerosity 2
                        cluster_P[level][id][2]+=rule[2]
                        #exp 9
                        cluster_P[level][id][9]+=rule[9]
                    else:
                        cluster_P[level].append(rule)
                elif rule[6]==0:
                    level=self.calculate_cluster_level(rule[0])
                    id= self.Is_Exist_Level(cluster_N[level],rule)
                    if id !=None:
                        #numerosity 2
                        cluster_N[level][id][2]+=rule[2]
                        #exp 9
                        cluster_N[level][id][9]+=rule[9]
                    else:
                        cluster_N[level].append(rule)
        return cluster_P,cluster_N

    def Print_Cluster_P(self):
        for i in range(0,len(self.clustered_P)):
            print('=================================',i)
            for rule in self.clustered_P[i]:
                print rule[0],rule[1]
                print rule[11]

    def Print_Cluster_N(self):
        for i in range(0,len(self.clustered_N)):
            print('=================================',i)
            for rule in self.clustered_N[i]:
                print rule[0],rule[1]
                print rule[11]
                print len(rule[11])

    def Is_contained_two_level(self,gener_list,specific_list):
        for spe in specific_list:
            if not spe in gener_list:
                return False
        return True

    def Is_contained_same_level(self,gener_list,specific_list):
        for spe in specific_list:
            if not spe in gener_list:
                return False

        if len(gener_list)==len(specific_list):
            return False
        return True

    def Optimal_P(self):

        #remove the over specific rule in lower level
        for i in range(len(self.clustered_P)-1,0,-1):
            #remove subsumable rules based pn genptype(phenotype)
            if len(self.clustered_P[i])>0:
                for g_rule in self.clustered_P[i]:
                    
                    for c_i in range(i-1,-1,-1):
                        s_d_list=[]
                        if len(self.clustered_P[c_i])>0:                        
                            for s_id in range(0,len(self.clustered_P[c_i])):
                                if g_rule[1]==self.clustered_P[c_i][s_id][1]:
                                    if self.Is_contained_two_level(g_rule[11],self.clustered_P[c_i][s_id][11]):
                                        s_d_list.append(s_id)

                        inner_count=0
                        if len(s_d_list)>0:
                            for r_id in s_d_list:
                                self.clustered_P[c_i].pop(r_id-inner_count)
                                inner_count+=1
                        
        #remove the over specific rule in same level
        for i in range(0,len(self.clustered_P)):
            if len(self.clustered_P[i])>0:
                remove_list=[]
                #find subsumable at the same general level
                for g_id in range(0,len(self.clustered_P[i])):
                    for s_id in range(0,len(self.clustered_P[i])):
                        if not s_id in remove_list:
                            if g_id!=s_id:
                                if self.clustered_P[i][g_id][1]==self.clustered_P[i][s_id][1]:
                                    if self.Is_contained_same_level(self.clustered_P[i][g_id][11],self.clustered_P[i][s_id][11]):
                                        remove_list.append(s_id)
                same_count=0
                if len(remove_list)>0:
                    remove_list.sort()
                    for r_id in remove_list:
                        self.clustered_P[i].pop(r_id-same_count)
                        same_count+=1

    def Optimal_N(self):

        #remove the over specific rule in lower level
        for i in range(len(self.clustered_N)-1,0,-1):
            #remove subsumable rules based pn genptype(phenotype)
            if len(self.clustered_N[i])>0:
                for g_rule in self.clustered_N[i]:
                    
                    for c_i in range(i-1,-1,-1):
                        s_d_list=[]
                        if len(self.clustered_N[c_i])>0:                        
                            for s_id in range(0,len(self.clustered_N[c_i])):
                                if g_rule[1]==self.clustered_N[c_i][s_id][1]:
                                    if self.Is_contained_two_level(g_rule[11],self.clustered_N[c_i][s_id][11]):
                                        s_d_list.append(s_id)

                        inner_count=0
                        if len(s_d_list)>0:
                            for r_id in s_d_list:
                                self.clustered_N[c_i].pop(r_id-inner_count)
                                inner_count+=1
                        
        #remove the over specific rule in same level
        for i in range(0,len(self.clustered_N)):
            if len(self.clustered_N[i])>0:
                remove_list=[]
                #find subsumable at the same general level
                for g_id in range(0,len(self.clustered_N[i])):
                    for s_id in range(0,len(self.clustered_N[i])):
                        if not s_id in remove_list:
                            if g_id!=s_id:
                                if self.clustered_N[i][g_id][1]==self.clustered_N[i][s_id][1]:
                                    if self.Is_contained_same_level(self.clustered_N[i][g_id][11],self.clustered_N[i][s_id][11]):
                                        remove_list.append(s_id)
                same_count=0
                
                if len(remove_list)>0:
                    remove_list.sort()
                    #print(remove_list)
                    for r_id in remove_list:
                        self.clustered_N[i].pop(r_id-same_count)
                        same_count+=1

    ################### Save compacted result  ##############
    def save_performance(self,txt,name):
        f=open(name,'wb')
        f.write(txt.encode())
        f.close()

    def Convert_To_String(self,clustered):
        results=''
        for i in range(0,len(clustered)):
            for rule in clustered[i]:
                condition=''
                for cod in rule[0]:
                    condition+=str(cod)+' '
                result=condition+'--> '+str(rule[1])+'\n'
                results+=result
        return results
    
    
    def Save(self):
        P_result=self.Convert_To_String(self.clustered_P)
        self.save_performance(P_result,self.savename_P)
        N_result=self.Convert_To_String(self.clustered_N)
        self.save_performance(N_result,self.savename_N)

#add='Check_Boolean\\ZOO_XCS'
#add='Check_Boolean\\ZOO_100K_A'
#add='Check_Boolean\\ZOO_100K_S'
#add='Check_Boolean\\ZOO_100K_S'
#add='Check_Boolean\\ZOO_XCS_Standard'
#add='Check_Boolean\\ZOO_4m_acs'
#add='Check_Boolean\\ZOO_4m_xcs'
#add='Check_Boolean\\Breast_Cancer'
add='Check_Boolean\\Voting'
ID=8
xcs_type=0 #0: absumption XCS, 1: Standard XCS
XCS_Abusmption_RCR(add,ID,xcs_type)
