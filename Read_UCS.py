import os


class Read_UCS:
    def __init__(self,Address):
        self.population=[]
        self.micro_size=0
        self.Read(Address)
        
        #self.Print_Population()
        #print (self.micro_size)

    def Create_new_Single_Rule(self,condition,action,numerosity,fit,acc,Ssize,D_V,match_c,correct_c):
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
        rule.append(numerosity) #2 numerosity
        rule.append(fit) #3 fitness
        rule.append(acc) #4 accuracy
        rule.append(Ssize) #5 aveActionSetSize
        rule.append(D_V) #6 deletionvote
        rule.append(1) #7 timeStampGA
        rule.append(1) # 8 initiTieStamp
        rule.append(match_c) # 9 match count
        rule.append(correct_c) # 10 correct count

        return rule


    def Read_Information(self,address):
        read_information=open(address,'r')
        information=[]
        for lines in read_information:
            if lines != '' and lines !='\n':
             information.append(lines)
        #print (information)
        return information

    def Read(self,address):
        informations=self.Read_Information(address)
        for infor in informations:
            raw= infor.split('\n')[0].split('->')
            condition=raw[0]
            condition=self.read_condition(condition)
            #actions and parameters
            a_p=raw[1]
            val=self.read_details(a_p)
            rule=self.Create_new_Single_Rule(condition,val[0],val[1],val[2],val[3],val[4],val[5],val[8],val[9])
            self.micro_size+=val[1]
            self.population.append(rule)

    def read_condition(self,condition_list):
        conditions=condition_list.split(' ')[0:-1]
        condition=[]
        for cod in conditions:
            if cod!='#':
                if not '.' in cod:
                    condition.append(int(cod))
                else:
                    condition.append(float(cod))
            else:
                condition.append(cod)
        #print condition
        return condition

    def read_details(self,a_p):
        s_values=a_p.split(' ')[0:-1]

        a_p_list=[]
        for val in s_values:
            if '.' in val:
                a_p_list.append(float(val))
            else:
                a_p_list.append(int(val))

        #print a_p_list
        return a_p_list

    ################### Print Population  ##############
    def Print_Population(self):
        for id in range(0,len(self.population)):
            print(self.population[id][0],':',self.population[id][1],"Num:",self.population[id][2],
                  "Fit:", round(self.population[id][3],2),"Acc:", round(self.population[id][4],2))

            #print(self.population[id][0],':',self.population[id][1],"Exp:",self.population[id][9],
            #      "Fit:", round(self.population[id][3],2),"Acc:", round(self.population[id][4],2))
#add='Result\\MUX_62018_11_7_16_18_18.txt'
#UCS=Read_UCS(add)

class Read_UCS_Sets:
    def __init__(self,address):
        self.population_list=[]
        self.Read(address)
        #print(len(self.population_list))

    #judge is the file exist
    def Is_File_Exist(self,file_Name):
        return os.path.exists(file_Name)


    def GetFileList(self,path,type):
        FileList=[]
        FindPath=path
        if self.Is_File_Exist(FindPath):
            FileNames=os.listdir(FindPath)
            for i in FileNames:
                if type in i:
                    FileList.append(path+'\\'+i)
        return FileList

    def Read(self,address):
        read_list=self.GetFileList(address,'.txt')
        for add in read_list:
            UCS=Read_UCS(add)
            self.population_list.append(UCS.population)

#add='Result'
#UCSs=Read_UCS_Sets(add)

class Read_Natural_UCS_Solution:
    def __init__(self,address):
        self.address=address
        self.population=[]
        self.Read()
        #self.read_population()
        print len(self.population)

    def Read_Information(self,address):
        read_information=open(address,'r')
        information=[]
        for lines in read_information:
            if lines != '' and lines !='\n':
             information.append(lines)
        #print (information)
        return information

    def Read(self):
        informations=self.Read_Information(self.address)
        for raw in informations:
            extracted= raw.split('\n')[0].split('-->')
            action=int(extracted[1].split(' ')[-1])
            condition=extracted[0].split(' ')[0:-1]
            for i in range(0,len(condition)):
                if condition[i]!='#':
                    if not '.' in condition[i]:
                        condition[i]=int(condition[i])
                    else:
                        condition[i]=float(condition[i])
            rule=self.create_rule(condition,action)
            self.population.append(rule)
         


    def create_rule(self,condition,action):
        rule=[]
        rule.append(condition)
        rule.append(action)
        return rule

    def read_population(self):
        for rule in self.population:
            print rule


