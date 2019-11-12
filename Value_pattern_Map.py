from Read_UCS import Read_Natural_UCS_Solution
import numpy as np
import random
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import os
import matplotlib.lines as mlines
import matplotlib as mpl
import copy

class Value_knowledge:
    def __init__(self,address,action_list):


        Read_UCS=Read_Natural_UCS_Solution(address)

        self.action_list=action_list

        self.Raw_Population=Read_UCS.population

        self.clustered=self.Conver_to_Cluster()

        self.attribute_List=self.Calculate_Attribute_importance_distribution()

        
        
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


    def General_Level(self,condition):
        count=0
        for cod in condition:
            if cod=='#':
                count+=1
        return count

    def Calculate_Attribute_importance_distribution(self):
        
        #Initial the action based distribution list
        distribution_list=[]
        length=len(self.Raw_Population[0][0])
        #print len(self.negative_set)
        for i in range(0,len(self.clustered)):
            temp=[]
            for j in range(0,length):               
                temp.append(0)
            distribution_list.append(temp)

        #Action distributed list
        G_distribution_list=[]
        for i in range(0,len(self.action_list)):
            temp=copy.deepcopy(distribution_list)
            G_distribution_list.append(temp)

        G_count_list=copy.deepcopy(G_distribution_list)

        #Z_count_list=copy.deepcopy(G_distribution_list)

        #Z_distribution_list=copy.deepcopy(G_distribution_list)


        #print distribution_list
        for i in range(0,len(self.clustered)):
            if len(self.clustered[i])!=0:
                for rule in self.clustered[i]:
                    for cond_l in range(0,length):
                        if rule[0][cond_l]!='#':
                            G_distribution_list[rule[1]][i][cond_l]+=rule[0][cond_l]
                            G_count_list[rule[1]][i][cond_l]+=1
                        #elif rule[0][cond_l]==0:

                for d_l in range(0,length):
                    for action in self.action_list:
                        if G_count_list[action][i][d_l]!=0:
                            G_distribution_list[action][i][d_l]=1.0*G_distribution_list[action][i][d_l]/G_count_list[action][i][d_l]
                            if G_distribution_list[action][i][d_l]==0:
                                G_distribution_list[action][i][d_l]=-1
        print (G_distribution_list)
        #print len(distribution_list)



        return G_distribution_list




