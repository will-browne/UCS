from Config import Config
from Env import environment
import random
import copy
import os
import time

class UCS:
    def __init__(self,problem_ID, Problem_Length,num_actions):
        self.con=Config(None)
        # the population of the rules
        self.population=[]

        self.microPopSize=0

        self.Problem_Id=problem_ID

        self.Problem_Length=Problem_Length

        self.numActions=num_actions

        self.IsLinux=False

        #Environment
        self.env=environment(None)
        if problem_ID>3:
            self.env.Initial_Real_Value(problem_ID)
            self.Problem_Length=self.env.real_length
            self.numActions=self.env.real_actions
            #print (self.Problem_Length)
            #print (self.numActions)

        

        

        self.Action_list=self.Initial_Action_List()
        # Major Run Parameters #
        # Specify complete algorithm evaluation maximum number of learning iterations 
        self.maxLearningIterations = 40*1000
        # Maximum size of the rule population (a.k.a. Micro-classifier population size, where N is the sum of the classifier numerosities in the population)
        self.N = 1500                                                
        # The probability of specifying an attribute when covering. (1-p_spec = the probability of adding '#' in ternary rule representations). Greater numbers of attributes in a dataset will require lower values of p_spec.
        self.p_spec = 0.3  

        # Logistical Run Parameters 
        # Specifies the number of iterations before each estimated learning progress report by the algorithm .
        self.trackingFrequency = 5000 
        
        self.correct_track=[0]*self.trackingFrequency
        
        self.Training_Performance=[]   
        ##BEGIN###
        self.Start()

    ################   CLASSIFIER   ##################
    def Create_new_Single_Rule(self,condition,action,explorIter):
        # States of Attributes Specified in classifier (Ternary)
        # 0: condition 
        #class
        # 1: action 
        # The number of rule copies stored in the population.  (Indirectly stored as incremented numerosity)
        # 2: numerosity
        # Classifier fitness - initialized to a constant initial fitness value 
        # 3: fitness
        # Classifier accuracy - Accuracy calculated using only instances in the dataset which this rule matched.
        # 4: accuracy
        # A parameter used in deletion which reflects the size of match sets within this rule has been included.
        # 5: aveActionSetSize
        # The current deletion weight for this classifier.
        # 6: deletionvote
        # Time since rule last in a correct set.
        # 7: timeStampGA
        # Iteration in which the rule first appeared.
        # 8: initiTieStamp
        # Known in many LCS implementations as experience i.e. the total number of times this classifier was in a match set
        # 9: match count
        # The total number of times this classifier was in a correct set
        # 10 correct count

        rule=[]
        rule.append(condition) #0 condition
        rule.append(action) #1 action
        rule.append(1) #2 numerosity
        rule.append(self.con.init_fit) #3 fitness
        rule.append(0.0) #4 accuracy
        rule.append(1) #5 aveActionSetSize
        rule.append(None) #6 deletionvote
        rule.append(explorIter) #7 timeStampGA
        rule.append(explorIter) # 8 initiTieStamp
        rule.append(0) # 9 match count
        rule.append(0) # 10 correct count

        return rule

    ####################   COVERING   ######################
    #Judge whether state match the condition in classifier if match return true otherwise return false
    def isConditionMatched(self,condition,state):
        for i in range(0,len(condition)):
            if condition[i]!='#' and condition[i] != state[i]:
                return False
        return True

    #create a condition which can match the input state
    def createMatchingCondition(self,state):
        condition=[0]*len(state)
        for i in range(0,len(state)):
            if(random.random()<self.p_spec):
                condition[i]='#'
            else:
                condition[i]=state[i]
        return condition

    #get the match set
    def getMatchSet(self,state,action,explorIter):
        fitness_sum=0.0
        match_set=[]
        docovering=True
        #print "begin"
        for i in range(0,len(self.population)):
            #2 numerosity 3 fitness
            fitness_sum+=self.population[i][2]*self.population[i][3]
            #0: condition
            if(self.isConditionMatched(self.population[i][0],state)):
                #add matching classifier to the matchset
                match_set.append(i)
                #1 action
                if self.population[i][1]==action:
                    docovering=False


        # create covering classifiers, if not observed actions are covered
        while (docovering):
            condition_new=self.createMatchingCondition(state)
            rule=self.Create_new_Single_Rule(condition_new,action,explorIter)
            #increase population size
            self.microPopSize+=1
            #2 numerosity 3 fitness
            fitness_sum+=rule[2]*rule[3]
            self.population.append(rule)
            match_set.append(len(self.population)-1)
            docovering=False

        return match_set,fitness_sum


    ################   Prediction   ##################
    def Prediction(self,match_set):
        actions_value=[]
        for i in range(0,self.numActions):
            actions_value.append(0)

        for id in match_set:
            #1: action 2:numerosity 3: # 3: fitness
            actions_value[self.population[id][1]]+=self.population[id][2]*self.population[id][3]

        #deault maxi
        max_id=0
        max_value=actions_value[0]
        for i in range(1,self.numActions):
            if actions_value[i]>max_value:
                max_value=actions_value[i]
                max_id=i
        if max_value==0:
            max_id=None
        return max_id


    ################   Correct Set   ##################
    def getCorrectSet(self,action,match_Set):
        
        Correct_Numerosity=0
        correct_set=[]
        
        num_stamp=0.0
        average_stamp=0.0
        for id in match_Set:
            #1 action
            if self.population[id][1]==action:
                correct_set.append(id)
                #2 numerosity
                Correct_Numerosity+=self.population[id][2]
                #2 numerosity* 7 timestampGA
                num_stamp +=self.population[id][2]*self.population[id][7]


        # calculate the average of the time stamps in the correct set
        average_stamp=num_stamp/float(Correct_Numerosity)
        return correct_set,Correct_Numerosity,average_stamp

    ################   Update Set   ##################
    def Update_Match_Set(self, Match_Set, Correct_Set,Correct_Numerosity):
        for id in Match_Set:
            #update experience
            # 9 match count
            self.population[id][9]+=1

            #update action set size
            if self.population[id][9]<1.0/self.con.beta:
                #5 aveActionSetSize
                # (aveActionSetSize * (matchCount-1)+ matchSetSize) / float(matchCount)
                self.population[id][5]= (self.population[id][5]*(self.population[id][9]-1)+Correct_Numerosity) / float(self.population[id][9])
            else:
                #aveActionSetSize + cons.beta * (matchSetSize - aveActionSetSize)
                self.population[id][5]=self.population[id][5]+self.con.beta*(Correct_Numerosity-self.population[id][5])

            #update correct
            if id in Correct_Set:
                # 10 correct count
                self.population[id][10]+=1

            #update Accuracy
            #4 accuracy
            # correctCount / matchCount
            self.population[id][4]=self.population[id][10]/ float(self.population[id][9])

            #update fitness
            #3 fitness
            #pow(accuracy, nu)
            self.population[id][3]=pow(self.population[id][4],self.con.nu)

    ################ Deletion #######################
    def getDelProp(self, meanFitness,id):
        #  Returns the vote for deletion of the classifier.
        #  3 fitness 2 numerosity 9 match count
        # fitness/numerosity >= cons.delta*meanFitness or self.matchCount < cons.theta_del:
        if self.population[id][3]/self.population[id][2] >= self.con.delta * meanFitness or self.population[id][9] <self.con.theta_del:
            #6 deletionvote ,5 aveActionSetSize
            # deletionVote = aveActionSetSize*numerosity
            self.population[id][6]=self.population[id][5]*self.population[id][2]
        #fitness==0
        elif self.population[id][3]==0.0:
            #aveActionSetSize * numerosity * meanFitness / (cons.init_fit/numerosity)
            self.population[id][6]=self.population[id][5]*self.population[id][2]*meanFitness/(self.con.init_fit/self.population[id][2])
        else:
            # aveActionSetSize * numerosity * meanFitness / (fitness/numerosity)
            self.population[id][6]=self.population[id][5]*self.population[id][2]*meanFitness/(self.population[id][3]/self.population[id][2])
        return self.population[id][6]


    def deleteFromPopulation(self,fitness_sum,size):
        # Deletes one classifier in the population.  The classifier that will be deleted is chosen by roulette wheel selection
        # considering the deletion vote. Returns the macro-classifier which got decreased by one micro-classifier. 
        mean_fitness=fitness_sum/float(self.microPopSize)

        #Calculate total wheel size
        sumCl = 0.0
        voteList = []
        for id in range(0,len(self.population)):
            vote = self.getDelProp(mean_fitness,id)
            sumCl += vote
            voteList.append(vote)

        #Determine the choice point
        choice_list=[]
        while len(choice_list)!=size:
            choicePoint = sumCl * random.random() 
            if not choicePoint in choice_list:
                choice_list.append(choicePoint)

        #choice_list.sort()
        #print choice_list

        exe_time=0
        remove_id_list=[]

        while exe_time!=size:
            countSum=0.0
            

            for id in range(0,len(voteList)):

                countSum += voteList[id]

                if countSum > choice_list[exe_time]: #Select classifier for deletion
                    
                    #Delete classifier
                    #decrease numerosity(2) 1
                    if not id in remove_id_list:
                        exe_time+=1
                        self.population[id][2]-=1
                        #decrease micro size
                        self.microPopSize -= 1
                        # When all micro-classifiers for a given classifier have been depleted.
                        if self.population[id][2] < 1: 
                            remove_id_list.append(id)
                        break
                    else:
                        # in case conflit
                        choice_list[exe_time]=sumCl * random.random() 
                        break

        count=0
        remove_id_list.sort()

        #print (remove_id_list)

        if len(remove_id_list) > 0:
            for remove_id in remove_id_list:
                self.population.pop(remove_id-count)
                count+=1


    #maintain the size of the population
    def Deletion(self,fitness_sum):
        size=self.microPopSize-self.N
        if size>0:
            self.deleteFromPopulation(fitness_sum,size)


    ################### Genetic Algorithm ##############
    def runGA(self, exploreIter, state, phenotype,average_stamp,correct_set): 
        #Judge whether the correct set meet the requirements for activating the GA?
        #Not frequently active the GA?
        if (exploreIter - average_stamp) < self.con.theta_GA:  
            return 

        #update all correct set's time stamp
        for i in correct_set:
            self.population[i][7]=exploreIter


        if self.con.selectionMethod==0:
            parents=self.selectClassifierRWheel(correct_set)
        elif self.con.selectionMethod==1:
            parents=self.selectClassifierTournament(correct_set)
            #print (correct_set)
            #print (parents)
        changed=False

        c1=copy.deepcopy(self.population[parents[0]][0])
        c2=copy.deepcopy(self.population[parents[1]][0])

        if parents[0]!=parents[1]:
            if random.random() < self.con.chi:
                changed=self.Uniform_crossover(c1,c2)

        #condition
        changed=self.Mutation_Condition(c1,state,changed)
        changed=self.Mutation_Condition(c2,state,changed)

        #action
        changed,A1=self.Mutation_Action(self.population[parents[0]][1],changed)
        changed,A2=self.Mutation_Action(self.population[parents[1]][1],changed)



        if changed:
            #print ('=================================')
            #print (c1,A1)
            #print (c2,A2)

            #print (self.population[parents[0]][0],self.population[parents[0]][1])
            
            #print (self.population[parents[1]][0],self.population[parents[0]][1])
            if self.con.doGASubsumption:
                self.subsume_classifier(parents,c1,A1,correct_set,exploreIter)
                self.subsume_classifier(parents,c2,A2,correct_set,exploreIter)
            else:
                self.Add_rule_population(c1,A1,exploreIter)
                self.Add_rule_population(c2,A2,exploreIter)

    #roulette wheel
    def selectClassifierRWheel(self,correct_set):
        #Selects parents using roulette wheel selection according to the fitness of the classifiers. 
        select_list=[]
        for i in range(0,2):
            select_list.append(None)


        if len(correct_set)==1:
            #parents
            select_list[0]=correct_set[0]
            select_list[1]=correct_set[0]
        elif len(correct_set)==2:
            select_list[0]=correct_set[0]
            select_list[1]=correct_set[1]
        elif len(correct_set)==0:
            print('ERROR')
        else:
            #print(correct_set)
            candidate_list=copy.deepcopy(correct_set)
            exe_time=0

            while exe_time!=2:
                #get fitness sum
                fit_sum=0.0
                for i in candidate_list:
                    #3 fitness
                    fit_sum+=self.population[i][3]

                choicePoint = fit_sum * random.random() 

                countSum=0.0
                for id in candidate_list:
                    #3 fitness
                    countSum += self.population[id][3]
                    if countSum >choicePoint:
                        select_list[exe_time]=id
                        exe_time+=1
                        break

                candidate_list.remove(select_list[exe_time-1])


        #print (select_list)
        return select_list

    
    # tournament selection
    def selectClassifierTournament(self,correct_set):
        select_list=[]
        #initial parents
        for i in range(0,2):
            select_list.append(None)

        exe_id=0

        while exe_id<2:
            Size = int(len(correct_set)*self.con.theta_sel)
            if Size<1:
                Size=1

            candidate_List=random.sample(correct_set,Size)

            best_id=candidate_List[0]
            #3 fitness
            best_fit=self.population[best_id][3]

            for i in range(1,len(candidate_List)):
                if self.population[candidate_List[i]][3]>best_fit:
                    best_id=candidate_List[i]
                    #3 fitness
                    best_fit=self.population[best_id][3]
            select_list[exe_id]=best_id
            exe_id+=1
        return select_list

    #Uniform_crossover
    def Uniform_crossover(self,c1,c2):
        changed=False
        for i in range(0,len(c1)):
            if random.random() < 0.5:
                changed=True
                temp=c1[i]
                c1[i]=c2[i]
                c2[i]=temp
        return changed

    #Mutation
    def Mutation_Condition(self,c1,state,changed):

        for i in range(0,len(c1)):
            if random.random()<self.con.upsilon:
                changed=True
                if c1[i]!='#':
                    c1[i]='#'
                else:
                    c1[i]=state[i]
        return changed

    #Initial action list
    def Initial_Action_List(self):
        a_list=[]
        for i in range(0,self.numActions):
            a_list.append(i)
        return a_list

    #Mutation Action
    def Mutation_Action(self,action,changed):
        result=action

        if random.random()<self.con.upsilon:
            changed=True
            use_list=copy.deepcopy(self.Action_list)
            use_list.remove(action)
            result=random.sample(use_list,1)[0]
        return changed, result


    ################### Subsumption Algorithm ##############
    def isSubsumer(self,id):
        # Returns True if the classifieris a possible subsumer.
        #matchcount 9 Accuracy 4 
        if self.population[id][9] > self.con.theta_sub and self.population[id][4] > self.con.acc_sub: 
            return True
        return False

    #check whether gener rule is more gener
    def Is_More_general_Subsumption(self,gener_condition,specific_condition):
         for i in range(0,len(gener_condition)):
             if gener_condition[i] !='#' and gener_condition[i]!=specific_condition[i]:
                 return False
         return True


    def subsumeable(self,gener_id,specifi_condition,specific_action):
        if self.population[gener_id][1]==specific_action:
            if self.isSubsumer(gener_id):
                if self.Is_More_general_Subsumption(self.population[gener_id][0],specifi_condition):
                    return True
        return False

    def subsume_classifier(self,parents,c1,a1,correct_set,explorId):
        #parents
        for parent in parents:
            if self.subsumeable(parent,c1,a1):
                self.microPopSize+=1
                #2 numerosity
                self.population[parent][2]+=1
                return

        #correct set
        ref_set=[]
        for id in correct_set:
            if not id in parents:
                if self.subsumeable(id,c1,a1):
                    ref_set.append(id)
        if len(ref_set)>0:
            use_id=random.sample(ref_set,1)[0]
            self.microPopSize+=1
            #2 numerosity
            self.population[use_id][2]+=1
            return

        self.Add_rule_population(c1,a1,explorId)

    #judge whether two condition is same
    def Is_Same_Condition(self,c1,c2):
        for i in range(0,len(c1)):
            if c1[i] != c2[i]:
                return False
        return True

    def FindIdenticalClassifier(self,c1,a1):
        for id in range(0,len(self.population)):
            # action 1
            if self.population[id][1]==a1:
                #condition 2
                if self.Is_Same_Condition(c1,self.population[id][0]):
                    #numerosity 2
                    self.population[id][2]+=1
                    self.microPopSize+=1
                    return id
        return None

    def Add_rule_population(self,c1,a1,explorId):
        Exist_id=self.FindIdenticalClassifier(c1,a1)
        if Exist_id !=None:
            return
        new_rule=self.Create_new_Single_Rule(c1,a1,explorId)
        self.microPopSize+=1
        self.population.append(new_rule)
        

    ################### Print Population  ##############
    def Print_Population(self):
        for id in range(0,len(self.population)):
            #print(self.population[id][0],':',self.population[id][1],"Num:",self.population[id][2],
            #      "Fit:", round(self.population[id][3],2),"Acc:", round(self.population[id][4],2))

            print(self.population[id][0],':',self.population[id][1],"Exp:",self.population[id][9],
                  "Fit:", round(self.population[id][3],2),"Acc:", round(self.population[id][4],2))

    def Rank_Population_Numerosity(self):
        self.population=sorted(self.population,key=lambda x:(x[2]), reverse=True)

    ################### Save Performance  ##############
    def Covert_To_String(self):
        self.Rank_Population_Numerosity()
        F_result=''
        for id in range(0,len(self.population)):
            result=''
            condition=''
            for cod in self.population[id][0]:
                condition+=str(cod)+' '

            result+=condition
            result+='->'+str(self.population[id][1])+' '
            for i in range(2,len(self.population[id])):
                if isinstance( self.population[id][i],float):
                    result+=str( round( self.population[id][i],2))+' '
                else:
                    result+=str( self.population[id][i])+' '
            F_result+=result+'\n'
        return F_result

    def save_performance(self,txt,name):
        f=open(name,'wb')
        f.write(txt.encode())
        f.close()

    def GetTimer(self):
        local_time= time.localtime(time.time())
        format_time=time.strftime('DAY: %Y-%m-%d  Time: %H : %M : %S',local_time)
        #print format_time
        #print local_time
        Year= local_time[0]
        Month=local_time[1]
        day=local_time[2]
        Hour= local_time[3]
        Min= local_time[4]
        second= local_time[5]
        return format_time,Hour,Min,second,Year,Month,day

    def Generate_Store_Name(self):
        F,H,M,S,Ye,Mo,Da=self.GetTimer()
        file_type='.txt'
        if self.IsLinux==False:
            name='Result/'+self.env.problems_involved[self.Problem_Id]+'_'+str(
            self.Problem_Length)+'_'+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        else:
            name=os.getcwd()+'/Parallel_XCS/Result/'+self.env.problems_involved[self.Problem_Id]+'_'+str(
            self.Problem_Length)+'_'+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        return name

    def Generate_Store_Name_Accuracy(self):
        F,H,M,S,Ye,Mo,Da=self.GetTimer()
        file_type='.txt'
        if self.IsLinux==False:
            name='Result/'+self.env.problems_involved[self.Problem_Id]+'ACCU_'+str(
            self.Problem_Length)+'_'+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        else:
            name=os.getcwd()+'/Parallel_XCS/Result/'+self.env.problems_involved[self.Problem_Id]+'ACCU_'+str(
            self.Problem_Length)+'_'+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        return name
    def Covert_To_String_Accuracy(self):
        result=''
        for accu in self.Training_Performance:
            result+=str(accu)+' '
        result+='\n'
        return result

    def Save(self):
        Name=self.Generate_Store_Name()
        result=self.Covert_To_String()
        self.save_performance(result,Name)
        acc_Name=self.Generate_Store_Name_Accuracy()
        acc_result=self.Covert_To_String_Accuracy()
        self.save_performance(acc_result,acc_Name)

    ####################   BEGIN UCS   ######################
    def Start(self):
        for i in range(0,self.maxLearningIterations):
            if self.Problem_Id<4:
                #Boolean domain
                state=self.env.Create_Set_condition(self.Problem_Length)
                action=self.env.executeAction_supervisor(self.Problem_Id,state)
            else:
                #Real domain
                state,action=self.env.Real_random_state_action()


            Match_Set,fitness_sum=self.getMatchSet(state,action,0)
            Correct_Set,correct_numerosity,average_stamp=self.getCorrectSet(action,Match_Set)

            self.Update_Match_Set(Match_Set,Correct_Set,correct_numerosity)

            P_A=self.Prediction(Match_Set)
            if P_A==action:
                self.correct_track[i%self.trackingFrequency]=1
            else:
                self.correct_track[i%self.trackingFrequency]=0

            self.runGA(i, state, action,average_stamp,Correct_Set)

            self.Deletion(fitness_sum)

            if i % self.trackingFrequency==0:
                correct_rate=round(1.0*sum(self.correct_track)/self.trackingFrequency,2)
                self.Training_Performance.append(correct_rate)
                print (correct_rate,'%')
                
        #self.Rank_Population_Numerosity()
        self.Save()
        #self.Print_Population()
        print(len(self.population))
 
#Proble Tyoe, problem length, action number   
U=UCS(7,None,None)