#add='Natural_Solution\\6_MUX.txt'
#RNU=Read_Natural_UCS_Solution(add)
class Read_XCS_Absumption:
    def __init__(self,Address):
        self.population=[]
        self.micro_size=0
        self.Read(Address)
        #self.Print_Population()

    def Create_new_Single_Rule(self,condition,action,numerosity,acc,fit,P_E,Pre,Exp,Ssize,N_P,P_P):
        # States of Attributes Specified in classifier (Ternary)
        # 0: condition 
        #class
        # 1: action 
        # The number of rule copies stored in the population.  (Indirectly stored as incremented numerosity)
        # 2: numerosity
        
        # Classifier accuracy - Accuracy calculated using only instances in the dataset which this rule matched.
        # 3: accuracy
        # Classifier fitness - initialized to a constant initial fitness value 
        # 4: fitness
       
       
        # 5: Prediction Error
        # The Error of the prediction.
        # 6: Prediction
        # The prediction 0 minimum 1000 maximum.
        # 7: Experience
        # Trained times.
        # 8: AxtionSetSize
        # Niches
        # 9: Negative prediction
        # The total number of times this classifier was in a incorrect set
        # 10 Positive prediction
        #The total number of times this classifier was in a correct set
        rule=[]
        rule.append(condition) #0 condition
        rule.append(action) #1 action
        rule.append(numerosity) #2 numerosity
        rule.append(acc) #3 Accuracy
        rule.append(fit) #4 Fitness
        rule.append(P_E) #5 Prediction Error
        rule.append(Pre) #6 Prediction
        rule.append(Exp) #7 Experience
        rule.append(Ssize) # 8 ActionSetSize
        rule.append(N_P) # 9 Negative Prediction
        rule.append(P_P) # 10 Positive Prediction

        return rule

    def Read_Information(self,address):
        read_information=open(address,'r')
        information=[]
        for lines in read_information:
            if lines != '' and lines !='\n':
             information.append(lines)
        #print (information)
        return information

    def Read(self,address):
        informations=self.Read_Information(address)
        for infor in informations:
            raw= infor.split('\n')[0].split(' ----> ')
            #print raw
            condition_action=raw[0].split(' : ')
            #print condition_action
            condition=self.read_condition(condition_action[0])
            action=int(condition_action[1])
            #print condition,len(condition)
            


            parameters=raw[1]
            
            val=self.read_details(parameters)
            rule=self.Create_new_Single_Rule(condition,action,val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7],val[8])
            self.micro_size+=val[1]
            self.population.append(rule)

    """
    #read the condition part
    def read_condition(self,condition_list):
        conditions=condition_list.split('.')
        r_condition=[]
        for i in range(0,len(conditions)):
            if i >0:
                for j in range(1,len(conditions[i])):
                    if conditions[i][j]!='#':
                        r_condition.append(int(conditions[i][j]))
                    else:
                        r_condition.append(conditions[i][j])
            else:
                for j in range(0,len(conditions[i])):
                    if conditions[i][j]!='#':
                        r_condition.append(int(conditions[i][j]))
                    else:
                        r_condition.append(conditions[i][j])


        #print (r_condition)
        return r_condition
     """
    def read_condition(self,condition_list):
        conditions=condition_list.split('.')
        r_condition=[]
        for i in range(0,len(conditions)):
            if i >0:
                for j in range(1,len(conditions[i])):
                    if conditions[i][j]!='#':
                        r_condition.append(int(conditions[i][j]))
                    else:
                        r_condition.append(conditions[i][j])
            else:
                for j in range(0,len(conditions[i])):
                    if conditions[i][j]!='#':
                        r_condition.append(int(conditions[i][j]))
                    else:
                        r_condition.append(conditions[i][j])


        #print (r_condition)
        return r_condition

    #read the parameters
    def read_details(self,parameters):
        P_values=parameters.split(' ')
        parameters_list=[]

        parameter_list=[1,3,5,8,10,12,14,16,18]
        a_p_list=[]
        s_values=[]
        for i in range(0,len(P_values)):
            if i in parameter_list:
                s_values.append(P_values[i])
        for val in s_values:
            if '.' in val:
                a_p_list.append(float(val))
            else:
                a_p_list.append(int(val))

        return a_p_list

     ################### Print Population  ##############
    def Print_Population(self):
        for id in range(0,len(self.population)):
            print(self.population[id][0],':',self.population[id][1],"Num:",self.population[id][2],
                  "Fit:", round(self.population[id][4],2),"Acc:", round(self.population[id][3],2))

#add='Check_Boolean\\ZOO_XCS\\XCS_45598a9f_15e3_4393_b4e4_da00bc199dfdAgent_ded54b4e_710c_4cc8_95ee_c5c21c5cfa5bProblem_ZOOPlength_6FTime_DAY__2018_11_23__Time__03___19___55.txt'
#Read_XCS_Absumption(add)

class Read_XCS_Absumption_Sets:
    def __init__(self,address):
        self.population_list=[]
        self.Read(address)
        #print(len(self.population_list))

    def Is_File_Exist(self,file_Name):
        return os.path.exists(file_Name)


    def GetFileList(self,path,type):
        FileList=[]
        FindPath=path
        if self.Is_File_Exist(FindPath):
            FileNames=os.listdir(FindPath)
            for i in FileNames:
                if type in i:
                    FileList.append(path+'\\'+i)
        return FileList

    def Read(self,address):
        read_list=self.GetFileList(address,'.txt')
        for add in read_list:
            XCS_A=Read_XCS_Absumption(add)
            self.population_list.append(XCS_A.population)