class Visualize_value_pattern:
    def __init__(self,address,action_list,path):
        self.action_list=action_list
        V_K=Value_knowledge(address,action_list)
        self.png_path=path
        self.distribution_list=V_K.attribute_List

        self.Drew()
        #self.Drew_Real()
    def Rainbown_color(self,length):
        R=0xff
        G_begin=0x66
        B_begin=0x66
        step=G_begin//length
        color='#'
        colors=[]
        for i in range(0,length):
            #color=color+str(hex(R))+str(hex(B_begin+step*i))+str(hex(G_begin-step*i))
            color=color+self.translate_sixteen_string(R)+self.translate_sixteen_string(B_begin+step*i)+self.translate_sixteen_string(B_begin-step*i)
            colors.append(color)
            color='#'
        #for co in colors:
        #    print co
        return colors


    def translate_sixteen_string(self,value):
        if abs(value)<0x10:
            #print value, '           ', 0x10
            result='0'
            result=result+str(hex(value)).split('x')[-1]
        else:
         result=str(hex(value)).split('x')[-1]
        return result   


    def Detect_Inforative_levels(self,list):
         result=[]
         for i in range(0,len(list)):
             for j in list[i]:
                 if j!=0:
                    result.append(i)
                    break
         print result
         return result


    def Drew(self):
        fig=plt.figure(figsize=(10, 10), dpi=150)
        ax1=fig.add_subplot(111,projection='3d')
        z_first=np.asarray( self.distribution_list[0])
        z=z_first.T


        
        xlabels_t=[]       
        for i in range(0,len(z)):
            xlabels_t.append(str(i))
        xlabels=np.array(xlabels_t)
        xpos=np.arange(xlabels.shape[0])

        ylabels_t=[]       
        for i in range(0,len(z[0])):
            ylabels_t.append(str(i))
        ylabels=np.array(ylabels_t)
        ypos=np.arange(ylabels.shape[0])



        xposM, yposM=np.meshgrid(xpos,ypos,copy=False)

        dx=0.3
        dy=0.1

        ax1.w_xaxis.set_ticks(xpos + dx/2.)
        ax1.w_xaxis.set_ticklabels(xlabels)

        ax1.w_yaxis.set_ticks(ypos + dy/3.)
        ax1.w_yaxis.set_ticklabels(ylabels)

        color_list=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan','tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

        line_list=['--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':']
        #for act in range(6,7):
        for act in range(0,len(self.action_list)):
            important_list=self.Detect_Inforative_levels(self.distribution_list[act])
            z_first=np.asarray( self.distribution_list[act])
            z=z_first.T

            y=[]

            for i in range(0,len(z[0])):
                y.append(i)



            for i in range(0,len(z)):
                x=[i]*len(z[i])
                if len(z)>=20:

                    ax1.plot(x, y, z[i], line_list[act],color=color_list[act],lw=3,alpha=3)

                    ax1.legend()
                    for j in range(0,len(z[i])):
                        if z[i][j] !=0 and i%4==0:

                            ax1.text(i, j, z[i][j]+0.1, str(round(z[i][j],2)), color=color_list[act])  
                else:
                    ax1.plot(x, y, z[i], line_list[act], color=color_list[act],lw=2)
                    ax1.legend()
                    for j in range(0,len(z[i])):
                        if z[i][j]>0:
                            ax1.text(i, j, z[i][j]+0.01, str(round(z[i][j],2)), color=color_list[act])
   
        



            
            #y=[]
            #count=0
            #for i in range(0,len(z_first[0])):
            #    y.append(i)
         
            #for level in important_list:
            #    x=[level]*len(z_first[level])
            #    n_z=z_first[level]
            
            #    ax1.plot( y, x,n_z, '--', color=color_list[count],lw=1,alpha=3)

                    
            #    ax1.scatter(y, x,n_z,color=color_list[count]) 
            #    count+=1
            #    if count>len(color_list):
            #        count=0

            
                       


        ax1.set_xlabel('X ', fontsize=20)
        #ax1.set_title('6-BIT MUX', fontsize=30)
        ax1.set_ylabel('Y', fontsize=20)
        ax1.set_zlabel("Z", fontsize=20)

        for angle in range(1, 360,30):
            ax1.view_init(30, angle)
            plt.draw()
            png_complete_name = self.png_path + str(angle) + ".png"
            # fig.savefig(png_complete_name, dpi=(400))
            #fig.savefig(png_complete_name,bbox_inches='tight')
            fig.savefig(png_complete_name)
            plt.pause(.001)

    def Drew_Real(self):
        fig=plt.figure(figsize=(10, 10), dpi=150)
        ax1=fig.add_subplot(111,projection='3d')
        z_first=np.asarray( self.distribution_list[0])
        z=z_first.T


        
        
        action_list=['Mammal','Bird','Reptile','Fish','Amphibian','Insect','Sea_others']
        color_list=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan','tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

        line_list=['--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':']
        path_list=['UCS_V\\ZOO0\\','UCS_V\\ZOO1\\','UCS_V\\ZOO2\\','UCS_V\\ZOO3\\','UCS_V\\ZOO4\\','UCS_V\\ZOO5\\','UCS_V\\ZOO6\\']
        #for act in range(6,7):
        for act in range(0,len(self.action_list)):
            xlabels_t=[]       
            for i in range(0,len(z)):
                xlabels_t.append(str(i))

            #xlabels_t=['hair','feathers','eggs','milk','airborne','aquatic','predator','toothed','backbone','breathes','venomous','fins','legs','tail','domestic','catsize'] 
            xlabels=np.array(xlabels_t)
            xpos=np.arange(xlabels.shape[0])

            ylabels_t=[]       
            for i in range(0,len(z[0])):
                ylabels_t.append(str(i))
            ylabels=np.array(ylabels_t)
            ypos=np.arange(ylabels.shape[0])



            xposM, yposM=np.meshgrid(xpos,ypos,copy=False)

            dx=0.3
            dy=0.1

            ax1.w_xaxis.set_ticks(xpos + dx/2.)
            #ax1.w_xaxis.set_ticks(xpos + dx*5)
            ax1.w_xaxis.set_ticklabels(xlabels)

            ax1.w_yaxis.set_ticks(ypos + dy/3.)
            ax1.w_yaxis.set_ticklabels(ylabels)

            important_list=self.Detect_Inforative_levels(self.distribution_list[act])
            z_first=np.asarray( self.distribution_list[act])
            z=z_first.T

            y=[]

            for i in range(0,len(z[0])):
                y.append(i)



            for i in range(0,len(z)):
                x=[i]*len(z[i])
                if len(z)>=20:

                    ax1.plot(x, y, z[i], line_list[act],color=color_list[act],lw=3,alpha=3)

                    ax1.legend()
                    for j in range(0,len(z[i])):
                        if z[i][j] !=0 and i%4==0:

                            ax1.text(i, j, z[i][j]+0.1, str(round(z[i][j],2)), color=color_list[act])  
                else:
                    ax1.plot(x, y, z[i], line_list[act], color=color_list[act],lw=2)
                    ax1.legend()
                    for j in range(0,len(z[i])):
                        if z[i][j]>0:
                            ax1.text(i, j, z[i][j]+0.01, str(round(z[i][j],2)), color=color_list[act])
   
        



            
            #y=[]
            #count=0
            #for i in range(0,len(z_first[0])):
            #    y.append(i)
         
            #for level in important_list:
            #    x=[level]*len(z_first[level])
            #    n_z=z_first[level]
            
            #    ax1.plot( y, x,n_z, '--', color=color_list[count],lw=1,alpha=3)

                    
            #    ax1.scatter(y, x,n_z,color=color_list[count]) 
            #    count+=1
            #    if count>len(color_list):
            #        count=0

            
                       


            ax1.set_xlabel('X ', fontsize=20)
            ax1.set_title(action_list[act], fontsize=30)
            ax1.set_ylabel('Y', fontsize=20)
            ax1.set_zlabel("Z", fontsize=20)

            for angle in range(1, 360,20):
                ax1.view_init(30, angle)
                plt.draw()
                png_complete_name = path_list[act] + str(angle) + ".png"
                # fig.savefig(png_complete_name, dpi=(400))
                fig.savefig(png_complete_name,bbox_inches='tight')
                #fig.savefig(png_complete_name)
                plt.pause(.001)

            ax1.clear()

class Value_knowledge_boundary:
    def __init__(self,address,action_list):


        Read_UCS=Read_Natural_UCS_Solution(address)

        self.action_list=action_list

        self.Raw_Population=Read_UCS.population

        self.clustered=self.Conver_to_Cluster()

        self.attribute_List_up=self.Calculate_Attribute_importance_distribution_upper()

        self.attribute_List_lower=self.Calculate_Attribute_importance_distribution_lower()

        
        
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


    def General_Level(self,condition):
        count=0
        for cod in condition:
            if cod=='#':
                count+=1
        return count

    def Calculate_Attribute_importance_distribution_upper(self):
        
        #Initial the action based distribution list
        distribution_list=[]
        length=len(self.Raw_Population[0][0])
        #print len(self.negative_set)
        for i in range(0,len(self.clustered)):
            temp=[]
            for j in range(0,length):               
                temp.append(0)
            distribution_list.append(temp)

        #Action distributed list
        G_distribution_list=[]
        for i in range(0,len(self.action_list)):
            temp=copy.deepcopy(distribution_list)
            G_distribution_list.append(temp)

        G_count_list=copy.deepcopy(G_distribution_list)

        

        #Z_count_list=copy.deepcopy(G_distribution_list)

        #Z_distribution_list=copy.deepcopy(G_distribution_list)


        #print distribution_list
        for i in range(0,len(self.clustered)):
            if len(self.clustered[i])!=0:
                for rule in self.clustered[i]:
                    for cond_l in range(0,length):
                        if rule[0][cond_l]!='#':
                            G_count_list[rule[1]][i][cond_l]+=1

                            if rule[0][cond_l]>G_distribution_list[rule[1]][i][cond_l]:
                                G_distribution_list[rule[1]][i][cond_l]=rule[0][cond_l]
                                
                        #elif rule[0][cond_l]==0:

                for d_l in range(0,length):
                    for action in self.action_list:

                        if G_count_list[action][i][d_l]!=0:
                            #G_distribution_list[action][i][d_l]=1.0*G_distribution_list[action][i][d_l]/G_count_list[action][i][d_l]
                            if G_distribution_list[action][i][d_l]==0:
                                G_distribution_list[action][i][d_l]=-1
        print (G_distribution_list)
        #print len(distribution_list)



        return G_distribution_list

    def Calculate_Attribute_importance_distribution_lower(self):
        
        #Initial the action based distribution list
        distribution_list=[]
        length=len(self.Raw_Population[0][0])
        #print len(self.negative_set)
        for i in range(0,len(self.clustered)):
            temp=[]
            for j in range(0,length):               
                temp.append(0)
            distribution_list.append(temp)

        #Action distributed list
        G_distribution_list=[]
        for i in range(0,len(self.action_list)):
            temp=copy.deepcopy(distribution_list)
            G_distribution_list.append(temp)

        G_count_list=copy.deepcopy(G_distribution_list)

        G_distribution_list=copy.deepcopy(self.attribute_List_up)

        #Z_count_list=copy.deepcopy(G_distribution_list)

        #Z_distribution_list=copy.deepcopy(G_distribution_list)


        #print distribution_list
        for i in range(0,len(self.clustered)):
            if len(self.clustered[i])!=0:
                for rule in self.clustered[i]:
                    for cond_l in range(0,length):
                        if rule[0][cond_l]!='#':
                            G_count_list[rule[1]][i][cond_l]+=1

                            if rule[0][cond_l]<G_distribution_list[rule[1]][i][cond_l]:
                                G_distribution_list[rule[1]][i][cond_l]=rule[0][cond_l]
                                
                        #elif rule[0][cond_l]==0:

            for d_l in range(0,length):
                    for action in self.action_list:
                        if G_count_list[action][i][d_l]!=0:
                            #G_distribution_list[action][i][d_l]=1.0*G_distribution_list[action][i][d_l]/G_count_list[action][i][d_l]
                            if G_distribution_list[action][i][d_l]==0:
                                G_distribution_list[action][i][d_l]=-1
        print (G_distribution_list)
        #print len(distribution_list)



        return G_distribution_list


class Visualize_value_pattern_boundary:
    def __init__(self,address,action_list,path):
        self.action_list=action_list
        V_K=Value_knowledge_boundary(address,action_list)
        self.png_path=path
        self.distribution_list_U=V_K.attribute_List_up
        self.distribution_list_L=V_K.attribute_List_lower

        
        self.Drew_Real()
    def Rainbown_color(self,length):
        R=0xff
        G_begin=0x66
        B_begin=0x66
        step=G_begin//length
        color='#'
        colors=[]
        for i in range(0,length):
            #color=color+str(hex(R))+str(hex(B_begin+step*i))+str(hex(G_begin-step*i))
            color=color+self.translate_sixteen_string(R)+self.translate_sixteen_string(B_begin+step*i)+self.translate_sixteen_string(B_begin-step*i)
            colors.append(color)
            color='#'
        #for co in colors:
        #    print co
        return colors


    def translate_sixteen_string(self,value):
        if abs(value)<0x10:
            #print value, '           ', 0x10
            result='0'
            result=result+str(hex(value)).split('x')[-1]
        else:
         result=str(hex(value)).split('x')[-1]
        return result   


    def Detect_Inforative_levels(self,list):
         result=[]
         for i in range(0,len(list)):
             for j in list[i]:
                 if j!=0:
                    result.append(i)
                    break
         print result
         return result



    def Drew_Real(self):
        fig=plt.figure(figsize=(10, 10), dpi=150)
        ax1=fig.add_subplot(111,projection='3d')
        z_first=np.asarray( self.distribution_list_U[0])
        z=z_first.T


        
        
        action_list=['Mammal','Bird','Reptile','Fish','Amphibian','Insect','Sea_others']
        color_list=['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan','tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

        line_list=['--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':','--',':']
        #path_list=['UCS_V\\ZOO0\\','UCS_V\\ZOO1\\','UCS_V\\ZOO2\\','UCS_V\\ZOO3\\','UCS_V\\ZOO4\\','UCS_V\\ZOO5\\','UCS_V\\ZOO6\\']
        path_list=['UCS_V\\NZOO0\\','UCS_V\\NZOO1\\','UCS_V\\NZOO2\\','UCS_V\\NZOO3\\','UCS_V\\NZOO4\\','UCS_V\\NZOO5\\','UCS_V\\NZOO6\\']
        #for act in range(6,7):
        for act in range(0,len(self.action_list)):
            for face in range(0,2):
                xlabels_t=[]       
                for i in range(0,len(z)):
                    xlabels_t.append(str(i))

                #xlabels_t=['hair','feathers','eggs','milk','airborne','aquatic','predator','toothed','backbone','breathes','venomous','fins','legs','tail','domestic','catsize'] 
                xlabels=np.array(xlabels_t)
                xpos=np.arange(xlabels.shape[0])

                ylabels_t=[]       
                for i in range(0,len(z[0])):
                    ylabels_t.append(str(i))
                ylabels=np.array(ylabels_t)
                ypos=np.arange(ylabels.shape[0])



                xposM, yposM=np.meshgrid(xpos,ypos,copy=False)

                dx=0.3
                dy=0.1

                ax1.w_xaxis.set_ticks(xpos + dx/2.)
                #ax1.w_xaxis.set_ticks(xpos + dx*5)
                ax1.w_xaxis.set_ticklabels(xlabels)

                ax1.w_yaxis.set_ticks(ypos + dy/3.)
                ax1.w_yaxis.set_ticklabels(ylabels)
                if face==0:
                    important_list=self.Detect_Inforative_levels(self.distribution_list_U[act])
                    z_first=np.asarray( self.distribution_list_U[act])
                    z=z_first.T
                elif face==1:
                    important_list=self.Detect_Inforative_levels(self.distribution_list_L[act])
                    z_first=np.asarray( self.distribution_list_L[act])
                    z=z_first.T


                y=[]

                for i in range(0,len(z[0])):
                    y.append(i)



                for i in range(0,len(z)):
                    x=[i]*len(z[i])
                    if len(z)>=20:

                        ax1.plot(x, y, z[i], line_list[act],color=color_list[act],lw=3,alpha=3)

                        ax1.legend()
                        for j in range(0,len(z[i])):
                            if z[i][j] !=0 and i%4==0:

                                ax1.text(i, j, z[i][j]+0.1, str(round(z[i][j],2)), color=color_list[act])  
                    else:
                        ax1.plot(x, y, z[i], line_list[act], color=color_list[act],lw=2)
                        ax1.legend()
                        for j in range(0,len(z[i])):
                            if z[i][j]>0:
                                ax1.text(i, j, z[i][j]+0.01, str(round(z[i][j],2)), color=color_list[act])
            
                       


                ax1.set_xlabel('X ', fontsize=20)
                #ax1.set_title(action_list[act], fontsize=30)
                ax1.set_ylabel('Y', fontsize=20)
                ax1.set_zlabel("Z", fontsize=20)

            for angle in range(1, 360,20):
                ax1.view_init(30, angle)
                plt.draw()
                png_complete_name = path_list[act] + str(angle) + ".png"
                # fig.savefig(png_complete_name, dpi=(400))
                #fig.savefig(png_complete_name,bbox_inches='tight')
                fig.savefig(png_complete_name)
                plt.pause(.001)

            ax1.clear()

#action_list=[0,1]
action_list=[0,1,2,3,4,5,6]
#add='Natural_Solution\\6_Carry.txt'
#PATH='UCS_V\\Carry_6V\\'

#add='Natural_Solution\\6_MUX.txt'
#PATH='UCS_V\\MUX_6V\\'


#add='Natural_Solution\\carry_8.txt'
#PATH='UCS_V\\Carry_8V\\'

#add='Natural_Solution\\6_MajorityOn.txt'
#PATH='UCS_V\\Majority6V\\'

#add='Natural_Solution\\7_MajorityOn.txt'
#PATH='UCS_V\\Majority7V\\'

#add='Natural_Solution\\8_MajorityOn.txt'
#PATH='UCS_V\\Majority8V\\'

#add='Natural_Solution\\11_MUX.txt'
#PATH='UCS_V\\11_MUX\\'

#add='Natural_Solution\\20_MUX.txt'
#PATH='UCS_V\\20_MUX\\'

#add='Natural_Solution\\10_Majority.txt'
#PATH='UCS_V\\Majority_10\\'


#add='Natural_Solution\\12_carry.txt'
#PATH='UCS_V\\12_carry\\'

#add='Natural_Solution\\10_carry.txt'
#PATH='UCS_V\\10_carry\\'

#add='Natural_Solution\\9_MajorityOn.txt'
#PATH='UCS_V\\Majority_9\\'

#add='Natural_Solution\\ZOO.txt'
#PATH='UCS_V\\ZOOV\\'

#add='Natural_Solution\\Poly_ZOO.txt'
#add='Natural_Solution\\ZOO_RICH_OPTIMAL.txt'
#add='Natural_Solution\\ZOO_Absumption_100k_Positive.txt'
add='Natural_Solution\\ZOO_Absumption_100k_Negative.txt'
PATH='UCS_V\\ZOO_P\\'

#Visualize_value_pattern(add,action_list,PATH)
Visualize_value_pattern_boundary(add,action_list,PATH)