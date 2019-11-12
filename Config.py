class Config:

    def __init__(self,Address):

        # Supervised Learning Parameters -------------------------------------------------------------------------------
        #  Power parameter used to determine the importance of high accuracy when calculating fitness. (typically set to 5, recommended setting of 1 in noisy data)
        self.nu = 5                                                
        #  The probability of applying crossover in the GA. (typically set to 0.5-1.0)
        self.chi = 0.8                                            
        #  The probability of mutating an allele within an offspring.(typically set to 0.01-0.05)
        self.upsilon = 0.04
        # The GA threshold; The GA is applied in a set when the average time since the last GA in the set is greater than theta_GA.                                    
        self.theta_GA = 25                                    
        # The deletion experience threshold; The calculation of the deletion probability changes once this threshold is passed.
        self.theta_del = 20                                 
        # The subsumption experience threshold;
        self.theta_sub = 20                                  
        # Subsumption accuracy requirement
        self.acc_sub = 0.99                                    
        # Learning parameter; Used in calculating average correct set size
        self.beta = 0.2                                          
        # Deletion parameter; Used in determining deletion vote calculation.
        self.delta = 0.1                                        
        # The initial fitness for a new classifier. (typically very small, approaching but not equal to zero)
        self.init_fit = 0.01                                
        # Initial fitness reduction in GA offspring rules.
        self.fitnessReduction = 0.1                  


        # Algorithm Heuristic Options -------------------------------------------------------------------------------
        # Activate Subsumption? (True, False).  Subsumption is a heuristic that actively seeks to increase generalization in the rule population.
        self.doGASubsumption = True               
        self.doCorrectSetSubsumption = False

        # Select GA parent selection strategy (0:'tournament' or 1:'roulette')
        self.selectionMethod = 1                        

        # The fraction of the correct set to be included in tournament selection.
        self.theta_sel = 0.5                                

        # PopulationReboot -------------------------------------------------------------------------------
        # Start UCS from an existing rule population? (1 is True, 0 is False).
        self.doPopulationReboot = False          

        # Path/FileName of previously evolved rule population output file. Include file/pathname up to until 'RulePop.txt', as this is automatically included.
        self.popRebootPath = Address                              

                    


                                          

        
        #Covering alphabet
        self.covering_alphabet='#'