#add='Check_Boolean\\ZOO_XCS'
#Read_XCS_Absumption_Sets(add)

class Read_XCS_Standard:
    def __init__(self,Address):
        self.population=[]
        self.micro_size=0
        self.Read(Address)
        #self.Print_Population()

    def Create_new_Single_Rule(self,condition,action,numerosity,acc,fit,P_E,Pre,Exp,Ssize):
        # States of Attributes Specified in classifier (Ternary)
        # 0: condition 
        #class
        # 1: action 
        # The number of rule copies stored in the population.  (Indirectly stored as incremented numerosity)
        # 2: numerosity
        
        # Classifier accuracy - Accuracy calculated using only instances in the dataset which this rule matched.
        # 3: accuracy
        # Classifier fitness - initialized to a constant initial fitness value 
        # 4: fitness
       
       
        # 5: Prediction Error
        # The Error of the prediction.
        # 6: Prediction
        # The prediction 0 minimum 1000 maximum.
        # 7: Experience
        # Trained times.
        # 8: AxtionSetSize
        # Niches
        # 9: Negative prediction
        # The total number of times this classifier was in a incorrect set
        # 10 Positive prediction
        #The total number of times this classifier was in a correct set
        rule=[]
        rule.append(condition) #0 condition
        rule.append(action) #1 action
        rule.append(numerosity) #2 numerosity
        rule.append(acc) #3 Accuracy
        rule.append(fit) #4 Fitness
        rule.append(P_E) #5 Prediction Error
        rule.append(Pre) #6 Prediction
        rule.append(Exp) #7 Experience
        rule.append(Ssize) # 8 ActionSetSize
        rule.append(0) # 9 Negative Prediction
        rule.append(0) # 10 Positive Prediction

        return rule

    def Read_Information(self,address):
        read_information=open(address,'r')
        information=[]
        for lines in read_information:
            if lines != '' and lines !='\n':
             information.append(lines)
        #print (information)
        return information

    def Read(self,address):
        informations=self.Read_Information(address)
        for infor in informations:
            raw= infor.split('\n')[0].split(' ----> ')
            condition_action=raw[0].split(' : ')
            condition=self.read_condition(condition_action[0])
            action=int(condition_action[1])
            #print condition,len(condition)
            


            parameters=raw[1]
            
            val=self.read_details(parameters)
            rule=self.Create_new_Single_Rule(condition,action,val[0],val[1],val[2],val[3],val[4],val[5],val[6])
            self.micro_size+=val[1]
            self.population.append(rule)

    #read the condition part
    def read_condition(self,condition_list):
        conditions=condition_list.split('.')
        r_condition=[]
        for i in range(0,len(conditions)):
            if i >0:
                for j in range(1,len(conditions[i])):
                    if conditions[i][j]!='#':
                        r_condition.append(float(conditions[i][j]))
                    else:
                        r_condition.append(conditions[i][j])
            else:
                for j in range(0,len(conditions[i])):
                    if conditions[i][j]!='#':
                        r_condition.append(float(conditions[i][j]))
                    else:
                        r_condition.append(conditions[i][j])


        return r_condition


    #read the parameters
    def read_details(self,parameters):
        P_values=parameters.split(' ')
        parameters_list=[]

        parameter_list=[1,3,5,8,10,12,14]
        a_p_list=[]
        s_values=[]
        for i in range(0,len(P_values)):
            if i in parameter_list:
                s_values.append(P_values[i])
        for val in s_values:
            if '.' in val:
                a_p_list.append(float(val))
            else:
                a_p_list.append(int(val))

        return a_p_list

     ################### Print Population  ##############
    def Print_Population(self):
        for id in range(0,len(self.population)):
            print(self.population[id][0],':',self.population[id][1],"Num:",self.population[id][2],
                  "Fit:", round(self.population[id][4],2),"Acc:", round(self.population[id][3],2))

#add='Check_Boolean\\ZOO_XCS_Standard\\XCS_45598a9f_15e3_4393_b4e4_da00bc199dfdAgent_6914c4c6_8522_4343_80d2_5ea4005f34f8Problem_ZOOPlength_6FTime_DAY__2018_11_23__Time__02___51___10.txt'
#Read_XCS_Standard(add)

class Read_XCS_Standard_Sets:
    def __init__(self,address):
        self.population_list=[]
        self.Read(address)
        #print(len(self.population_list))

    def Is_File_Exist(self,file_Name):
        return os.path.exists(file_Name)


    def GetFileList(self,path,type):
        FileList=[]
        FindPath=path
        if self.Is_File_Exist(FindPath):
            FileNames=os.listdir(FindPath)
            for i in FileNames:
                if type in i:
                    FileList.append(path+'\\'+i)
        return FileList

    def Read(self,address):
        read_list=self.GetFileList(address,'.txt')
        for add in read_list:
            XCS_A=Read_XCS_Standard(add)
            self.population_list.append(XCS_A.population)

#add='Check_Boolean\\ZOO_XCS_Standard'
#Read_XCS_Standard_Sets(add)

