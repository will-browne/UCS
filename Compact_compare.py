from Read_UCS import Read_UCS
from Read_UCS import Read_UCS_Sets
from Env import environment
from Env import create_global_instance
import copy
from Time_Record import Time_Calculate
import time

class compare_compacted_Method:
    def __init__(self,add,Problem_Id,problem_length,action_num,problem_name):
        self.Problem_Id=Problem_Id
        self.problem_name=problem_name
        self.action_num=action_num
        self.address=add

        self.env=environment(1000)
        self.IsLinux=False
        if self.IsLinux==True:
            self.address=os.getcwd()+'/UCS/'+add
            RUS=Read_UCS_Sets(self.address)
            self.TC=Time_Calculate()
            self.population_list=RUS.population_list
        else:
            RUS=Read_UCS_Sets(self.address)
            self.TC=Time_Calculate()
            self.population_list=RUS.population_list
            

        if Problem_Id<4:
            CGI=create_global_instance(problem_length)
            self.states=CGI.inputs
            self.actions=[]
            for stat in self.states:
                self.actions.append(self.env.executeAction_supervisor(self.Problem_Id,stat))
        else:
            self.env.Initial_Real_Value(Problem_Id)
            self.states=self.env.state
            self.actions=self.env.actions

    
        #self.Compared_Test(1)
        self.Global_Test()
    #add additional column
    def Add_additional_column_list(self,population):
        for rule in population:
            temp=[]
            #11 correct match
            temp_1=[]
            #12 incorrect match
            c_size=0
            #13 correct match size
            Ic_size=0
            #14 incorrect match size
            match_size=0
            #15 match size

            #16 entropy value
            rule.append(temp)
            rule.append(temp)
            rule.append(c_size)
            rule.append(Ic_size)
            rule.append(match_size)


    #Judge whether condition is matched
    def isConditionMatched(self,condition,state):
        for i in range(0,len(condition)):
            if condition[i]!='#' and condition[i] != state[i]:
                return False
        return True

    #review the training_set
    def Review_all_train_instance(self,population):

        self.Add_additional_column_list(population)

        for id in range(0,len(self.states)):
            for rule in population:
                #0 condition
                if self.isConditionMatched(rule[0],self.states[id]):
                    if self.Problem_Id<4:
                        action=self.env.executeAction_supervisor(self.Problem_Id,self.states[id])
                        if action==rule[1]:
                            rule[11].append(id)
                        else:
                            rule[12].append(id)
                    else:
                        action=self.env.actions[id]
                        if action==rule[1]:
                            rule[11].append(id)
                        else:
                            rule[12].append(id)

        for rule in population:
            #correct size
            rule[13]=len(rule[11])
            #incorrect size
            rule[14]=len(rule[12])
            rule[15]=rule[13]+rule[14]

    #get the match set
    def getMatchSet(self,state,population):
        match_set=[]
        #print "begin"
        for i in range(0,len(population)):
            #0: condition
            if(self.isConditionMatched(population[i][0],state)):
                #add matching classifier to the matchset
                match_set.append(i)
        return match_set

    def Prediction(self,match_set,population):
        actions_value=[]
        for i in range(0,self.action_num):
            actions_value.append(0)

        for id in match_set:
            #1: action 2:numerosity 3: # 3: fitness
            actions_value[population[id][1]]+=population[id][2]*population[id][3]

        #deault maxi
        max_id=0
        max_value=actions_value[0]
        for i in range(1,self.action_num):
            if actions_value[i]>max_value:
                max_value=actions_value[i]
                max_id=i
        if max_value==0:
            max_id=None
        return max_id

    def Accuracy_Test(self,population):
        correct=0
        for id in range(0,len(self.states)):
            Match_Set=self.getMatchSet(self.states[id],population)
            P_action=self.Prediction(Match_Set,population)
            if self.Problem_Id<4:
                action=self.env.executeAction_supervisor(self.Problem_Id,self.states[id])
            else:
                action=self.env.actions[id]

            if P_action==action:
                correct+=1
        accu=1.0*correct/len(self.states)
        return accu

    def Run_All_Accu(self):
        for population in self.population_list:
            print(self.Accuracy_Test(population))
        
    def Review_training_set(self):
        for population in self.population_list:
            self.Review_all_train_instance(population)

    def Compared_Test(self,exeid):
        size=[]
        accuracy=[]
        u_time=[]
            
        for population in self.population_list:
            if exeid==0:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.CRA_OLD(population)
                accuracy.append(acc)
                #f_siz=1.0*siz/len(population)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==1:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.Dixon(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==2:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.UCRA(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==3:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.Fu_Method(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==4:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.CRA_F(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==5:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.Entropy_Based(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==6:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.QCRA(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==7:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.QuickRuleCleanup(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==8:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.Experimental_App(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==9:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.CRA(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==10:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.Fu_1(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==11:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.Fu_2(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
            elif exeid==12:
                format_time_2,Hour_2,Min_2,second_2,day_2=self.TC.startTimer()
                acc,siz,c_population=self.Fu_3(population)
                accuracy.append(acc)
                size.append(siz)
                self.print_population(c_population)
                format_time_1,Hour_1,Min_1,second_1,day_1=self.TC.startTimer()
                r_time=self.TC.elapsed(Hour_1,Hour_2,Min_1,Min_2,second_1,second_2,day_1,day_2)
                u_time.append(r_time)
        mins,maxs=self.Max_Min(size)
        avg=round(1.0*sum(size)/len(size),2)
        size.append(mins)
        size.append(maxs)
        size.append(avg)

        mins,maxs=self.Max_Min(accuracy)
        avg=round(1.0*sum(accuracy)/len(accuracy),2)
        accuracy.append(mins)
        accuracy.append(maxs)
        accuracy.append(avg)

        mins,maxs=self.Max_Min(u_time)
        avg=round(1.0*sum(u_time)/len(u_time),2)
        u_time.append(mins)
        u_time.append(maxs)
        u_time.append(avg)

        result=self.convert_tostring(accuracy,size,u_time,exeid)
        print('accuracy',1.0*sum(accuracy)/len(accuracy))
        print('size[',mins,maxs,']',1.0*sum(size)/len(size))
        print(u_time)
        return result

    def Global_Test(self):
        result=''
        #test_ids=[0,1,2,3,8]
        test_ids=[12]
        for i in range(0,15):
            if i in test_ids:
                piece_result=self.Compared_Test(i)
                result+=piece_result
                RUS=Read_UCS_Sets(self.address)
                self.population_list=RUS.population_list
            #print(piece_result)
        #print (result)
        name=self.Generate_Store_Name()
        self.save_performance(result,name)

    # A CRA based approach introduced by Fu 2000. The first two stages are the same as Fu's approach. The third stage first use how
    #    many samples a rule matched to rank the rule. Then the covering is done based on the ranking. The ranking list is not updated each
    #    time some samples are covered and removed from the training set. """

    def CRA_OLD(self,population):
        print('==================================')
        print(len(population))
        #2 numerosity
        population.sort(key=lambda x:x[2],reverse=True)

        original_accu=self.Accuracy_Test(population)
        
        go_on=True
        #stage 1
        #remove rules according to the numerosity from highest to lowest
        #while accuracy do not decrease
        while go_on:
            #print population[0]
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<original_accu:
                go_on=False
                population.append(hold_rule)

        #stage 2 select rule which can influence the accuracy
        refaccu=original_accu
        com_population=[]
        for i in range(0,len(population)):
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<refaccu:
                refaccu=new_accuracy
                com_population.append(hold_rule)

        #stage 3
        self.Review_all_train_instance(com_population)
        com_population.sort(key=lambda x:x[15],reverse=True)
        ref_accu=self.Accuracy_Test(com_population)
        for i in range(0,len(com_population)):
            hold_rule=com_population[-1]
            com_population.pop()
            new_accuracy=self.Accuracy_Test(com_population)
            if new_accuracy<ref_accu:
                com_population.insert(0,hold_rule)
            else:
                ref_accu=new_accuracy


        final_acc=self.Accuracy_Test(com_population)
        print (final_acc)
        print (len(com_population))
        return final_acc, len(com_population),com_population

    def print_population(self,population):
        for rule in population:
            print (rule[0],rule[1])

    
    def Max_Min(self,a_list):
         min=100000000000
         max=-10000000000
         for inf in a_list:
             if inf<min:
                 min=inf
             if inf>max:
                 max=inf
         return min, max   

    # This approach is based on Dixon's method. For each sample, form a match set and then a correct set. The most useful rule in 
    #        the correct set is moved into the final ruleset. In this approach, the most useful rule has the largest product of accuracy
    #        and generality.

    def Dixon(self,population):
        print('==================================')
        print('CRA2')
        print(len(population))
        selected_ids=[]
        for i in range(0,len(self.states)):
            
            M_Set=self.getMatchSet(self.states[i],population)
            C_Set=[]
            #form the correct id
            for id in M_Set:
                #1 action
                if self.Problem_Id<4:
                    action=self.env.executeAction_supervisor(self.Problem_Id,self.states[i])
                else:
                    action=self.env.actions[i]
                if population[id][1]==action:
                    C_Set.append(id)

            best_score=-100
            best_Id=None

            for c_id in C_Set:
                #4 accuracy, #0condition
                general_level=(1.0*self.Calculate_general_level(population[c_id][0])/len(population[c_id][0]))
                score=population[c_id][4]*general_level
                if score>best_score:
                    best_score=score
                best_Id=c_id

            if best_Id!=None: 
                if not best_Id in selected_ids:
                   selected_ids.append(best_Id)

        c_population=[]
        for id in selected_ids:
            c_population.append(population[id])

        acc=self.Accuracy_Test(c_population)
        size=len(c_population)
        print ('accuracy: ',acc)
        print ('size: ',size)
        return acc, size, c_population

    # This approach is based on Dixon's approach, called UCRA in the paper. For each sample, form a match set and then a correct set. 
    #    The most useful rule in the correct set is moved into the final ruleset. In this approach, the most useful rule has the largest 
    #    product of accuracy, numerosity and generality.
    def UCRA(self,population):
        print('==================================')
        print(len(population))
        selected_ids=[]
        for i in range(0,len(self.states)):
            
            M_Set=self.getMatchSet(self.states[i],population)
            C_Set=[]
            #form the correct id
            for id in M_Set:
                #1 action
                if self.Problem_Id<4:
                    action=self.env.executeAction_supervisor(self.Problem_Id,self.states[i])
                else:
                    action=self.env.actions[i]
                if population[id][1]==action:
                    C_Set.append(id)

            best_score=-100
            best_Id=None

            for c_id in C_Set:
                #4 accuracy, #0condition #2numerosity
                general_level=(1.0*self.Calculate_general_level(population[c_id][0])/len(population[c_id][0]))
                score=population[c_id][4]*general_level*population[c_id][2]
                if score>best_score:
                    best_score=score
                best_Id=c_id

            if best_Id!=None: 
                if not best_Id in selected_ids:
                    selected_ids.append(best_Id)

        c_population=[]
        for id in selected_ids:
            c_population.append(population[id])

        acc=self.Accuracy_Test(c_population)
        size=len(c_population)
        print ('accuracy: ',acc)
        print ('size: ',size)
        return acc, size, c_population

    # calculate a rule' condition' general level
    def Calculate_general_level(self,condition):
        result=0
        for cod in condition:
            if cod=='#':
                result+=1

        return result

    #This approach completely follows Fu's second approach. All three stages use accuracy to sort rules.
    def Fu_Method(self,population):
        print('==================================')
        print(len(population))
        #2 numerosity
        population.sort(key=lambda x:x[2],reverse=True)

        original_accu=self.Accuracy_Test(population)
        
        go_on=True
        #stage 1
        #remove rules according to the numerosity from highest to lowest
        #while accuracy do not decrease
        while go_on:
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<original_accu:
                go_on=False
                population.append(hold_rule)

        #stage 2 select rule which can influence the accuracy
        refaccu=original_accu
        com_population=[]
        for i in range(0,len(population)):
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<refaccu:
                refaccu=new_accuracy
                com_population.append(hold_rule)

        #stage3

        ref_accu=self.Accuracy_Test(com_population)
        com_population.sort(key=lambda x:x[2],reverse=True)
        for i in range(0,len(com_population)):
            hold_rule=com_population[-1]
            com_population.pop()
            new_accuracy=self.Accuracy_Test(com_population)
            if new_accuracy<ref_accu:
                com_population.insert(0,hold_rule)
            else:
                ref_accu=new_accuracy

        final_acc=self.Accuracy_Test(com_population)
        print (final_acc)
        print (len(com_population))
        return final_acc, len(com_population),com_population


    # A variant of CRA based approach introduced by Fu 2000. The first two stages are the same as Fu's approach. In the third stage,
    #    fitness is used to rank the rules and guide covering. Ranking list is updated each time some samples are covered and removed from 
    def CRA_F(self,population):
        print('==================================')
        print(len(population))
        #2 numerosity
        population.sort(key=lambda x:x[2],reverse=True)

        original_accu=self.Accuracy_Test(population)
        
        go_on=True
        #stage 1
        #remove rules according to the numerosity from highest to lowest
        #while accuracy do not decrease
        while go_on:
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<original_accu:
                go_on=False
                population.append(hold_rule)

        #stage 2 select rule which can influence the accuracy
        refaccu=original_accu
        com_population=[]
        for i in range(0,len(population)):
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<refaccu:
                refaccu=new_accuracy
                com_population.append(hold_rule)

        #stage3

        ref_accu=self.Accuracy_Test(com_population)
        #3 fitness
        com_population.sort(key=lambda x:x[3],reverse=True)
        for i in range(0,len(com_population)):
            hold_rule=com_population[-1]
            com_population.pop()
            new_accuracy=self.Accuracy_Test(com_population)
            if new_accuracy<ref_accu:
                com_population.insert(0,hold_rule)
            else:
                ref_accu=new_accuracy

        final_acc=self.Accuracy_Test(com_population)
        print (final_acc)
        print (len(com_population))
        return final_acc, len(com_population),com_population
    #    the training set. 

    #A method introduced by Kharbat, 2008. Add the rule with the highest entropy to the final compact set. A rule's entropy is
    #    Defined as (correct matched cases - wrong matched cases)/ number of cases.

    def Entropy_Based(self,population):
        print('==================================')
        print(len(population))


        selected_ids=[]

        self.Review_all_train_instance(population)


        for i in range(0,len(self.states)):
            
            M_Set=self.getMatchSet(self.states[i],population)
            C_Set=[]
            #form the correct id
            for id in M_Set:
                #1 action
                if self.Problem_Id<4:
                    action=self.env.executeAction_supervisor(self.Problem_Id,self.states[i])
                else:
                    action=self.env.actions[i]
                if population[id][1]==action:
                    C_Set.append(id)

            best_score=-100
            best_Id=None

            for c_id in C_Set:
                #4 accuracy, #0condition
                general_level=(1.0*self.Calculate_general_level(population[c_id][0])/len(population[c_id][0]))
                #entropy
                score=1.0*(population[c_id][15]-(len(self.states)-population[c_id][15]))/len(self.states)
                if score>best_score:
                    best_score=score
                best_Id=c_id

            if best_Id!=None: 
                if not best_Id in selected_ids:
                    selected_ids.append(best_Id)

        c_population=[]
        for id in selected_ids:
            c_population.append(population[id])

        acc=self.Accuracy_Test(c_population)
        size=len(c_population)
        print ('accuracy: ',acc)
        print ('size: ',size)
        return acc, size, c_population

     # Called QCRA in the paper. It uses fitness to rank rules and guide covering. It's the same as Approach 15, but the code is re-written in 
     #   order to speed up.
    def QCRA(self,population):
        print('==================================')
        print(len(population))

        #3 fitness
        population.sort(key=lambda x:x[3],reverse=True)

        T_state=copy.deepcopy( self.states)

        keep_go=True
        c_population=[]
        #for rule in population:
        #    print rule[0],rule[3]
        while len(T_state)>0 and keep_go:
            new_T_state=[]
            match_count=0
            rule=population[0]
            for state in T_state:
                if self.isConditionMatched(rule[0],state):
                    match_count+=1
                else:
                    new_T_state.append(state)

            if match_count>0:
                c_population.append(rule)

            #remove tested rule
            population.pop(0)

            if len(population)==0:
                keep_go=False

            T_state=copy.deepcopy(new_T_state)

        final_acc=self.Accuracy_Test(c_population)
        print (final_acc)
        print (len(c_population))
        return final_acc, len(c_population),c_population

    #An extremely fast rule compaction strategy. Removes any rule with an accuracy below 50% and any rule that covers only one instance, but specifies more than one attribute
    #     (won't get rid of rare variant rules)
    def QuickRuleCleanup(self,population):
        c_population=[]
        for rule in population:
            #4 accuracy<0.5, general_level>1
            if rule[4]>0.5 and self.Calculate_general_level(rule[0])>0:
                c_population.append(rule)

        acc=self.Accuracy_Test(c_population)
        size=len(c_population)
        print ('accuracy: ',acc)
        print ('size: ',size)
        return acc, size, c_population

    #Experimental Approach: remove likely bad rules without evaluations then follow with standard Training Accuracy Based State 1, 
    #    and 2. 

    def Experimental_App(self,population):
        r_population=[]
        #4 accuracy
        for rule in population:
            if rule[4]>0.8:
                r_population.append(rule)

        population=copy.deepcopy(r_population)

        selected_ids=[]
        for i in range(0,len(self.states)):
            
            M_Set=self.getMatchSet(self.states[i],population)
            C_Set=[]
            #form the correct id
            for id in M_Set:
                #1 action
                if self.Problem_Id<4:
                    action=self.env.executeAction_supervisor(self.Problem_Id,self.states[i])
                else:
                    action=self.env.actions[i]
                if population[id][1]==action:
                    C_Set.append(id)

            best_score=-100
            best_Id=None

            for c_id in C_Set:
                #4 accuracy, #0condition
                general_level=(1.0*self.Calculate_general_level(population[c_id][0])/len(population[c_id][0]))
                score=population[c_id][4]*general_level
                if score>best_score:
                    best_score=score
                best_Id=c_id

            if best_Id!=None: 
                if not best_Id in selected_ids:
                    selected_ids.append(best_Id)

        c_population=[]
        for id in selected_ids:
            c_population.append(population[id])

        acc=self.Accuracy_Test(c_population)
        size=len(c_population)
        print ('accuracy: ',acc)
        print ('size: ',size)
        return acc, size, c_population

    def convert_tostring(self,accuracy,size,time,ID):
        result=str(ID)+' '
        for acc in accuracy:
            result+=str(acc)+' '
        result+='==>'
        for si in size:
            result+=str(si)+' '
        result+='==>'
        for ti in time:
            result+=str(ti)+' '
        result+='\n'
        return result

    def save_performance(self,txt,name):
        f=open(name,'wb')
        f.write(txt.encode())
        f.close()

    def Generate_Store_Name(self):
        F,H,M,S,Ye,Mo,Da=self.GetTimer()
        file_type='.txt'
        if self.IsLinux==False:
            name='Result/'+self.problem_name+'Compact'+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        else:
            name=os.getcwd()+'/Parallel_XCS/Result/'+self.problem_name+'Compact'+str(Ye)+'_'+str(Mo)+'_'+str(Da)+'_'+str(H
            )+'_'+str(M)+'_'+str(S)+file_type
        return name

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

    # A RCA based approach introduced by Will utilize numerosity to rank the rules
    def CRA(self,population):
        print('==================================')
        print('CRA')
        print(len(population))

        #2 numerosity
        population.sort(key=lambda x:x[2],reverse=True)
        #print population[-1]
        original_accu=self.Accuracy_Test(population)
        new_accuracy=0
        
        subset=[]

        #stage 1
        #Find a maximally correct rule-set
        count=0
        while new_accuracy<original_accu and len(subset)<len(population):
            
            subset.append(population[count])
            new_accuracy=self.Accuracy_Test(subset)
            count+=1


        #stage 2 remove rules which is potential redundant
        subset.sort(key=lambda x:x[2],reverse=False)
        #print population[-1]
        refaccu=original_accu
        circle_size=len(subset)
        for i in range(0,circle_size):
            hold_rule=subset[-1]
            subset.pop()
            new_accuracy=self.Accuracy_Test(subset)
            if new_accuracy<refaccu:
                subset.insert(0,hold_rule)

        #stage 3 again remove replaceable rules
        self.Review_all_train_instance(subset)
        #ranked by matched size
        subset.sort(key=lambda x:x[15],reverse=True)

        final_set=[]

        D_set_state=copy.deepcopy(self.states)
        D_set_action=copy.deepcopy(self.actions)

        while len(subset)>0 and len(D_set_state)>0:
            final_set.append(subset[0])
            
            del_list=[]
            for id in range(0,len(D_set_state)):
                if self.isConditionMatched(subset[0],D_set_state[id]):
                    del_list.append(id)

            count=0
            for d_id in del_list:
                D_set_state.pop(d_id-count)
                count+=1
            subset.pop(0)



        final_acc=self.Accuracy_Test(final_set)
        print (final_acc)
        print (len(final_set))
        return final_acc, len(final_set),final_set

    #This approach completely follows Fu's first approach. All three stages use accuracy to sort rules.
    def Fu_1(self,population):
        print('==================================')
        print(len(population))
        print('Fu_1')

        #2 numerosity
        population.sort(key=lambda x:x[2],reverse=True)

        original_accu=self.Accuracy_Test(population)
        
        go_on=True
        #stage 1
        #remove rules according to the numerosity from highest to lowest
        #while accuracy do not decrease
        while go_on:
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<original_accu:
                go_on=False
                population.append(hold_rule)

        #stage 2 select rule which can influence the accuracy
        refaccu=original_accu
        com_population=[]
        for i in range(0,len(population)):
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<refaccu:
                refaccu=new_accuracy
                com_population.append(hold_rule)

        #stage3

        ref_accu=self.Accuracy_Test(com_population)
        #com_population.sort(key=lambda x:x[2],reverse=True)


        final_set=[]

        D_set_state=copy.deepcopy(self.states)
        D_set_action=copy.deepcopy(self.actions)

        while len(com_population)>0 and len(D_set_state)>0:
            final_set.append(com_population[0])
            
            del_list=[]
            for id in range(0,len(D_set_state)):
                if self.isConditionMatched(com_population[0],D_set_state[id]):
                    del_list.append(id)

            count=0
            for d_id in del_list:
                D_set_state.pop(d_id-count)
                count+=1
            com_population.pop(0)



        final_acc=self.Accuracy_Test(final_set)
        print (final_acc)
        print (len(final_set))
        return final_acc, len(final_set),final_set
        return final_acc, len(com_population),com_population

    #This approach completely follows Fu's second approach. All three stages use accuracy to sort rules.
    def Fu_2(self,population):
        print('==================================')
        print(len(population))
        print('Fu_2')

        #2 numerosity
        population.sort(key=lambda x:x[2],reverse=True)

        original_accu=self.Accuracy_Test(population)
        
        go_on=True
        #stage 1
        #remove rules according to the numerosity from highest to lowest
        #while accuracy do not decrease
        while go_on:
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<original_accu:
                go_on=False
                population.append(hold_rule)

        #stage 2 select rule which can influence the accuracy
        refaccu=original_accu
        com_population=[]
        for i in range(0,len(population)):
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<refaccu or hold_rule[2]>1:
                refaccu=new_accuracy
                com_population.append(hold_rule)
            if hold_rule[2]>2:
                population.insert(0,hold_rule)
            

        #stage3

        ref_accu=self.Accuracy_Test(com_population)
        com_population.sort(key=lambda x:x[2],reverse=True)


        final_set=[]

        D_set_state=copy.deepcopy(self.states)
        D_set_action=copy.deepcopy(self.actions)

        while len(com_population)>0 and len(D_set_state)>0:
            final_set.append(com_population[0])
            
            del_list=[]
            for id in range(0,len(D_set_state)):
                if self.isConditionMatched(com_population[0],D_set_state[id]):
                    del_list.append(id)

            count=0
            for d_id in del_list:
                D_set_state.pop(d_id-count)
                count+=1
            com_population.pop(0)



        final_acc=self.Accuracy_Test(final_set)
        print (final_acc)
        print (len(final_set))
        return final_acc, len(final_set),final_set
        return final_acc, len(com_population),com_population


     #This approach completely follows Fu's third approach. All three stages use accuracy to sort rules.
    def Fu_3(self,population):
        print('==================================')
        print(len(population))
        print('Fu_3')

        #2 numerosity
        population.sort(key=lambda x:x[2],reverse=True)

        original_accu=self.Accuracy_Test(population)
        
        go_on=True
        #stage 1
        #remove rules according to the numerosity from highest to lowest
        #while accuracy do not decrease
        while go_on:
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<original_accu:
                go_on=False
                population.append(hold_rule)

        #stage 2 select rule which can influence the accuracy
        refaccu=original_accu
        com_population=[]
        for i in range(0,len(population)):
            hold_rule=population[-1]
            population.pop()
            new_accuracy=self.Accuracy_Test(population)
            if new_accuracy<refaccu or hold_rule[2]>1:
                refaccu=new_accuracy
                com_population.append(hold_rule)
            if hold_rule[2]>2:
                population.insert(0,hold_rule)
            

        #stage3

        #stage3

        ref_accu=self.Accuracy_Test(com_population)
        #3 fitness
        com_population.sort(key=lambda x:x[3],reverse=False)
        for i in range(0,len(com_population)):
            hold_rule=com_population[-1]
            com_population.pop()
            new_accuracy=self.Accuracy_Test(com_population)
            if new_accuracy<ref_accu:
                com_population.insert(0,hold_rule)
            elif new_accuracy>ref_accu:
                ref_accu=new_accuracy

        final_acc=self.Accuracy_Test(com_population)
        print (final_acc)
        print (len(com_population))
        return final_acc, len(com_population),com_population



#address,Problem_Id,problem_length,action_num,problem_name
#add='Check_Boolean/Carry_6'    
#CCM=compare_compacted_Method(add,1,6,2,'6_carry')

add='Check_Boolean/Mux'
CCM=compare_compacted_Method(add,0,6,2,'6_MUX')

#add='Check_Boolean/Majority_6'
#CCM=compare_compacted_Method(add,3,6,2)

#add='Check_Boolean/Majority_8'
#CCM=compare_compacted_Method(add,3,8,2)
