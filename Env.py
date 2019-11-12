import random
import math
import os

class environment:
    def __init__(self,maxipayoff):
        self.multiplexer_posbits=[1,2,3,4,5,6,7,8,9,10,11]
        self.multiplexer_length=[3,6,11,20,37,70,135,264,521,1034,2059]
        self.problems_involved=['MUX','Carry','Parity','Majority','ZOO','Audiology','Balance','Breast_Cancer','Congressional_Voting','balloon1'
                             ,'balloon2','balloon3','balloon4','soybean_small','tumor','Splice_junction_Gene_Sequences','Promoter_Gene_Sequences','monk1','monk2',
                             'monk3']
        self.maxPayOff=maxipayoff
        self.Is_LinuX=False
        #Real Value
        self.state=None
        self.actions=None
        self.real_length=None
        self.real_actions=None

     #Create a state
    def Create_Set_condition(self,length):
        state=[0]*length
        for i in range(0, length):
            random_number=random.randint(0,1)
            if(random_number==0):
                state[i]=0
            else:
                state[i]=1
        return state

    # generate multiplexer result
    def execute_Multiplexer_Action(self,state):
        actual_Action=0
        length=len(state)
        post_Bits=1
        for number in range(0,len(self.multiplexer_length)):
            if length==self.multiplexer_length[number]:
                post_Bits=self.multiplexer_posbits[number]
        place=post_Bits
        for i in range(0,post_Bits):
            if state[i]==1:
                place=place+int(math.pow(2.0,float(post_Bits-1-i)))
                #print place
        if state[place]==1:
            actual_Action=1
        return actual_Action

    # generate carry result
    def execute_Carry_Action(self,state):
        carry=0
        actual_Action=0
        half_condition=int(len(state)/2)
        for i in range(0, half_condition):
            carry=int((carry+int(state[half_condition-1-i])+int(state[half_condition-1-i+half_condition]))/2)
  
        
        if carry==1:
            actual_Action=1
        return actual_Action

    # generate even parity result
    def execute_Even_parity_Action(self,state):
        numbers=0
        actual_Action=0
        for i in range(0,len(state)):
            if state[i]==1:
                numbers=numbers+1
        if numbers%2==0:
            actual_Action=1
        return actual_Action

    # generate the majority on result
    def execute_Majority_On_Action(self,state):
        actual_Action=0
        Numbers=0
        for i in range(0,len(state)):
            if(state[i]==1):
                Numbers=Numbers+1
        if Numbers>(len(state)/2):
            actual_Action=1
        return actual_Action

    # This function is for reinforcement learning     
    def executeAction(self, exenumber,state,action):
        ret=0
        #['multiplexer','carry', 'evenParity', 'majorityOn']
        if exenumber==0:
            #result=self.execute_Multiplexer_Action(state)
            result=self.execute_Multiplexer_Action(state)
        elif exenumber==1:
            #result=self.execute_Carry_Action(state)
            result=self.execute_Carry_Action(state)
        elif exenumber==2:
            result=self.execute_Even_parity_Action(state)
        elif exenumber==3:
            #result=self.execute_Majority_On_Action(state)
            result=self.execute_Majority_On_Action(state)

        if result==action:
            ret=self.maxPayOff
        return ret

    def Read_Information(self,path):
        read_information=open(path,'r')
        information=[]
        for lines in read_information:
            if lines != '' and lines !='\n':
             information.append(lines)
        return information 


    def global_Zoo(self):
        attribute=16
        datas=[]
        actions=[]
        raw_information=self.Read_Information('R_env\\Zoo.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(',')
            #print first_inf
            actions.append( int(first_inf[-1])-1)
            temp=[]
            for i in range(1,len(first_inf)-1):
                temp.append(float(first_inf[i]))
            datas.append(temp)

        return actions,datas

    def executeAction_supervisor(self, exenumber,state):
        #['multiplexer','carry', 'evenParity', 'majorityOn']
        if exenumber==0:
            #result=self.execute_Multiplexer_Action(state)
            result=self.execute_Multiplexer_Action(state)
        elif exenumber==1:
            #result=self.execute_Carry_Action(state)
            result=self.execute_Carry_Action(state)
        elif exenumber==2:
            result=self.execute_Even_parity_Action(state)
        elif exenumber==3:
            #result=self.execute_Majority_On_Action(state)
            result=self.execute_Majority_On_Action(state)

        
        return result

    def Initial_Real_Value(self,exenumber):
        if exenumber==4:
            self.real_length=16
            self.real_actions=7
            self.actions, self.state=self.global_Zoo()
            self.Initial_Action_Set_candidate_Real()
        elif exenumber==5:
            self.real_length=69
            self.real_actions=24
            self.actions, self.state=self.global_Audiology()
            self.Initial_Action_Set_candidate_Real()
            #print self.action_value_candidate
            #print len(self.action_value_candidate)
        elif exenumber==6:
            self.real_length=4
            self.real_actions=3
            self.actions, self.state=self.global_Balance()
            self.Initial_Action_Set_candidate_Real()
            #print self.action_value_candidate
            #print len(self.action_value_candidate)
            #print self.actions
            #print self.state
        elif exenumber==7:
            self.real_length=9
            self.real_actions=2
            self.actions, self.state=self.global_Breast_Cancer()
            self.Initial_Action_Set_candidate_Real()
        elif exenumber==8:
            self.real_length=16
            self.real_actions=2
            self.actions, self.state=self.global_Congressional_Voting()
            self.Initial_Action_Set_candidate_Real()
        #balloon_1
        elif exenumber==9:
            self.real_length=4
            self.real_actions=2
            self.actions, self.state=self.global_balloon_1()
            self.Initial_Action_Set_candidate_Real()
        #balloon_2
        elif exenumber==10:
            self.real_length=4
            self.real_actions=2
            self.actions, self.state=self.global_balloon_2()
            self.Initial_Action_Set_candidate_Real()
        #balloon_3
        elif exenumber==11:
            self.real_length=4
            self.real_actions=2
            self.actions, self.state=self.global_balloon_3()
            self.Initial_Action_Set_candidate_Real()
        #balloon_4
        elif exenumber==12:
            self.real_length=4
            self.real_actions=2
            self.actions, self.state=self.global_balloon_4()
            self.Initial_Action_Set_candidate_Real()
        #soybean small
        elif exenumber==13:
            self.real_length=35
            self.real_actions=4
            self.actions, self.state=self.global_soybean_small()
            self.Initial_Action_Set_candidate_Real()
        #tumor
        elif exenumber==14:
            self.real_length=17
            self.real_actions=22
            self.actions, self.state=self.global_Tumor()
            self.Initial_Action_Set_candidate_Real()
        #Splice_junction_Gene_Sequences
        elif exenumber==15:
            self.real_length=60
            self.real_actions=3
            self.actions, self.state=self.global_Splice_junction_Gene_Sequences()
            self.Initial_Action_Set_candidate_Real()
        #Splice_junction_Gene_Sequences
        elif exenumber==16:
            self.real_length=57
            self.real_actions=2
            self.actions, self.state=self.global_Splice_Promoter_Gene_Sequences()
            self.Initial_Action_Set_candidate_Real()
        #monk1
        elif exenumber==17:
            self.real_length=6
            self.real_actions=2
            self.actions, self.state=self.global_monk1()
            self.Initial_Action_Set_candidate_Real()
        #monk2
        elif exenumber==18:
            self.real_length=6
            self.real_actions=2
            self.actions, self.state=self.global_monk2()
            self.Initial_Action_Set_candidate_Real()
        #monk3
        elif exenumber==19:
            self.real_length=6
            self.real_actions=2
            self.actions, self.state=self.global_monk3()
            self.Initial_Action_Set_candidate_Real()


    def Real_random_state_action(self):
        id=random.randint(0,len(self.state)-1)
        return self.state[id], self.actions[id]


    def global_Audiology(self):
        attribute=69
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Audiology.txt')
        else:
            raw_information=self.Read_Information('R_env\\Audiology.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #Balance
    def global_Balance(self):
        attribute=4
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Balance.txt')
        else:
            raw_information=self.Read_Information('R_env\\Balance.txt')

        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas


    def global_Breast_Cancer(self):
        attribute=9
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Breast_Cancer.txt')
        else:
            #Breast_Cancer_Test_9.txt
            #raw_information=self.Read_Information('R_env\\Breast_Cancer.txt')
            
            #raw_information=self.Read_Information('R_env\\Breast_Cancer_Test_9.txt')
            raw_information=self.Read_Information('R_env\\Breast_Cancer_Train_0.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #soybean_small

    #Congressional_Voting
    def global_Congressional_Voting(self):
        attribute=16
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Congressional_Voting.txt')
        else:
            raw_information=self.Read_Information('R_env\\Congressional_Voting.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #Initial an action-set for the real domains' actions
    def Initial_Action_Set_candidate_Real(self):
        value_result=[]
        for i in range(0,self.real_length):
            temp=[]
            value_result.append(temp)


        for j in range(0,len(self.state)):
            #print self.state
            #print len(self.state[j]), self.real_length
            for s_id in range(0,len(self.state[j])):
                if not self.state[j][s_id] in value_result[s_id] and self.state[j][s_id]!='?':
                    value_result[s_id].append(self.state[j][s_id])

        for temp in value_result:
            temp.sort()
        #print (value_result)

        self.action_value_candidate= value_result

   #balloon1
    def global_balloon_1(self):
        attribute=2
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/balloon_1.txt')
        else:
            raw_information=self.Read_Information('R_env\\balloon_1.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

     #balloon2
    def global_balloon_2(self):
        attribute=2
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/balloon_2.txt')
        else:
            raw_information=self.Read_Information('R_env\\balloon_2.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #balloon3
    def global_balloon_3(self):
        attribute=2
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/balloon_3.txt')
        else:
            raw_information=self.Read_Information('R_env\\balloon_3.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #balloon4
    def global_balloon_4(self):
        attribute=2
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/balloon_4.txt')
        else:
            raw_information=self.Read_Information('R_env\\balloon_4.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #soybean_small
    def global_soybean_small(self):
        attribute=35
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/soybean_small.txt')
        else:
            raw_information=self.Read_Information('R_env\\soybean_small.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #Tumor
    def global_Tumor(self):
        attribute=17
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/tumor.txt')
        else:
            raw_information=self.Read_Information('R_env\\tumor.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #Splice_junction_Gene_Sequences
    def global_Splice_junction_Gene_Sequences(self):
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Splice_junction_Gene_Sequences.txt')
        else:
            raw_information=self.Read_Information('R_env\\Splice_junction_Gene_Sequences.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas


    #Promoter_Gene_Sequences
    def global_Splice_Promoter_Gene_Sequences(self):
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/Promoter_Gene_Sequences.txt')
        else:
            raw_information=self.Read_Information('R_env\\Promoter_Gene_Sequences.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #monk1
    def global_monk1(self):
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/monk1.txt')
        else:
            raw_information=self.Read_Information('R_env\\monk1.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas

    #monk2
    def global_monk2(self):
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/monk2.txt')
        else:
            raw_information=self.Read_Information('R_env\\monk2.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas


        #monk3
    def global_monk3(self):
        datas=[]
        actions=[]
        if self.Is_LinuX:
            raw_information=self.Read_Information(os.getcwd()+'/Parallel_CXCS_V2/R_env/monk3.txt')
        else:
            raw_information=self.Read_Information('R_env\\monk3.txt')
        for raw_inf in raw_information:
            first_inf= raw_inf.split('\n')[0].split(' ')
            #print len(first_inf)

            actions.append( int(first_inf[-1]))
            temp=[]
            for i in range(0,len(first_inf)-1):
                if first_inf[i] !='?':
                    temp.append(int(first_inf[i]))
                else:
                    temp.append(first_inf[i])
            datas.append(temp)

        #print actions
        #print datas
        return actions,datas
class create_global_instance:
    def __init__(self,length):
        self.inputs=[[0]*length for i in range(2**length)]
        for i in range(2**length):
            value=i
            divisor=2**length
            #fill the input bits
            for j in range(length):
                divisor/=2
                if value >=divisor:
                    self.inputs[i][j]=1
                    value -=divisor
        #print (self.inputs)

#Env=environment(None)
#Env.execute_Real_Value(4)

class Real_Environment_Simper:
    def __init__(self,Address):
        self.actions=None
        self.states=None
        self.Address=Address
        #self.save_name='Result\\Audiology.txt'
        #self.save_name='Result\\Congressional_Voting.txt'
        #self.save_name='Result\\Balance.txt'
        #self.save_name='Result\\balloon_1.txt'
        #self.save_name='Result\\balloon_2.txt'
        #self.save_name='Result\\balloon_3.txt'
        #self.save_name='Result\\balloon_4.txt'
        #self.save_name='Result\\Breast_Cancer.txt'
        #self.save_name='Result\\Promoter_Gene_Sequences.txt'
        #self.save_name='Result\\Splice_junction_Gene_Sequences.txt'
        #self.save_name='Result\\soybean_small.txt'
        #self.save_name='Result\\tumor.txt'
        #self.save_name='Result\\monk1.txt'
        #self.save_name='Result\\monk2.txt'
        self.save_name='Result\\monk3.txt'


        #self.Read_Audiology()
        #self.Read_Congressional()
        #self.Read_Balance()
        #self.Read_Balloon()
        #self.Read_BreastCancer()
        #self.Read_Promoter_Gene_Sequences()
        #self.Read_Splice_junction_Gene_Sequences()
        #self.Read_soybean_small()
        #self.Read_tumor()
        #self.creat_Monk_1()
        #self.creat_Monk_2()
        self.creat_Monk_3()
        #self.action_value_candidate=None
        self.Save()
        print('finish')

    def save_performance(self,txt,name):
        f=open(name,'wb')
        f.write(txt.encode())
        f.close()

    def Read_Information(self,path):
        read_information=open(path,'r')
        information=[]
        for lines in read_information:
            if lines != '' and lines !='\n':
             information.append(lines)
        return information 

    def conver_string(self):
        result=''
        for i in range(0,len(self.states)):
            line=''
            for stat in self.states[i]:
                line+=str(stat)+' '
            line+=str(self.actions[i])+'\n'
            result+=line
        return result

    def Save(self):
        save_txt=self.conver_string()
        self.save_performance(save_txt,self.save_name)

    ######## Audiology ##############
    def Read_Audiology(self):
        actions=[]
        Attribute_list=[1,3,4,5,7,58,59,63,65]
        state_list=[]
        #attribute_list=['']
        Raw_Information=self.Read_Information(self.Address)

        
        #print Raw_Information[0]
        for i in range(0, len(Raw_Information)):
            raw_Inf=Raw_Information[i].split('\n')[0].split(',')
            #print raw_Inf[7]
            actions.append(self.Audiology_Action(raw_Inf[70]))
            stats= raw_Inf[0:69]
            state=[]
            for j in range(0,69):
                state.append(self.Audiology_state(j,stats[j]))

            state_list.append(state)

        
        self.actions= actions
        self.states= state_list
        #print len(self.states)
        #print len(self.actions)
        
        """
        raw_Inf=Raw_Information[7].split('\n')[0].split(',')
        for i in range(0,len( raw_Inf)):
            if raw_Inf[i]!='f' and raw_Inf[i]!='t':
                print(i, raw_Inf[i])
        """

    def Audiology_Action(self,description):
        if description=='acoustic_neuroma':
            return 0
        elif description=='bells_palsy':
            return 1
        elif description=='cochlear_age':
            return 2
        elif description=='cochlear_age_and_noise':
            return 3
        elif description=='cochlear_age_plus_poss_menieres':
            return 4
        elif description=='cochlear_noise_and_heredity':
            return 5
        elif description=='cochlear_poss_noise':
            return 6
        elif description=='cochlear_unknown':
            return 7
        elif description=='conductive_discontinuity':
            return 8
        elif description=='conductive_fixation':
            return 9
        elif description=='mixed_cochlear_age_fixation':
            return 10
        elif description=='mixed_cochlear_age_otitis_media':
            return 11
        elif description=='mixed_cochlear_age_s_om':
            return 12
        elif description=='mixed_cochlear_unk_discontinuity':
            return 13
        elif description=='mixed_cochlear_unk_fixation':
            return 14
        elif description=='mixed_cochlear_unk_ser_om':
            return 15
        elif description=='mixed_poss_central_om':
            return 16
        elif description=='mixed_poss_noise_om':
            return 17
        elif description=='normal_ear':
            return 18
        elif description=='otitis_media':
            return 19
        elif description=='poss_central':
            return 20
        elif description=='possible_brainstem_disorder':
            return 21
        elif description=='possible_menieres':
            return 22
        elif description=='retrocochlear_unknown':
            return 23
        


    def Audiology_FT(self,value):
        if value=='f':
            return 0
        elif value=='t':
            return 1
        else:
            return value


    def Audiology_air(self,value):
        #	mild,moderate,severe,normal,profound
        if value=='mild':
            return 0
        elif value=='moderate':
            return 1
        elif value=='severe':
            return 2
        elif value=='normal':
            return 3
        elif value=='profound':
            return 4
        else:
            return value


    def Audiology_ar_c(self,value):
        if value=='normal':
            return 0
        elif value=='elevated':
            return 1
        elif value=='absent':
            return 2
        else:
            return value


    def Audiology_ar_u(self,value):
        if value=='normal':
            return 0
        elif value=='absent':
            return 1
        elif value=='elevated':
            return 2
        else:
            return value

    def Audiology_bone(self,value):
        if value=='mild':
            return 0
        elif value=='moderate':
            return 1
        elif value=='normal':
            return 2
        elif value=='unmeasured':
            return 3
        else:
            return value


    def Audiology_bser(self,value):
         if value=='normal':
            return 0
         elif value=='degraded':
            return 1
         else:
            return value


    def Audiology_o_ar_c(self,value):
         if value=='normal':
            return 0
         elif value=='elevated':
            return 1
         elif value=='absent':
            return 2
         else:
            return value

    def Audiology_o_ar_u(self,value):
         if value=='normal':
            return 0
         elif value=='absent':
            return 1
         elif value=='elevated':
            return 2
         else:
            return value


    #speech():	normal,good,very_good,very_poor,poor,unmeasured. 
    #tymp():	a,as,b,ad,c. 
    def Audiology_speech(self,value):
         if value=='normal':
            return 0
         elif value=='good':
            return 1
         elif value=='very_good':
            return 2
         elif value=='very_poor':
            return 3
         elif value=='poor':
            return 4
         elif value=='unmeasured':
            return 5
         else:
            return value

    def Audiology_tymp(self,value):
         if value=='a':
            return 0
         elif value=='as':
            return 1
         elif value=='b':
            return 2
         elif value=='ad':
            return 3
         elif value=='c':
            return 4
         else:
            return value

    def Audiology_state(self,id,value):
        Attribute_list=[1,3,4,5,7,58,59,63,65]
        if id==1:
            return self.Audiology_air(value)
        elif id==3:
            return self.Audiology_ar_c(value)
        elif id==4:
            return self.Audiology_ar_u(value)
        elif id==5:
            return self.Audiology_bone(value)
        elif id==7:
            return self.Audiology_bser(value)
        elif id==58:
            return self.Audiology_o_ar_c(value)
        elif id==59:
            return self.Audiology_o_ar_u(value)
        elif id==63:
            return self.Audiology_speech(value)
        elif id==65:
            return self.Audiology_tymp(value)
        else:
            return self.Audiology_FT(value)


    def Initial_Action_Set_candidate_Real(self):
        value_result=[]
        for i in range(0,self.real_length):
            temp=[]
            value_result.append(temp)

        for j in range(0,len(self.state)):
            for s_id in range(0,len(self.state[j])):
                if not self.state[j][s_id] in value_result[s_id] and self.state[j][s_id]!='?':
                    value_result[s_id].append(self.state[j][s_id])

        for temp in value_result:
            temp.sort()
        #print (value_result)

        self.action_value_candidate= value_result

    ######## Congressional Voting ##############

    def Read_Congressional(self):
        actions=[]
        state_list=[]
        #attribute_list=['']
        Raw_Information=self.Read_Information(self.Address)

        
        #print Raw_Information[0]
        for i in range(0, len(Raw_Information)):
            raw_Inf=Raw_Information[i].split('\n')[0].split(',')
            #print raw_Inf[7]
            actions.append(self.Congression_action(raw_Inf[0]))
            #stats= raw_Inf[0:17]
            state=[]
            for j in range(1,17):
                state.append(self.Congression_NY_convert(raw_Inf[j]))

            state_list.append(state)

        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list
        #print actions
        #print self.actions

    def Congression_NY_convert(self,value):
        if value=='n':
            return 0
        elif value=='y':
            return 1
        else:
            return value

    def Congression_action(self,value):
        if value=='republican':
            return 0
        elif value=='democrat':
            return 1
        else:
            return value

    ######## Balance ##############
    def Read_Balance(self):
        actions=[]
        state_list=[]
        #attribute_list=['']
        Raw_Information=self.Read_Information(self.Address)

        
        #print Raw_Information[0]
        for i in range(0, len(Raw_Information)):
            raw_Inf=Raw_Information[i].split('\n')[0].split(',')
            #print raw_Inf
            actions.append(self.Balance_convert_action(raw_Inf[0]))
            #stats= raw_Inf[0:17]
            state=[]
            for j in range(1,5):
                #print j
                state.append(int(raw_Inf[j]))

            state_list.append(state)

        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list
        #print actions
        #print self.actions

    def Balance_convert_action(self,value):
        if value=='L':
            return 0
        elif value=='B':
            return 1
        elif value=='R':
            return 2
        else:
            return value

    ######## Balloon ##############
    def Read_Balloon(self):
        actions=[]
        state_list=[]
        #attribute_list=['']
        Raw_Information=self.Read_Information(self.Address)

        
        #print Raw_Information[0]
        for i in range(0, len(Raw_Information)):
            raw_Inf=Raw_Information[i].split('\n')[0].split(',')
            #print raw_Inf
            actions.append(self.Balloon_convert_action(raw_Inf[4]))
            #stats= raw_Inf[0:17]
            state=[]
            state.append(self.Balloon_color(raw_Inf[0]))
            state.append(self.Balloon_size(raw_Inf[1]))
            state.append(self.Balloon_act(raw_Inf[2]))
            state.append(self.Balloon_age(raw_Inf[3]))

            state_list.append(state)

        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list

    def Balloon_convert_action(self,value):
        if value=='T':
            return 1
        elif value=='F':
            return 0

    def Balloon_color(self,value):
        if value=='YELLOW':
            return 0
        elif value=='PURPLE':
            return 1
        else:
            return value

    def Balloon_size(self,value):
        if value=='LARGE':
            return 0
        elif value=='SMALL':
            return 1
        else:
            return value

    def Balloon_act(self,value):
        if value=='STRETCH':
            return 0
        elif value=='DIP':
            return 1
        else:
            return value

    def Balloon_age(self,value):
        if value=='ADULT':
            return 0
        elif value=='CHILD':
            return 1
        else:
            return value

    ######## Breast Cancer ##############
    def Read_BreastCancer(self):
        actions=[]
        state_list=[]
        #attribute_list=['']
        Raw_Information=self.Read_Information(self.Address)

        
        #print Raw_Information[0]
        for i in range(0, len(Raw_Information)):
            raw_Inf=Raw_Information[i].split('\n')[0].split(',')
            #print raw_Inf
            actions.append(self.BreastCancer_convert_action(raw_Inf[0]))
            #stats= raw_Inf[0:17]
            state=[]
            state.append(self.BreastCancer_age(raw_Inf[1]))
            state.append(self.BreastCancer_menopause(raw_Inf[2]))
            state.append(self.BreastCancer_tumor_size(raw_Inf[3]))
            state.append(self.BreastCancer_inv_nodes(raw_Inf[4]))
            state.append(self.BreastCancer_node_caps(raw_Inf[5]))
            state.append(self.BreastCancer_deg_malig(raw_Inf[6]))
            state.append(self.BreastCancer_breast(raw_Inf[7]))
            state.append(self.BreastCancer_breast_quad(raw_Inf[8]))
            state.append(self.BreastCancer_irradiat(raw_Inf[9]))

            state_list.append(state)

        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list

    def BreastCancer_convert_action(self,value):
        if value=='no-recurrence-events':
            return 0
        elif value=='recurrence-events':
            return 1
        else:
            return value

    def BreastCancer_age(self,value):
        if value=='10-19':
            return 0
        elif value=='20-29':
            return 1
        elif value=='30-39':
            return 2
        elif value=='40-49':
            return 3
        elif value=='50-59':
            return 4
        elif value=='60-69':
            return 5
        elif value=='70-79':
            return 6
        elif value=='80-89':
            return 7
        elif value=='90-99':
            return 8
        else:
            return value

    def BreastCancer_menopause(self,value):
        if value=='lt40':
            return 0
        elif value=='ge40':
            return 1
        elif value=='premeno':
            return 2
        else:
            return value

    def BreastCancer_tumor_size(self,value):
        if value=='0-4':
            return 0
        elif value=='5-9':
            return 1
        elif value=='10-14':
            return 2
        elif value=='15-19':
            return 3
        elif value=='20-24':
            return 4
        elif value=='25-29':
            return 5
        elif value=='30-34':
            return 6
        elif value=='35-39':
            return 7
        elif value=='40-44':
            return 8
        elif value=='45-49':
            return 9
        elif value=='50-54':
            return 10
        elif value=='55-59':
            return 11
        else:
            return value

    def BreastCancer_inv_nodes(self,value):
        if value=='0-2':
            return 0
        elif value=='3-5':
            return 1
        elif value=='6-8':
            return 2
        elif value=='9-11':
            return 3
        elif value=='12-14':
            return 4
        elif value=='15-17':
            return 5
        elif value=='18-20':
            return 6
        elif value=='21-23':
            return 7
        elif value=='24-26':
            return 8
        elif value=='27-29':
            return 9
        elif value=='30-32':
            return 10
        elif value=='33-35':
            return 11
        elif value=='36-39':
            return 12
        else:
            return value

    def BreastCancer_node_caps(self,value):
        if value=='yes':
            return 0
        elif value=='no':
            return 1
        else:
            return value


    def BreastCancer_deg_malig(self,value):
        if value=='1':
            return 0
        elif value=='2':
            return 1
        elif value=='3':
            return 2
        else:
            return value

    def BreastCancer_breast(self,value):
        if value=='left':
            return 0
        elif value=='right':
            return 1
        else:
            return value

    def BreastCancer_breast_quad(self,value):
        if value=='left_up':
            return 0
        elif value=='left_low':
            return 1
        elif value=='right_up':
            return 2
        elif value=='right_low':
            return 3
        elif value=='central':
            return 4
        else:
            return value

    def BreastCancer_irradiat(self,value):
        if value=='yes':
            return 0
        elif value=='no':
            return 1
        else:
            return value


    ######## Promoter Gene Sequences ##############
    def Read_Promoter_Gene_Sequences(self):
        actions=[]
        state_list=[]
        #attribute_list=['']
        Raw_Information=self.Read_Information(self.Address)

        
        #print Raw_Information[0]
        for i in range(0, len(Raw_Information)):
            raw_Inf=Raw_Information[i].split('\n')[0].split(',')
            #print raw_Inf
            actions.append(self.Promoter_Gene_Sequences_convert_action(raw_Inf[0]))
            #stats= raw_Inf[0:17]
            art_inf=raw_Inf[2].replace('\t','')
            
            state=[]
            for piece in art_inf:
                if piece=='a':
                    state.append(0)
                elif piece=='t':
                    state.append(1)
                elif piece=='c':
                    state.append(2)
                elif piece=='g':
                    state.append(3)
                else:
                    state.append(piece)

            #print len(state)
            state_list.append(state)

        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list

    def Promoter_Gene_Sequences_convert_action(self,value):
        if value=='+':
            return 0
        elif value=='-':
            return 1
        else:
            return value

    ##############Splice_junction_Gene_Sequences############################
    def Read_Splice_junction_Gene_Sequences(self):
        actions=[]
        state_list=[]
        #attribute_list=['']
        Raw_Information=self.Read_Information(self.Address)

        
        #print Raw_Information[0]
        for i in range(0, len(Raw_Information)):
            raw_Inf=Raw_Information[i].split('\n')[0].split(',')
            #print raw_Inf
            actions.append(self.Splice_junction_Gene_Sequences_convert_action(raw_Inf[0]))
            #stats= raw_Inf[0:17]
            art_inf=raw_Inf[2].replace(' ','')
           
            state=[]
            
            for piece in art_inf:
                if piece=='A':
                    state.append(0)
                elif piece=='T':
                    state.append(1)
                elif piece=='C':
                    state.append(2)
                elif piece=='G':
                    state.append(3)
                elif piece=='D':
                    state.append(4)
                elif piece=='N':
                    state.append(5)
                elif piece=='S':
                    state.append(6)
                elif piece=='R':
                    state.append(7)
                else:
                    state.append(piece)

            #print(len(state))
            #print state
            state_list.append(state)

        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list

    def Splice_junction_Gene_Sequences_convert_action(self,value):
        if value=='EI':
            return 0
        elif value=='IE':
            return 1
        elif value=='N':
            return 2
        else:
            return value
    
    ######## soybean_smalls ##############
    def Read_soybean_small(self):
        actions=[]
        state_list=[]
        #attribute_list=['']
        Raw_Information=self.Read_Information(self.Address)

        
        #print Raw_Information[0]
        for i in range(0, len(Raw_Information)):
            raw_Inf=Raw_Information[i].split('\n')[0].split(',')
            #print raw_Inf
            actions.append(self.soybean_small_convert_action(raw_Inf[35]))
            stats= raw_Inf[0:35]
            #print stats
            state=[]
            for j in range(0,len(stats)):
                state.append(int(stats[j]))


            state_list.append(state)

        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list

    def soybean_small_convert_action(self,value):
        if value=='D1':
            return 0
        elif value=='D2':
            return 1
        elif value=='D3':
            return 2
        elif value=='D4':
            return 3
        else:
            return value

    ######## tumor ##############
    def Read_tumor(self):
        actions=[]
        state_list=[]
        #attribute_list=['']
        Raw_Information=self.Read_Information(self.Address)

        
        #print Raw_Information[0]
        for i in range(0, len(Raw_Information)):
            raw_Inf=Raw_Information[i].split('\n')[0].split(',')
            print raw_Inf
            actions.append(int(raw_Inf[0])-1)
            stats= raw_Inf[1:18]
            #print stats
            state=[]
            for j in range(0,len(stats)):
                if stats[j]!='?':
                    state.append(int(stats[j]))
                else:
                    state.append(stats[j])
            

            state_list.append(state)

        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list

    ####### Monk problem #################
    def creat_Monk_1(self):
        actions=[]
        state_list=[]
        for lev1 in range(1,4):
            for lev2 in range(1,4):
                for lev3 in range(1,3):
                    for lev4 in range(1,4):
                        for lev5 in range(1,5):
                            for lev6 in range(1,3):
                                state=[]
                                state.append(lev1)
                                state.append(lev2)
                                state.append(lev3)
                                state.append(lev4)
                                state.append(lev5)
                                state.append(lev6)
                                state_list.append(state)
                                if lev1==lev2 or lev5==1:
                                    actions.append(1)
                                else:
                                    actions.append(0)
        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list

    def creat_Monk_2(self):
        actions=[]
        state_list=[]
        for lev1 in range(1,4):
            for lev2 in range(1,4):
                for lev3 in range(1,3):
                    for lev4 in range(1,4):
                        for lev5 in range(1,5):
                            for lev6 in range(1,3):
                                state=[]
                                count=0
                                state.append(lev1)
                                state.append(lev2)
                                state.append(lev3)
                                state.append(lev4)
                                state.append(lev5)
                                state.append(lev6)
                                state_list.append(state)
                                if lev1==1:
                                    count+=1
                                if lev2==1:
                                    count+=1
                                if lev3==1:
                                    count+=1
                                if lev4==1:
                                    count+=1
                                if lev5==1:
                                    count+=1
                                if lev6==1:
                                    count+=1

                                if count==2:
                                    actions.append(1)
                                else:
                                    actions.append(0)
        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list

    def creat_Monk_3(self):
        actions=[]
        state_list=[]
        for lev1 in range(1,4):
            for lev2 in range(1,4):
                for lev3 in range(1,3):
                    for lev4 in range(1,4):
                        for lev5 in range(1,5):
                            for lev6 in range(1,3):
                                state=[]
                                count=0
                                state.append(lev1)
                                state.append(lev2)
                                state.append(lev3)
                                state.append(lev4)
                                state.append(lev5)
                                state.append(lev6)
                                state_list.append(state)


                                if (lev5==3 and lev4==1) or (lev5!=4 and lev2!=3):
                                    actions.append(1)
                                else:
                                    actions.append(0)
        #print actions
        #print state_list
        self.actions= actions
        self.states= state_list

#address='R_env\\Audiology.txt'
#address='R_env\\Congressional_Voting.txt'
#address='R_env\\Balance.txt'
#address='R_env\\balloon_1.txt'
#address='R_env\\balloon_2.txt'
#address='R_env\\balloon_3.txt'
#address='R_env\\balloon_4.txt'
#address='R_env\\Breast_Cancer.txt'
address='R_env\\Promoter_Gene_Sequences.txt'
#address='R_env\\Splice_junction_Gene_Sequences.txt'
#address='R_env\\soybean_small.txt'

#address='R_env\\tumor.txt'
RES=Real_Environment_Simper(address)